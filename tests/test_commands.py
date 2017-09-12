from pipm import InstallCommandPlus
from pipm.file import get_req_filename
from pip.req.req_install import InstallRequirement


def test_fill_args_when_no_args_given(chdir):
    """

    Args:
        tmpdir (LocalPath): fixture

    """
    f = get_req_filename()
    cmd = InstallCommandPlus()
    opts, args = cmd.parse_args([])
    assert opts.requirements == [f, ]


def test_fill_args_when_no_args_given_dev(chdir):
    """

    Args:
        tmpdir (LocalPath): fixture

    """
    for env in ['dev', 'test', 'prod']:
        f = get_req_filename(env)
        cmd = InstallCommandPlus()
        opts, args = cmd.parse_args(['--{}'.format(env)])
        assert opts.requirements == [f, ]


def test_fill_args_when_no_args_given_environ(chdir):
    """

    Args:
        tmpdir (LocalPath): fixture

    """
    env = 'staging'
    f = get_req_filename(env)
    cmd = InstallCommandPlus()
    opts, args = cmd.parse_args(['--env', env])
    assert opts.requirements == [f, ]


def test_req_environment():
    cmd = InstallCommandPlus()
    opts, args = cmd.parse_args(['--dev'])
    assert opts.req_environment == 'dev'
    opts, args = cmd.parse_args(['--test'])
    assert opts.req_environment == 'test'
    opts, args = cmd.parse_args(['pkg_name', '--prod'])
    assert opts.req_environment == 'prod'
    opts, args = cmd.parse_args(['pkg_name', '--env', 'staging'])
    assert opts.req_environment == 'staging'
    opts, args = cmd.parse_args([])
    assert opts.req_environment is None
