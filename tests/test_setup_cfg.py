from pipm.src import setup_cfg
from pytest import fixture


@fixture
def req_set_py(pkg_ir_py):
    return [pkg_ir_py]


@fixture
def req_set_py_six(pkg_ir_py, pkg_ir_six):
    return [pkg_ir_py, pkg_ir_six]


def test_add_requirements_with_existing_config(config, req_set_py):
    config = setup_cfg.add_requirements(user_reqs=req_set_py)
    assert config.get("options", "install_requires") == "\npy==1.0.0\nsix~=1.11.0"
    assert config.get("options.extras_require", "dev") == "\npytest~=3.7.2"


def test_add_requirements_dev_with_existing_config(config, req_set_py):
    config = setup_cfg.add_requirements(user_reqs=req_set_py, env="dev")
    assert config.get("options", "install_requires") == "\nsix~=1.11.0"
    assert config.get("options.extras_require", "dev") == "\npy==1.0.0\npytest~=3.7.2"


def test_add_requirements_no_config_file(chdir, req_set_py_six):
    config = setup_cfg.add_requirements(user_reqs=req_set_py_six)
    assert config.get("options", "install_requires") == "\npy==1.0.0\nsix~=1.11.0"


def test_add_dev_requirements_no_config_file(chdir, req_set_py_six):
    config = setup_cfg.add_requirements(user_reqs=req_set_py_six, env="dev")
    assert config.get("options.extras_require", "dev") == "\npy==1.0.0\nsix~=1.11.0"


def test_remove_requirements(config):
    config = setup_cfg.remove_requirements({"six"})

    assert config.get("options", "install_requires") == "\nsix~=1.11.0"
    assert config.get("options.extras_require", "dev") == ""
