#! /usr/bin/env python
# -*- coding: utf-8 -*-

__version__ = '0.9'

import pip
import pip.basecommand
import pip.operations.freeze
import pip.utils

# patch for program name
from pipm.commands import InstallCommandPlus, UninstallCommandPlus, UpdateCommand, FreezeCommandPlus


def get_prog():
    return 'pipm'


pip.get_prog = get_prog
pip.utils.get_prog = get_prog
pip.basecommand.get_prog = get_prog
pip.commands_dict[InstallCommandPlus.name] = InstallCommandPlus
pip.commands_dict[UninstallCommandPlus.name] = UninstallCommandPlus
pip.commands_dict[FreezeCommandPlus.name] = FreezeCommandPlus
pip.commands_dict['save'] = FreezeCommandPlus
pip.commands_dict['i'] = InstallCommandPlus
pip.commands_dict['rm'] = UninstallCommandPlus
pip.commands_dict['update'] = UpdateCommand
pip.commands_dict['upgrade'] = UpdateCommand


# endpatch

def main():
    pip.main()


if __name__ == '__main__':
    main()
