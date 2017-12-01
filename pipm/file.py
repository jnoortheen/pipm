from __future__ import absolute_import

import errno
import logging
import os
from collections import OrderedDict

from pip.download import PipSession, get_file_content
from pip.req import req_file
from pip.req.req_install import InstallRequirement

from . import operations

logger = logging.getLogger(__name__)


def _new_line(filename):
    """
        append `\n` to the end of the file if it doesn't exist
    Args:
        filename:
    """
    with open(filename, 'ab+') as f:
        # check for empty file
        f.seek(0)
        if f.read(1) == b'' and f.read() == b'':
            return
        try:
            f.seek(-1, os.SEEK_END)
            if f.read(1) != b'\n':
                f.write(b'\n')
        except OSError:
            pass


def get_env_reqfile(*paths, base_file_name=''):
    """
        from the list of paths return the one that exists. If it doesn't exists then create with appropriate
        starter line
    Args:
        env:
        base_file_name:
        *paths:

    Returns:
        str:
    """
    requirements_dir = os.path.join('requirements', '')
    for path in paths:
        if os.path.exists(path):
            if path == 'requirements.txt':
                base_path = os.path.join('requirements', 'base.txt')
                if os.path.exists(base_path):
                    return base_path
            return path

    # create file if it doesnt exist
    filename = paths[0]  # prefer the first pattern in the list

    # if requirements directory exists then prefer creating files inside that one
    if os.path.exists(os.path.join(os.curdir, 'requirements')):
        for path in paths:
            if requirements_dir in path:
                filename = path

    if os.path.dirname(filename) and not os.path.exists(os.path.dirname(filename)):
        try:
            os.makedirs(os.path.dirname(filename))
        except OSError as exc:  # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise

    if not os.path.exists(filename):
        with open(filename, 'wb') as f:
            if base_file_name:
                if filename != base_file_name:
                    f.write(
                        '-r {}'.format(
                            'base.txt' if requirements_dir in filename else base_file_name
                        ).encode('utf-8')
                    )

    return filename


def get_patterns(*envs):
    """

    Args:
        *envs:

    Returns:
        list:

    >>> get_patterns('dev', 'development')
    ['dev-requirements.txt', 'requirements/dev.txt', 'requirements-dev.txt', 'development-requirements.txt', 'requirements/development.txt', 'requirements-development.txt']
    >>> get_patterns('base')
    ['requirements.txt', 'requirements/base.txt']
    """
    patterns = []
    for env in envs:
        patterns.append('{}requirements.txt'.format('' if env == 'base' else env + '-'))
        patterns.append(os.path.join('requirements', '{}.txt'.format(env)))
        if env != 'base':
            patterns.append('requirements-{}.txt'.format(env))
    return patterns


def get_req_filename(env=''):
    """

    Args:
        dev:
        test:
        prod:
        env:

    Returns:
        str:
    """
    BASE_PTRN = ('base',)
    DEV_PTRN = ('dev', 'development',)
    TEST_PTRN = ('test',)
    PROD_PTRN = ('prod', 'production',)

    envs = DEV_PTRN if env == 'dev' else PROD_PTRN if env == 'prod' else TEST_PTRN if env == 'test' else (
        env,) if env else BASE_PTRN
    paths = get_patterns(*envs)

    fname = get_env_reqfile(*paths, base_file_name='' if not env else get_env_reqfile(*get_patterns(*BASE_PTRN)))
    _new_line(fname)
    return fname


def get_req_filenames():
    """return all requirement files in the current project that matches the standard requirements filename pattern"""
    filenames = set()

    # if requirements directory exists then add those
    req_dir = os.path.join(os.curdir, 'requirements')
    if os.path.exists(req_dir):
        for fn in os.listdir(req_dir):
            filename = os.path.join('requirements', fn)
            if os.path.isfile(filename):
                if filename.endswith('.txt'):
                    filenames.add(filename)
    else:
        # walk current directory
        for filename in os.listdir(os.curdir):
            if os.path.isfile(filename):
                if filename.endswith('requirements.txt'):
                    filenames.add(filename)
                elif filename.startswith('requirements-'):
                    filenames.add(filename)

    return filenames


def parse_comes_from(comes_from, env):
    """
        parse comesfrom if valid otherwise return the filename for the environment
    Args:
        comes_from ([str]):
        env (str):

    Returns:
        str, int: filename and line number
    """
    if comes_from:
        comes_from = comes_from.split()
        return comes_from[1], int(comes_from[3].strip(')'))
    filename = get_req_filename(env)
    return filename, None


def _uniq_resources(reqs):
    """

    Args:
        reqs (list[InstallRequirement]):

    Returns:
        OrderedDict:
    """
    uniq_reqs = OrderedDict()
    for req in reqs:
        if req.name in uniq_reqs:
            old_req = uniq_reqs[req.name]
            if not req.comes_from and old_req.comes_from:
                req.comes_from = old_req.comes_from
        uniq_reqs[req.name] = req
    return uniq_reqs


def _cluster_to_file_reqs(reqs, env):
    """

    Args:
        reqs (list):

    Returns:
        OrderedDict:
    """
    filereqs = OrderedDict()
    for req in reqs:  # type: InstallRequirement
        filename, line_num = parse_comes_from(req.comes_from, env)

        if filename not in filereqs:
            filereqs[filename] = []

        req.filename = filename
        req.line_num = line_num

        filereqs[filename].append(req)
    return filereqs


def save(env='', session=None):
    """
        save installed requirements which is missing in the requirements files
    """
    session = session or PipSession()
    reqs = []

    # create base file if it doesnt exists
    env_filename = get_req_filename(env)

    for file in get_req_filenames():
        reqs += list(req_file.parse_requirements(file, session=session))

    uniq_reqs = _uniq_resources(reqs)
    file_reqs = _cluster_to_file_reqs(uniq_reqs.values(), env)
    for filename in get_req_filenames():
        if not file_reqs.get(filename):
            file_reqs[filename] = []

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
        with open(filename, 'wb') as f:
            for line in lines:
                cnt = lines[line].strip()
                if cnt:
                    f.write((cnt + '\n').encode('utf-8'))
