import codecs
import os
from pip._internal.req import InstallRequirement
from pip._vendor.packaging.requirements import Requirement
from pip._vendor.packaging.specifiers import SpecifierSet
from six.moves import configparser
from typing import Dict, Iterable, Set

SETUP_FILE_NAME = "setup.cfg"


def _req_list_to_str(reqs):
    # type: (Iterable) -> str
    return "".join(map(lambda x: "\n" + x, reqs))


def _req_str_to_list(reqs):
    # type: (str) -> list
    if reqs and isinstance(reqs, str):
        reqs = reqs.strip()
        if "\n" in reqs:
            return reqs.splitlines()
        elif "," in reqs:
            return reqs.split(",")
        else:
            return [reqs]
    return []


def _req_str_to_dict(config, base_key, key):
    # type: (configparser.ConfigParser, str, str) -> Dict[str, str]
    reqs = config.get(base_key, key, fallback="")
    return dict(map(lambda x: (Requirement(x).name, x), _req_str_to_list(reqs)))


def update_config(config, base_key, key, new_reqs):
    """
        updates config
    Args:
        config (configparser.ConfigParser): parsed config file
        base_key (str): i.e. options, options.extra_requires
        key (str):
        new_reqs (Dict[str, str]): a dict of newly installed/updated requirements.
                                Key is the package name and value is the full name with version and markers
    """
    if base_key not in config:
        config.add_section(base_key)

    reqs = _req_str_to_dict(config, base_key, key)
    reqs.update(new_reqs)
    if reqs:
        config[base_key][key] = _req_list_to_str(reqs.values())


def get_keys(env=None):
    """return key combination for adding new RequirementSet"""
    if env:
        base_key = "options.extras_require"
        key = "testing" if env and "test" in env else str(env)
    else:
        base_key = "options"
        key = "install_requires"
    return base_key, key


def _read_config():
    """read from existing file"""
    config = configparser.ConfigParser()
    if os.path.exists(SETUP_FILE_NAME):
        config.read(SETUP_FILE_NAME)
    return config


def _write_to_file(config):
    with codecs.open(SETUP_FILE_NAME, "w") as file_obj:
        config.write(file_obj)


def add_requirements(user_reqs, env=None):
    """
        create/update setup.cfg file
    Args:
        user_reqs (RequirementSet): list of user requirements
        file_obj: file object to write to
    """
    config = _read_config()

    reqs = {}
    for req in user_reqs.requirements.values():  # type: InstallRequirement
        if not req.comes_from:  # add only top-level dependencies
            if not req.req.specifier:
                req.req.specifier = SpecifierSet("~=" + str(req.installed_version))
            reqs[req.req.name] = str(req.req)
    if reqs:
        base_key, key = get_keys(env)
        update_config(config, base_key, key, reqs)
    _write_to_file(config)
    return config


def _remove_requirements(config, base_key, key, installed_reqs):
    # (ConfigParser, str, str, Set[str]) -> None
    # check all the sections and remove requirements that are not in the
    reqs = _req_str_to_dict(config, base_key, key)
    filtered = (req for req_name, req in reqs.items() if req_name in installed_reqs)
    config[base_key][key] = _req_list_to_str(filtered)


def remove_requirements(installed_reqs):
    # type: (Set[str]) -> configparser.ConfigParser
    """
        remove requirements from `setup.cfg` after `pip uninstall`
    Args:
        installed_reqs (set): set of requirements name strings
    """
    config = _read_config()

    # check all the sections and remove requirements that are not in the
    _remove_requirements(config, "options", "install_requires", installed_reqs)
    for name, section in config.items():
        if "options.extras_require" == name:
            for key in section.keys():
                _remove_requirements(config, name, key, installed_reqs)
    _write_to_file(config)

    return config
