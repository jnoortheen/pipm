from pipm import setup_cfg


def test_add_requirements_with_existing_config(config, requirement_set_factory):
    config = setup_cfg.add_requirements(user_reqs=requirement_set_factory("py==1.0.0"))
    assert config['options']['install_requires'] == "\nsix~=1.11.0\npy==1.0.0"
    assert config['options.extras_require']['dev'] == "\npytest~=3.7.2"


def test_add_requirements_dev_with_existing_config(config, requirement_set_factory):
    config = setup_cfg.add_requirements(user_reqs=requirement_set_factory("py==1.0.0"), env="dev")
    assert config['options']['install_requires'] == "\nsix~=1.11.0"
    assert config['options.extras_require']['dev'] == "\npytest~=3.7.2\npy==1.0.0"


def test_add_requirements_no_config_file(chdir, requirement_set_factory):
    config = setup_cfg.add_requirements(user_reqs=requirement_set_factory("py==1.0.0"), env="dev")
    assert config['options']['install_requires'] == "\nsix~=1.11.0"
    assert config['options.extras_require']['dev'] == "\npytest~=3.7.2\npy==1.0.0"


def test_remove_requirements(config):
    config = setup_cfg.remove_requirements({"six"})

    assert config['options']['install_requires'] == "\nsix~=1.11.0"
    assert config['options.extras_require']['dev'] == ""
