import os

import errno
from collections import OrderedDict

from pip import FrozenRequirement
from pip.download import PipSession, get_file_content
from pip.req import req_file
from pip.req.req_install import InstallRequirement


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
            f.seek(-2, os.SEEK_END)
            if f.read(1) != b'\n':
                f.write(b'\n')
        except OSError:
            f.seek(0)
            ls = f.readlines()
            if ls:
                last_line = ls[-1]
                if b'\n' not in last_line:
                    f.seek(0, os.SEEK_END)
                    f.write(b'\n')


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
    for path in paths:
        if os.path.exists(path):
            return path

    # create file if it doesnt exist
    filename = paths[0]
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
                    f.write('-r {}'.format('base.txt' if 'base' in base_file_name else base_file_name).encode('utf-8'))

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


def parse(env=''):
    """
        parse requirements file. This retains comments from the file and the exact content of them. So that they can
        be written back without much distortion in the content.
    Args:
        env:

    Returns:

    """
    return list(req_file.parse_requirements(get_req_filename(env), session=PipSession()))


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
        reqs list[InstallRequirement]:

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
        reqs (OrderedDict):

    Returns:
        OrderedDict:
    """
    filereqs = OrderedDict()
    for req_name in reqs:
        req = reqs[req_name]  # type: InstallRequirement
        filename, line_num = parse_comes_from(req.comes_from, env)

        if filename not in filereqs:
            filereqs[filename] = OrderedDict()

        req.filename = filename
        req.line_num = line_num

        filereqs[filename][req_name] = req
    return filereqs


def save(reqs, env=''):
    """
    save requirements to the files while retain the original as much as possible including comments, etc.,
    """
    uniq_reqs = _uniq_resources(reqs)
    file_reqs = _cluster_to_file_reqs(uniq_reqs, env)
    # first step process the requirements and split them into separate for each of the file
    for filename in file_reqs:  # type: str
        _, content = get_file_content(
            filename, session=PipSession()
        )
        lines_enum = enumerate(content.splitlines(), start=1)
        lines_enum = req_file.join_lines(lines_enum)
        lines = OrderedDict(lines_enum)
        filename = get_req_filename(env)
        for req_name in file_reqs[filename]:
            req = file_reqs[filename][req_name]
            try:
                frozenrequirement = FrozenRequirement.from_dist(req.get_dist(), [])
            except Exception:
                frozenrequirement = FrozenRequirement(req.name, req.req, req.editable)

            _line_num = req.line_num if req.line_num and req.line_num in lines else max(lines.keys()) + 1
            lines[_line_num] = str(frozenrequirement).strip()

        with open(filename, 'wb') as f:
            f.write("\n".join(lines.values()).encode('utf-8'))
