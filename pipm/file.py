from __future__ import absolute_import, unicode_literals

import logging
import os
from collections import OrderedDict

from pip._internal.network.session import PipSession
from pip._internal.req import req_file, RequirementSet
from pip._internal.req.req_file import get_file_content, ParsedRequirement
from pip._internal.req.req_install import InstallRequirement

from . import operations, setup_cfg
from .classes import OrderedDefaultDict, FileRequirement
from .file_utils import get_req_filename

try:
    from typing import List, Dict
except ImportError:
    pass

logger = logging.getLogger(__name__)


def get_req_filenames():
    """return all requirement files in the current project that matches the standard requirements filename pattern"""
    filenames = set()

    # if requirements directory exists then add those
    req_dir = os.path.join(os.curdir, "requirements")
    if os.path.exists(req_dir):
        for fn in os.listdir(req_dir):
            filename = os.path.join("requirements", fn)
            if os.path.isfile(filename):
                if filename.endswith(".txt"):
                    filenames.add(filename)
    else:
        # walk current directory
        for filename in os.listdir(os.curdir):
            if os.path.isfile(filename):
                if filename.endswith("requirements.txt"):
                    filenames.add(filename)
                elif filename.startswith("requirements-"):
                    filenames.add(filename)

    return filenames


def _uniq_resources(reqs):
    # type: (List[ParsedRequirement]) -> Dict[str, ParsedRequirement]
    uniq_reqs = OrderedDict()
    for req in reqs:  # type: ParsedRequirement
        if req.name in uniq_reqs:  # req.name = "xdis"
            old_req = uniq_reqs[req.name]
            if (
                not req.comes_from and old_req.comes_from
            ):  # req.comes_from = '-r requirements.txt (line 1)'
                req.comes_from = old_req.comes_from
        uniq_reqs[req.name] = req
    return uniq_reqs


def _cluster_to_file_reqs(reqs, env):
    # type: (List[ParsedRequirement], str) -> Dict[str, List[FileRequirement]]
    filereqs = OrderedDefaultDict(list)
    for req in reqs:  # type: InstallRequirement
        freq = FileRequirement(req, env)
        filereqs[freq.filename].append(freq)
    return filereqs


def get_parsed_requirements():
    # type: () -> (PipSession, Dict[str, ParsedRequirement])
    session = PipSession()
    reqs = []
    for file in get_req_filenames():
        reqs += list(req_file.parse_requirements(file, session=session))
    return session, _uniq_resources(reqs)


def save(env="", user_reqs=None, uninstall=False):
    """
        save installed requirements which is missing in the requirements files
    Args:
        env (str):
        user_reqs (RequirementSet): list of strings that are explicitly given as argument to the user installing
    """
    session, reqs = get_parsed_requirements()

    # create base file if it doesnt exists
    env_filename = get_req_filename(env)

    file_reqs = _cluster_to_file_reqs(list(reqs.values()), env)
    for filename in get_req_filenames():
        if not file_reqs.get(filename):
            file_reqs[filename] = []

    if user_reqs:
        setup_cfg.add_requirements(user_reqs, env)
    if uninstall:
        setup_cfg.remove_requirements()

    write_to_req_files(file_reqs, session, env_filename, reqs)


def write_to_req_files(file_reqs, session, env_filename, uniq_reqs):
    installations = operations.get_frozen_reqs()

    # first step process the requirements and split them into separate for each of the file
    for filename in file_reqs:  # type: str
        _, content = get_file_content(filename, session=session)

        orig_lines = enumerate(content.splitlines(), start=1)
        joined_lines = req_file.join_lines(orig_lines)
        lines = OrderedDict(joined_lines)

        # 1. save new requirements
        if filename == env_filename:
            installed = set(installations.keys()).difference(set(uniq_reqs.keys()))
            for new_req in installed:
                line_num = len(lines) + 1
                lines[line_num] = str(installations[new_req]).strip()

        for req in file_reqs[filename]:
            frozenrequirement = installations.get(req.name)
            if frozenrequirement:
                # 2. updates
                lines[req.line_num] = str(frozenrequirement).strip()
            else:
                # 3. removals
                lines.pop(req.line_num)

        # 4. finally write to file
        with open(filename, "wb") as f:
            for line in lines:
                cnt = lines[line].strip()
                if cnt:
                    f.write((cnt + "\n").encode("utf-8"))
