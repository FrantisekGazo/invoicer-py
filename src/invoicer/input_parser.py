import csv
from model import *

HOUR_CHARACTER = 'h'


def parse(file_path):
    records = []

    with open(file_path, 'rb') as csvfile:
        rows = csv.reader(csvfile, delimiter=' ', quotechar='|')
        current_client = ''
        for row in rows:
            parts_count = len(row)

            if parts_count < 1:
                continue
            elif parts_count == 1:
                if not is_number(row[0]):
                    current_client = row[0]
                    continue

            record = parse_record(current_client, row)
            records.append(record)

    return records


def parse_record(client, row):
    number = float(row[0])

    if number == 0:
        return None
    elif number < 0:
        return DiscountRecord(
            client_name=client,
            price=-number
        )
    else:  # number > 0
        if len(row) > 1:
            second_word = str(row[1])
            if second_word == HOUR_CHARACTER:
                return HoursRecord(
                    client_name=client,
                    project_name=create_name(row, 2),
                    hours=number
                )
            else:
                return PriceRecord(
                    client_name=client,
                    project_name=create_name(row, 1),
                    price=number
                )
        else:
            return PriceRecord(
                client_name=client,
                project_name=None,
                price=number
            )


def create_name(words, start_index):
    return ' '.join(words[start_index:])


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass

    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass

    return False
