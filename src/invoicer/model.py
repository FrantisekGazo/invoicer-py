#####################################################################################
# Base
#####################################################################################
class CurrencyImpl(object):
    def __init__(self, name, sign):
        self.name = name
        self.sign = sign


class Currency(object):
    EUR = CurrencyImpl('EUR', u'\u20ac')
    NONE = CurrencyImpl('', u'')

    all = [EUR]

    @staticmethod
    def for_name(name):
        for currency in Currency.all:
            if currency.name == name:
                return currency
        return Currency.NONE


class ProjectType(object):
    MOBILE = 'mobile'
    DESKTOP = 'desktop'

    all = [MOBILE, DESKTOP]

    @staticmethod
    def validate(name):
        if name in ProjectType.all:
            return name
        else:
            return None


class Base(object):
    def __init__(self, data):
        self.contractor = Contractor(data)
        self.numbering = data['numbering']
        self.default_curremcy = Currency.for_name(data['default_curremcy'])
        self.default_bank_account_name = data['default_bank_account']
        self.bank_accounts = {}
        for (acc_name, acc_data) in data['bank_accounts'].iteritems():
            self.bank_accounts[acc_name] = BankAccount(acc_data)

        self.clients = {}
        for (client_name, client_data) in data['clients'].iteritems():
            self.clients[client_name] = Client(client_data)


class Contractor(object):
    def __init__(self, data):
        self.name = data['name']
        self.address = data['address']
        self.ico = data['ico']
        self.dic = data['dic']
        self.icdph = data['icdph']
        self.phone = data['phone']
        self.email = data['email']
        self.signature = data['signature']


class Client(object):
    def __init__(self, data):
        self.name = data['name']
        self.order = data.get('order', 0)
        self.address = data['address']
        self.ico = data['ico']
        self.dic = data['dic']
        self.icdph = data['icdph']
        self.price = data['price']
        self.projects = {}
        for (project_name, project_data) in data.get('projects', {}).iteritems():
            self.projects[project_name] = Project(project_name, project_data, default_price=self.price)

    def is_foreign(self):
        return self.address[len(self.address) - 1] != 'Slovensko'


class Project(object):
    def __init__(self, name, data, default_price):
        self.name = name
        self.type = ProjectType.validate(data['type'])
        self.aliases = data.get('aliases', []) + [name]
        self.price = data.get('price', default_price)


class BankAccount(object):
    def __init__(self, data):
        self.iban = data['iban']
        self.swift = data['swift']


#####################################################################################
# Document
#####################################################################################
class Document(object):
    def __init__(self, number, due_date, issue_date, delivery_date, contractor, bank_account, currency, client, items,
                 discount=0):
        self.number = number
        self.due_date = due_date
        self.issue_date = issue_date
        self.delivery_date = delivery_date

        self.contractor = contractor
        self.bank_account = bank_account
        self.currency = currency

        self.client = client
        self.discount = discount
        self.items = items

    def total(self):
        return self._item_total() - self.discount

    def _item_total(self):
        sum = 0
        for item in self.items:
            sum += item.total()
        return sum

    def discount_percentage(self):
        return self.discount / self._item_total() * 100


class Item(object):
    def __init__(self, name, amount, unit, price):
        self.name = name
        self.amount = amount
        self.unit = unit
        self.price = price

    def total(self):
        return self.amount * self.price


class Unit(object):
    KS = 'ks'
    HOUR = 'hod'


#####################################################################################
# Input Record
#####################################################################################


class Record(object):
    pass


class DiscountRecord(Record):
    def __init__(self, client_name, price):
        self.client_name = client_name
        self.price = price


class HoursRecord(Record):
    def __init__(self, project_name, hours):
        self.project_name = project_name
        self.hours = hours


class PriceRecord(Record):
    def __init__(self, project_name, price):
        self.project_name = project_name
        self.price = price
