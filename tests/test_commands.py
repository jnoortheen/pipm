from mock import MagicMock

from pipm import commands
from pipm.file import get_req_filenames
from pipm.file_utils import get_req_filename


def test_fill_args_when_no_args_given(chdir):
    """

    Args:
        tmpdir (LocalPath): fixture

    """
    f = get_req_filename()
    cmd = commands.InstallCommandPlus("i", "i")
    opts, args = cmd.parse_args([])
    assert opts.requirements == [f]


def test_fill_args_when_no_args_given_dev(chdir):
    """

    Args:
        tmpdir (LocalPath): fixture

    """
    for env in ["dev", "test", "prod"]:
        f = get_req_filename(env)
        cmd = commands.InstallCommandPlus("i", "i")
        opts, args = cmd.parse_args(["--{}".format(env)])
        assert opts.requirements == [f]


def test_fill_args_when_no_args_given_all(chdir):
    """

    Args:
        tmpdir (LocalPath): fixture

    """
    # create the below two files
    get_req_filename("dev")
    get_req_filename("test")

    # start test
    fset = get_req_filenames()
    cmd = commands.InstallCommandPlus("i", "i")
    opts, args = cmd.parse_args(["--all"])
    assert set(opts.requirements) == fset


def test_fill_args_when_no_args_given_environ(chdir):
    """

    Args:
        tmpdir (LocalPath): fixture

    """
    env = "staging"
    f = get_req_filename(env)
    cmd = commands.InstallCommandPlus("i", "i")
    opts, args = cmd.parse_args(["--env", env])
    assert opts.requirements == [f]


def test_req_environment():
    cmd = commands.InstallCommandPlus("i", "i")
    opts, args = cmd.parse_args(["--dev"])
    assert opts.req_environment == "dev"
    opts, args = cmd.parse_args(["--test"])
    assert opts.req_environment == "test"
    opts, args = cmd.parse_args(["pkg_name", "--prod"])
    assert opts.req_environment == "prod"
    opts, args = cmd.parse_args(["pkg_name", "--env", "staging"])
    assert opts.req_environment == "staging"
    opts, args = cmd.parse_args([])
    assert opts.req_environment is None


def test_update_command_parse_args():
    cmd = commands.UpdateCommand("u", "u")
    opts, args = cmd.parse_args([])
    assert opts.upgrade


def test_install_cmd_run(mocker):
    """
    """
    run = mocker.patch.object(commands.install.InstallCommand, "run")  # type: MagicMock
    save = mocker.patch.object(commands.file, "save")  # type: MagicMock

    # run method
    cmd = commands.InstallCommandPlus("i", "i")
    cmd.main(["--dev", "pkg"])

    run.assert_called_once()
    save.assert_called_once()


def test_remove_cmd_run(mocker):
    run = mocker.patch.object(commands.UninstallCommand, "run")  # type: MagicMock
    save = mocker.patch.object(commands.file, "save")  # type: MagicMock
    mocker.patch.object(
        commands, "get_orphaned_packages", return_value=["pkg1", "pkg2"]
    )  # type: MagicMock

    # run method
    cmd = commands.UninstallCommandPlus("u", "u")
    opts, args = cmd.parse_args(["dev"])
    cmd.run(opts, args)

    run.assert_called_once_with(opts, ["dev", "pkg1", "pkg2"])
    save.assert_called_once()


def test_freeze_cmd_run(mocker):
    run = mocker.patch.object(commands.FreezeCommand, "run")  # type: MagicMock
    save = mocker.patch.object(commands.file, "save")  # type: MagicMock
    mocker.patch.object(
        commands, "get_orphaned_packages", return_value=["pkg1", "pkg2"]
    )  # type: MagicMock

    # run method
    cmd = commands.FreezeCommandPlus("f", "f")
    opts, args = cmd.parse_args([])
    cmd.run(opts, args)

    run.assert_called_once()
    save.assert_called_once()
