import csv
from model import *

HOUR_CHARACTER = 'h'


def parse(file_path):
    records = []

    with open(file_path, 'rb') as csvfile:
        rows = csv.reader(csvfile, delimiter=' ', quotechar='|')
        for row in rows:
            parts_count = len(row)
            if parts_count <= 0 or parts_count < 2:
                continue

            number = float(row[0])

            if number == 0:
                continue
            elif number < 0:
                records.append(DiscountRecord(client_name=create_name(row, 1), price=-number))
            else:  # number > 0
                second_word = str(row[1])
                if second_word == HOUR_CHARACTER:
                    records.append(HoursRecord(project_name=create_name(row, 2), hours=number))
                else:
                    records.append(PriceRecord(project_name=create_name(row, 1), price=number))

    return records


def create_name(words, start_index):
    return ' '.join(words[start_index:])
