import os

from reportlab.lib.utils import ImageReader
from pkg_resources import resource_filename
from util import load_yaml


class ResourceManager(object):
    def __init__(self, debug=False):
        if debug:  # this is only for local testing
            self.res_path = '../src/invoicer/res'
        else:  # this is used in release
            self.res_path = resource_filename("invoicer", "res")
        self.data = load_yaml(self.resource_path('values/strings.yaml'))

    def resource_path(self, relative_path):
        return os.path.join(self.res_path, relative_path)

    def get_string(self, key, value=None):
        if value is None:
            return self.data.get(key, "")
        else:
            return self.data.get(key, "") % value

    def get_image(self, name):
        return ImageReader(self.resource_path("imgs/%s.png" % name))

    def get_font(self, name):
        return self.resource_path("fonts/%s.ttf" % name)
