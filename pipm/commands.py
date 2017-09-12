from __future__ import absolute_import

from pip import FrozenRequirement
from pip.commands import InstallCommand, UninstallCommand
from pkg_resources import DistInfoDistribution

from . import file
from pipm.operations import get_frozen_reqs, get_distributions


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

    def _save_requirements(self, env):
        """
            save installed requirements to file
        Args:
            env: one of div/test/custom or empty
        """
        file.save(env)

    def parse_args(self, args):
        """
            when no argument given it fills with `-r requirements.txt` as default
        Args:
            args (list):

        Returns:
            options, list:
        """

        options, args = super(InstallCommandPlus, self).parse_args(args)
        env = options.req_environment
        if not options.requirements and not args:
            options, args = super(InstallCommandPlus, self).parse_args(['-r', file.get_req_filename(env)])
            options.req_environment = env

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
        result = super(InstallCommandPlus, self).run(options, args)

        if not options.requirements:
            self._save_requirements(options.req_environment, )

        return result


class UninstallCommandPlus(UninstallCommand):
    """
        a drop-in replacement of pip's uninstall command. It removes the entry from requirements file after a package
        is removed.
    """

    def run(self, options, args):
        orig_args = args[:]
        dists = get_distributions()
        removed_packages = []
        for pkg in orig_args:  # type: str
            removed_packages.append(dists.pop(pkg.lower()))

        orphaned_pkgs = set()
        for dist in removed_packages:  # type: DistInfoDistribution
            for r in dist.requires():
                orphaned_pkgs.add(r.name)

        all_requires = set()
        for dist in dists:
            for r in dists[dist].requires():
                all_requires.add(r.name)

        removable_pkgs = orphaned_pkgs.difference(all_requires)
        if removable_pkgs:
            print('Following packages are auto-installed and no longer required: \n', '\n'.join(removable_pkgs))
            super(UninstallCommandPlus, self).run(options, ((args or []) + list(removable_pkgs)))

        file.save()


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
