from collections import OrderedDict


class OrderedDefaultDict(OrderedDict):
    def __init__(self, factory, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.factory = factory

    def __missing__(self, key):
        self[key] = value = self.factory()
        return value

class FileRequirement:
    def __init__(self, req, env):
        # type: (object, str) -> None
        filename, line_num = parse_comes_from(req.comes_from, env)

        self.filename = filename
        self.line_num = line_num

