from pipm import setup_cfg


def test_add_requirements_with_existing_config(config, requirement_set_factory):
    config = setup_cfg.add_requirements(user_reqs=requirement_set_factory("py==1.0.0"))
    assert config.get('options', 'install_requires') == "\npy==1.0.0\nsix~=1.11.0"
    assert config.get('options.extras_require', 'dev') == "\npytest~=3.7.2"


def test_add_requirements_dev_with_existing_config(config, requirement_set_factory):
    config = setup_cfg.add_requirements(user_reqs=requirement_set_factory("py==1.0.0"), env="dev")
    assert config.get('options', 'install_requires') == "\nsix~=1.11.0"
    assert config.get('options.extras_require', 'dev', ) == "\npy==1.0.0\npytest~=3.7.2"


def test_add_requirements_no_config_file(chdir, requirement_set_factory):
    config = setup_cfg.add_requirements(user_reqs=requirement_set_factory("six~=1.1.0", "py==1.0.0", ))
    assert config.get('options', 'install_requires') == "\npy==1.0.0\nsix~=1.1.0"


def test_add_dev_requirements_no_config_file(chdir, requirement_set_factory):
    config = setup_cfg.add_requirements(user_reqs=requirement_set_factory("pytest~=3.7.2", "py==1.0.0"), env="dev")
    assert config.get('options.extras_require', 'dev', ) == "\npy==1.0.0\npytest~=3.7.2"


def test_remove_requirements(config):
    config = setup_cfg.remove_requirements({"six"})

    assert config.get('options', 'install_requires') == "\nsix~=1.11.0"
    assert config.get('options.extras_require', 'dev', ) == ""
