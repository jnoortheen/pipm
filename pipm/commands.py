from __future__ import absolute_import
from pkg_resources._vendor.packaging.specifiers import SpecifierSet
from pip.req import InstallRequirement
from pip.commands import InstallCommand, UninstallCommand
import pip
from . import file


def store_req_environment(option, opt_str, value, parser, *args, **kwargs):
    parser.values.req_environment = opt_str.strip('-')


class InstallCommandPlus(InstallCommand):
    def __init__(self, *args, **kw):
        """

        Args:
            *args:
            **kw:

        >>> cmd = InstallCommandPlus()
        >>> opts, args = cmd.parse_args([ '--dev'])
        >>> opts.req_environment
        'dev'
        >>> opts, args = cmd.parse_args([ '--test'])
        >>> opts.req_environment
        'test'
        >>> opts, args = cmd.parse_args(['pkg_name', '--prod'])
        >>> opts.req_environment
        'prod'
        >>> opts, args = cmd.parse_args(['pkg_name', '--env', 'staging'])
        >>> opts.req_environment
        'staging'
        >>> opts, args = cmd.parse_args([])
        >>> opts.req_environment
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

    def _save_requirements(self, env, *reqs):
        """
            save installed requirements to file
        Args:
            env: one of div/test/custom or empty
            *reqs (tuple(InstallRequirement)):
        """
        for installrequirement in reqs:  # type: InstallRequirement
            if not installrequirement.req.specifier:
                if installrequirement.specifier:
                    installrequirement.req.specifier = installrequirement.specifier
                elif installrequirement.installed_version:
                    installrequirement.req.specifier = SpecifierSet('==' + installrequirement.installed_version)
            if not installrequirement.req.extras and installrequirement.extras:
                installrequirement.req.extras = installrequirement.extras
            if not installrequirement.req.marker and installrequirement.markers:
                installrequirement.req.marker = installrequirement.markers
                # if not req.req.url and req.link:
                #     req.req.url = req.link if isinstance(req.link, str) else req.link.url
        file.save(reqs, env)
    def parse_args(self, args):
        """
            when no argument given it fills with `-r requirements.txt` as default
        Args:
            args (list):

        Returns:
            options, list:
        """
        if not args:
            args = ['-r', file.get_req_filename(), ]
        return super(InstallCommandPlus, self).parse_args(args)

    def run(self, options, args):
        """
            wrapper around pip.commands.InstallCommand
        Args:
            options:
            args:

        Returns:
            pip.req.RequirementSet:
        """

        reqs = super(InstallCommandPlus, self).run(options, args)

        # consider appending to requirements.txt only when
        if not options.requirements and reqs:
            self._save_requirements(options.req_environment, *reqs.successfully_installed, )

        return reqs
