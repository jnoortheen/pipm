#! /usr/bin/env python
# -*- coding: utf-8 -*-
__version__ = '0.1'

import sys

import pip
import pip.utils
import pip.basecommand
import pip.operations.freeze

# patch for program name
from pipm.commands import InstallCommandPlus


def get_prog():
    return 'pipm'


pip.get_prog = get_prog
pip.utils.get_prog = get_prog
pip.basecommand.get_prog = get_prog
pip.commands_dict[InstallCommandPlus.name] = InstallCommandPlus
# endpatch


if __name__ == '__main__':
    sys.exit(pip.main())
