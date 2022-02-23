from pip._internal.req import InstallRequirement

from .file_utils import parse_comes_from


class FileRequirement:
    def __init__(self, req, env):
        # type: (InstallRequirement, str) -> None
        filename, line_num = parse_comes_from(req.comes_from, env)
        self.req = req
        self.filename = filename
        self.line_num = line_num

    def __repr__(self):
        return "{}".format(self.req)
