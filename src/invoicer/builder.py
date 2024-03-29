from model import *
from datetime import datetime, timedelta
from resource import ResourceManager


def _last_day_of_month(any_date):
    next_month = any_date.replace(day=28) + timedelta(days=4)  # move to next month - this will never fail
    return next_month - timedelta(days=next_month.day)


def _last_day_of_previous_month(any_date):
    return any_date.replace(day=1) + timedelta(days=-1)  # move to previous month


class DocumentBuilder(object):
    def __init__(self, base, latest_doc_name):
        self.base = Base(base)
        self.latest_doc_name = latest_doc_name

    def build(self, records, delivery_date=None, due_eom=False):
        if delivery_date is None:
            today = datetime.now()
            if today.day < 15:
                delivery_date = _last_day_of_previous_month(today)
            else:
                delivery_date = _last_day_of_month(today)

        if due_eom:
            due_date = _last_day_of_month(delivery_date)
        else:
            due_date = delivery_date + timedelta(days=14)

        docs = []

        # create temporary documents and sort them base on client order
        temp_docs = []
        for (client_key, client) in self.base.clients.items():
            items = self._find_items(records, client)
            if items is None:
                continue
            items.sort(key=lambda i: i.name)
            discount = self._find_discount(records, client_key)
            temp_docs.append(TempDoc(client, items, discount))
        temp_docs = sorted(temp_docs, key=lambda c: c.client.order)

        # create documents
        for temp_doc in temp_docs:
            # ignore documents with no item
            if len(temp_doc.items) < 1:
                continue

            doc_name = self._check_format_doc_name(delivery_date, len(docs) + 1)
            docs.append(Document(
                number=doc_name,

                issue_date=self._format_date(delivery_date),
                delivery_date=self._format_date(delivery_date),
                due_date=self._format_date(due_date),

                contractor=self.base.contractor,
                currency=self.base.default_currency,
                bank_account=self.base.bank_accounts[self.base.default_bank_account_name],

                client=temp_doc.client,
                discount=temp_doc.discount,
                items=temp_doc.items
            ))

        return docs

    def _format_doc_name(self, date, num):
        numbering = self.base.numbering
        if numbering == 'YYYYMMccc':
            return "{:%Y%m}{:03d}".format(date, num)
        elif numbering == 'YYYYccc':
            return "{:%Y}{:03d}".format(date, num)
        else:
            return None

    def _check_format_doc_name(self, date, num):
        n = self._format_doc_name(date, num)
        if self.latest_doc_name is None or n[:-3] != self.latest_doc_name[:-3]:
            return n
        else:
            latest = int(self.latest_doc_name[-3:])
            return self._format_doc_name(date, num + latest)

    def _format_date(self, date):
        return "{:%d.%m.%Y}".format(date)

    def _find_discount(self, records, client_name):
        discount = 0
        used_records = []

        for record in records:
            if isinstance(record, DiscountRecord):
                if record.client_name == client_name:
                    discount += record.price
                    used_records.append(record)

        for record in used_records:
            records.remove(record)
        return discount

    def _find_items(self, records, client):
        items = []
        used_records = []
        resources = ResourceManager(res_type=client.type)

        for record in records:
            if isinstance(record, PriceRecord) or isinstance(record, HoursRecord):
                for (_, project) in client.projects.items():
                    if record.project_name in project.aliases:
                        items.append(self._map_record_to_item(project, record, resources))
                        used_records.append(record)
                        break

        for record in used_records:
            records.remove(record)
        return self._combine_same_items(items, resources)

    def _map_record_to_item(self, project, record, resources):
        if isinstance(record, HoursRecord):
            return Item(
                name=resources.get_string('item_name_' + project.type, project.name),
                amount=record.hours,
                unit=resources.get_string('unit_hod'),
                price=project.price
            )
        elif isinstance(record, PriceRecord):
            if project.type == ProjectType.GENERAL:
                return Item(
                    name=resources.get_string('item_name_general'),
                    amount=1,
                    unit=resources.get_string('unit_ks'),
                    price=record.price
                )
            if project.type == ProjectType.PROVISION:
                return Item(
                    name=resources.get_string('item_name_provision'),
                    amount=1,
                    unit=resources.get_string('unit_ks'),
                    price=record.price
                )
            else:
                return Item(
                    name=resources.get_string('item_name_ks', project.name),
                    amount=1,
                    unit=resources.get_string('unit_ks'),
                    price=record.price
                )

    def _combine_same_items(self, items_list, resources):
        items_map = {}

        for item in items_list:
            if item.name in items_map:
                old = items_map[item.name]
                if item.unit == resources.get_string('unit_hod'):
                    items_map[item.name] = Item(
                        name=item.name,
                        price=item.price,
                        amount=item.amount + old.amount,
                        unit=item.unit
                    )
                else:
                    items_map[item.name] = Item(
                        name=item.name,
                        price=item.price + old.price,
                        amount=item.amount,
                        unit=item.unit
                    )
            else:
                items_map[item.name] = item

        return list(items_map.values())


class TempDoc(object):
    def __init__(self, client, items, discount):
        self.client = client
        self.items = items
        self.discount = discount
