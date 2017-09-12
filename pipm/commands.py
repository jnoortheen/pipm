from __future__ import absolute_import
from pip.commands import InstallCommand, UninstallCommand
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
        if not options.requirements and not args:
            options.requirements = [file.get_req_filename(options.req_environment), ]
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
        super(UninstallCommandPlus, self).run(options, args)
        file.save()
