import os
import yaml
import shutil
from pdf_writer import PdfWriter
from serializer import doc_to_object, object_to_doc

BASE_PATH = './out'

DOC_PATH = 'doc'
PDF_PATH = 'pdf'

YAML_EXTENSION = '.yaml'
PDF_EXTENSION = '.pdf'


class DocState:
    PENDING = 'pending'
    SENT = 'sent'
    PAID = 'paid'


class DocManager(object):
    def __init__(self, resources):
        self._resources = resources

    def make_pending(self, doc):
        doc_dir_path = _prepare_dir(DOC_PATH, DocState.PENDING)
        pdf_dir_path = _prepare_dir(PDF_PATH, DocState.PENDING)

        _write_doc_to_yaml(doc_dir_path, doc)

        pdf_path = os.path.join(pdf_dir_path, _create_doc_pdf_name(doc.number))
        writer = PdfWriter(self._resources, pdf_path, doc)
        writer.write()

        print("%s was created" % doc.number)

    def move_to_sent(self):
        doc_numbers = self.get_doc_numbers_from(DocState.PENDING)
        for doc_number in doc_numbers:
            _move(DocState.PENDING, DocState.SENT, doc_number)
            print("%s was moved to sent state" % doc_number)

    def move_to_paid(self):
        doc_numbers = self.get_doc_numbers_from(DocState.SENT)
        for doc_number in doc_numbers:
            _move(DocState.SENT, DocState.PAID, doc_number)
            print("%s was moved to paid state" % doc_number)

    def clear_pending(self):
        shutil.rmtree(_prepare_dir(DOC_PATH, DocState.PENDING))
        shutil.rmtree(_prepare_dir(PDF_PATH, DocState.PENDING))
        print("Pending were cleared")

    def get_latest_doc_name(self):
        doc_files = self.get_doc_numbers_from(DocState.SENT) + self.get_doc_numbers_from(DocState.PAID)

        if len(doc_files) > 0:
            doc_files.sort()
            return doc_files[len(doc_files) - 1]
        else:
            return None

    def get_doc_numbers_from(self, state):
        doc_path = _prepare_dir(DOC_PATH, state)
        doc_numbers = [_strip_yaml_from_name(f) for f in os.listdir(doc_path)]
        return doc_numbers


def _prepare_dir(file_type, doc_state):
    dir_path = os.path.join(BASE_PATH, file_type, doc_state)
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    return dir_path


def _write_doc_to_yaml(path, doc):
    with open(os.path.join(path, _create_doc_yaml_name(doc.number)), 'w') as outfile:
        yaml.dump(doc_to_object(doc), outfile, default_flow_style=False)


def _read_doc_from_yaml(path, doc_number):
    with open(os.path.join(path, _create_doc_yaml_name(doc_number)), 'r') as infile:
        obj = yaml.load(infile)
    return object_to_doc(obj)


def _create_doc_yaml_name(doc_number):
    return str(doc_number) + YAML_EXTENSION


def _strip_yaml_from_name(file_name):
    return file_name[:-len(YAML_EXTENSION)]


def _create_doc_pdf_name(doc_number):
    return str(doc_number) + PDF_EXTENSION


def _move(from_state, to_state, doc_number):
    shutil.move(
        os.path.join(_prepare_dir(DOC_PATH, from_state), _create_doc_yaml_name(doc_number)),
        os.path.join(_prepare_dir(DOC_PATH, to_state), _create_doc_yaml_name(doc_number))
    )
    shutil.move(
        os.path.join(_prepare_dir(PDF_PATH, from_state), _create_doc_pdf_name(doc_number)),
        os.path.join(_prepare_dir(PDF_PATH, to_state), _create_doc_pdf_name(doc_number))
    )
