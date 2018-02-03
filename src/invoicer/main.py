import argparse

from util import load_yaml
from resource import ResourceManager
from builder import DocumentBuilder
from doc_manager import DocManager
import input_parser
import os


def run(resources):
    doc_manager = DocManager(resources)
    latest_doc_name = doc_manager.get_latest_doc_name()

    # retrieve input
    # TODO : tempo timesheets API : https://tempoplugin.jira.com/wiki/spaces/JTS/pages/120389685/Timesheets+REST+API
    records = input_parser.parse(os.path.abspath('IN'))

    # prepare documents
    builder = DocumentBuilder(load_yaml('base.yaml'), resources, latest_doc_name)
    docs = builder.build(records)

    # create documents
    doc_manager.clear_pending()
    for doc in docs:
        doc_manager.make_pending(doc)


def sent(resources, doc_number):
    doc_manager = DocManager(resources)
    doc_manager.move_to_sent(doc_number)


def paid(resources, doc_number):
    doc_manager = DocManager(resources)
    doc_manager.move_to_paid(doc_number)


def main(debug=False):
    parser = argparse.ArgumentParser()
    parser.add_argument('-r', '--run', action='store_true',
                        help="Create new documents")
    parser.add_argument('-s', '--sent', nargs=1, metavar="DOC_NUMBER",
                        help="Move the document with given number to the sent state")
    parser.add_argument('-p', '--paid', nargs=1, metavar="DOC_NUMBER",
                        help="Move the document with given number to the paid state")
    args = parser.parse_args()

    if args.run:
        run(ResourceManager(debug))
    elif args.sent is not None:
        sent(ResourceManager(debug), args.sent[0])
    elif args.paid is not None:
        paid(ResourceManager(debug), args.paid[0])


if __name__ == "__main__":
    main(debug=True)
