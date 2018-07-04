import codecs
from pip._internal.req import InstallRequirement
from setuptools.config import read_configuration
from six.moves import configparser
import os

SETUP_FILE_NAME = 'setup.cfg'


def _get_existing_reqs(config_dict, base_key, key, reqs):
    reqs_to_write = []
    if config_dict:  # parsed config
        existing = []
        if base_key in config_dict and key in config_dict[base_key]:
            existing = config_dict[base_key][key]
        elif '.' in base_key and base_key not in config_dict:
            part1, part2 = base_key.split('.', 1)
            if key in config_dict[part1][part2]:
                existing = config_dict[part1][part2][key]
        for _req in existing:  # type: str
            if not any((i in _req for i in reqs)):
                reqs_to_write.append(_req)
    return reqs_to_write


def _set_config_key(config, config_dict, base_key, key, reqs):
    if base_key not in config:
        config.add_section(base_key)

    reqs_to_write = _get_existing_reqs(config_dict, base_key, key, reqs)
    reqs_to_write.extend(reqs.values())

    reqs_string = "".join(map(lambda x: "\n" + x, reqs_to_write))
    config[base_key][key] = reqs_string


def _write_to_setup_cfg(config, config_dict, reqs, env=None):
    """
    Args:
        config:
        reqs (dict):
        env (str):
    """
    if env:
        base_key = 'options.extras_require'
        key = 'testing' if 'test' in env else str(env)
    else:
        base_key = 'options'
        key = 'install_requires'
    _set_config_key(config, config_dict, base_key, key, reqs)


def write_to_setup_cfg(user_reqs, env=None):
    """
        create/update setup.cfg file
    Args:
        user_reqs (RequirementSet): list of user requirements
        file_obj: file object to write to
    """
    config = configparser.ConfigParser()
    config_dict = None
    if os.path.exists(SETUP_FILE_NAME):
        config.read(SETUP_FILE_NAME)
        config_dict = read_configuration(SETUP_FILE_NAME)

    with codecs.open(SETUP_FILE_NAME, 'w') as file_obj:
        reqs = {}
        for req in user_reqs.requirements.values():  # type: InstallRequirement
            if not req.comes_from:
                req_string = str(req.req)
                if not any((i in req_string for i in {'<', '>', '=', '~'})):
                    req_string = req.req.name + '~=' + str(req.installed_version)
                reqs[req.req.name] = req_string
        if reqs:
            _write_to_setup_cfg(config, config_dict, reqs, env)
            config.write(file_obj)
