from collections import OrderedDict

from pip._internal.req import InstallRequirement
from .file_utils import parse_comes_from


class OrderedDefaultDict(OrderedDict):
    def __init__(self, factory, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.factory = factory

    def __missing__(self, key):
        self[key] = value = self.factory()
        return value


class FileRequirement:
    def __init__(self, req, env):
        # type: (InstallRequirement, str) -> None
        filename, line_num = parse_comes_from(req.comes_from, env)
        self.req = req
        self.filename = filename
        self.line_num = line_num

    def __repr__(self):
        return "Freq<{}>".format(self.req)
