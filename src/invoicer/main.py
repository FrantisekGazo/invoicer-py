import argparse

from datetime import datetime
from util import load_yaml
from resource import ResourceManager
from builder import DocumentBuilder
from doc_manager import DocManager
import input_parser
import os


def run(date=None):
    doc_manager = DocManager()
    latest_doc_name = doc_manager.get_latest_doc_name()

    # retrieve input
    # TODO : tempo timesheets API : https://tempoplugin.jira.com/wiki/spaces/JTS/pages/120389685/Timesheets+REST+API
    records = input_parser.parse(os.path.abspath('IN'))

    # prepare documents
    builder = DocumentBuilder(load_yaml('base.yaml'), latest_doc_name)
    docs = builder.build(records, date=date)

    # create documents
    doc_manager.clear_pending()
    for doc in docs:
        doc_manager.make_pending(doc)


def sent():
    doc_manager = DocManager()
    doc_manager.move_to_sent()


def paid():
    doc_manager = DocManager()
    doc_manager.move_to_paid()


def main(debug=False):
    parser = argparse.ArgumentParser()
    parser.add_argument('-r', '--run', action='store_true',
                        help="Create new documents")
    parser.add_argument('-rt', '--run-today', action='store_true',
                        help="Create new documents with today date")
    parser.add_argument('-s', '--sent', action='store_true',
                        help="Move the document with given number to the sent state")
    parser.add_argument('-p', '--paid', action='store_true',
                        help="Move the document with given number to the paid state")
    args = parser.parse_args()

    ResourceManager.debug = debug
    if args.run:
        run()
    if args.run_today:
        run(date=datetime.now())
    elif args.sent:
        sent()
    elif args.paid:
        paid()


if __name__ == "__main__":
    main(debug=True)
