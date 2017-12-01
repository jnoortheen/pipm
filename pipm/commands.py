from __future__ import absolute_import

from pip.commands import InstallCommand, UninstallCommand, FreezeCommand

from pipm.operations import get_orphaned_packages
from . import file


def store_req_environment(option, opt_str, value, parser, *args, **kwargs):
    parser.values.req_environment = opt_str.strip('-')


class InstallCommandPlus(InstallCommand):
    def __init__(self, *args, **kw):
        """

        Args:
            *args:
            **kw:
        """
        super(InstallCommandPlus, self).__init__(*args, **kw)

        cmd_opts = self.cmd_opts

        cmd_opts.add_option(
            '--dev',
            dest='req_environment',
            action='callback',
            callback=store_req_environment,
            help="Save package requirements to `dev-requirements.txt` or `requirements/dev.txt` or"
                 " `requirements/development.txt`"
        )

        cmd_opts.add_option(
            '--all',
            dest='req_environment',
            action='callback',
            callback=store_req_environment,
            help="install all requirements from all environments. (E.g. `pipm install --all` will install "
                 "requirements from all requirements-*.txt files.)"
        )

        cmd_opts.add_option(
            '--test',
            dest='req_environment',
            action='callback',
            callback=store_req_environment,
            help="Save package requirements to `test-requirements.txt` or `requirements/test.txt` or"
                 " `requirements/test.txt`"
        )

        cmd_opts.add_option(
            '--prod',
            dest='req_environment',
            action='callback',
            callback=store_req_environment,
            help="Save package requirements to `prod-requirements.txt` or `requirements/production.txt` or"
                 " `requirements/prod.txt`"
        )

        cmd_opts.add_option(
            '--env',
            dest='req_environment',
            action='store',
            help="Save package requirements to `prod-requirements.txt` or `requirements/production.txt` or"
                 " `requirements/prod.txt`"
        )

    def parse_args(self, args):
        """
            when no argument given it fills with `-r requirements.txt` as default
        Args:
            args (list):

        Returns:
            options, list:
        """
        options, args = super(InstallCommandPlus, self).parse_args(args)
        if not options.requirements and ((len(args) == 1 and set(args) == {'--all'}) or not args):
            env = options.req_environment
            upgrade = options.upgrade

            if env == 'all':
                req_args = []
                for req in file.get_req_filenames():
                    req_args.append('-r')
                    req_args.append(req)
            else:
                req_args = ['-r', file.get_req_filename(env)]
            options, args = super(InstallCommandPlus, self).parse_args(req_args)
            options.req_environment = env
            options.upgrade = upgrade
            options.no_save = True

        return options, args

    def run(self, options, args):
        """
            wrapper around pip.commands.InstallCommand
        Args:
            options:
            args:

        Returns:
            pip.req.RequirementSet:
        """
        result = super(InstallCommandPlus, self).run(options, args, )

        if not hasattr(options, 'no_save'):
            # save changes to file if any
            file.save(options.req_environment)

        return result


class FreezeCommandPlus(FreezeCommand):
    """
        A wrapper around standard freeze command that updates currently installed packages to requirement files
        after showing the packages list in standard output.
    """

    def run(self, options, args):
        res = super(FreezeCommandPlus, self).run(options, args)

        file.save()

        return res


class UninstallCommandPlus(UninstallCommand):
    """
        a drop-in replacement of pip's uninstall command. It removes the entry from requirements file after a package
        is removed.
    """

    def run(self, options, args):
        removable_pkgs = get_orphaned_packages(args)

        if removable_pkgs:
            print('Following packages are no longer required by any of the installed packages: \n', '\n'.join(
                removable_pkgs))

        res = super(UninstallCommandPlus, self).run(options, (args + list(removable_pkgs)))

        file.save()

        return res


class UpdateCommand(InstallCommandPlus):
    name = 'update'

    usage = """
          %prog [environment-to-update]
          %prog [package-names-to-update]"""

    summary = 'Update packages (equivalent to that of `install` with --upgrade)'

    def parse_args(self, args):
        """
            when no argument given it fills with `-r requirements.txt` as default
        Args:
            args (list):

        Returns:
            options, list:
        """
        return super(UpdateCommand, self).parse_args(args + ['--upgrade'])
