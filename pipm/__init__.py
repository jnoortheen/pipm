#! /usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import

__version__ = '10.4.0'

from pip import _internal as p

# patch for program name
from pipm.commands import InstallCommandPlus, UninstallCommandPlus, UpdateCommand, FreezeCommandPlus


def get_prog():
    return 'pipm'


p.get_prog = get_prog

p.commands_dict[InstallCommandPlus.name] = InstallCommandPlus
p.commands_dict['i'] = InstallCommandPlus

p.commands_dict[UninstallCommandPlus.name] = UninstallCommandPlus
p.commands_dict['rm'] = UninstallCommandPlus

p.commands_dict[FreezeCommandPlus.name] = FreezeCommandPlus
p.commands_dict['save'] = FreezeCommandPlus

p.commands_dict['update'] = UpdateCommand
p.commands_dict['upgrade'] = UpdateCommand
p.commands_dict['u'] = UpdateCommand


# endpatch

def main():
    p.main()


if __name__ == '__main__':
    main()
