#! /usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import

import sys

from pip._internal.utils import misc


def get_prog():
    return "pipm"


# patch for program name
misc.get_prog = get_prog

from pip._internal import commands

from pipm.commands import (
    InstallCommandPlus,
    UninstallCommandPlus,
    UpdateCommand,
    FreezeCommandPlus,
)


def _update_command_info(cls, *names):
    old_info = commands.commands_dict.get(names[0])
    for n in names:
        commands.commands_dict[n] = commands.CommandInfo(
            cls.__module__, cls.__name__, old_info.summary if old_info else cls.summary
        )


# replace commands
for args in [
    (InstallCommandPlus, "install", "i", "add"),
    (UninstallCommandPlus, "uninstall", "rm"),
    (FreezeCommandPlus, "freeze", "save"),
    (UpdateCommand, "update", "upgrade", "u"),
]:
    _update_command_info(*args)


def is_venv():
    return hasattr(sys, "real_prefix") or (
        hasattr(sys, "base_prefix") and sys.base_prefix != sys.prefix
    )


from pip._internal.cli.main import main as pip_main


def main():
    if not is_venv():
        raise Exception("Please install `pipm` inside virtualenv")
    pip_main()


if __name__ == "__main__":
    sys.exit(main())
