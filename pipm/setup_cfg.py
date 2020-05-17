import codecs
import os

try:
    from typing import Dict, Iterable, Set, List
except ImportError:
    pass

from pip._internal.req import InstallRequirement
from pip._vendor.packaging.requirements import Requirement
from pip._vendor.packaging.specifiers import SpecifierSet
from six.moves.configparser import ConfigParser

from . import operations

SETUP_FILE_NAME = "setup.cfg"


def _req_list_to_str(reqs):
    # type: (Iterable) -> str
    return "".join(map(lambda x: "\n" + x, sorted(reqs, key=lambda x: x.lower())))


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
    # type: (ConfigParser, str, str) -> Dict[str, str]
    reqs = (
        config.get(base_key, key)
        if config.has_section(base_key) and config.has_option(base_key, key)
        else ""
    )
    return dict(map(lambda x: (Requirement(x).name, x), _req_str_to_list(reqs)))


def update_config(config, env, new_reqs):
    """
        updates config
    Args:
        config (ConfigParser): parsed config file
        base_key (str): i.e. options, options.extra_requires
        key (str):
        new_reqs (Dict[str, str]): a dict of newly installed/updated requirements.
                                Key is the package name and value is the full name with version and markers
    """
    base_key, key = get_keys(env)

    if not config.has_section(base_key):
        config.add_section(base_key)

    reqs = _req_str_to_dict(config, base_key, key)
    reqs.update(new_reqs)
    if reqs:
        config.set(base_key, key, _req_list_to_str(reqs.values()))


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
    config = ConfigParser()
    if os.path.exists(SETUP_FILE_NAME):
        config.read(SETUP_FILE_NAME)
    return config


def _write_to_file(config):
    with codecs.open(SETUP_FILE_NAME, "w") as file_obj:
        config.write(file_obj)


def get_requirements(env=None):
    # (str) -> dict
    config = _read_config()
    base_key, key = get_keys(env)
    return _req_str_to_dict(config, base_key, key)


def add_requirements(user_reqs, env=None):
    # type: (List[InstallRequirement], str) -> ConfigParser
    """
        create/update setup.cfg file
    Args:
        user_reqs: list of user requirements
        file_obj: file object to write to
    """
    config = _read_config()

    reqs = {}
    for req in user_reqs:  # type: InstallRequirement
        if not req.comes_from:  # add only top-level dependencies
            if not req.req.specifier and req.installed_version:
                req.req.specifier = SpecifierSet("~=" + str(req.installed_version))
            reqs[req.req.name] = str(req.req)
    if reqs:
        update_config(config, env, reqs)
    _write_to_file(config)
    return config


def _remove_requirements(config, base_key, key, installed_reqs):
    # (ConfigParser, str, str, Set[str]) -> None
    # check all the sections and remove requirements that are not in the
    reqs = _req_str_to_dict(config, base_key, key)
    filtered = (req for req_name, req in reqs.items() if req_name in installed_reqs)
    config.set(base_key, key, _req_list_to_str(filtered))


def remove_requirements(installed_reqs=None):
    # type: (Set[str]) -> ConfigParser
    """
        remove requirements from `setup.cfg` after `pip uninstall`
    Args:
        installed_reqs (set): set of requirements name strings
    """
    installed_reqs = installed_reqs or set(operations.get_frozen_reqs().keys())
    config = _read_config()

    # check all the sections and remove requirements that are not in the
    for name in config.sections():
        if name == "options":
            section, option = get_keys()
            _remove_requirements(config, section, option, installed_reqs)
        elif name == "options.extras_require":
            for key in config.options(name):
                _remove_requirements(config, name, key, installed_reqs)
    _write_to_file(config)

    return config
