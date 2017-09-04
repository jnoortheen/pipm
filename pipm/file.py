import os

import errno


def append_last_line(filename):
    """
        create an empty line if one doesn't exist
    Args:
        filename:
    >>> f = get_requirements_filename('dev')
    >>> with open(f) as fl: fl.read()
    '-r requirements.txt'
    >>> os.remove(f)
    >>> os.remove('requirements.txt')
    """
    with open(filename, 'ab+') as f:
        # check first byte. if it is empty then it may be an empty file
        f.seek(-2, os.SEEK_END)
        if f.read(1) != b'\n':
            f.write(b'\n')


def get_env_requirement_file(*paths):
    """

    Args:
        *paths:

    Returns:

    >>> get_env_requirement_file('requirements/dev.txt')
    'requirements/dev.txt'
    >>> os.path.exists('requirements/dev.txt')
    True
    >>> os.remove('requirements/dev.txt')
    >>> os.rmdir('requirements')
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
        basename = get_requirements_filename()
        with open(filename, 'wb') as f:
            if filename != basename:
                f.write('-r {}'.format('base.txt' if 'base' in basename else basename).encode('utf-8'))

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


def get_requirements_filename(env=''):
    """

    Args:
        dev:
        test:
        prod:
        env:

    Returns:
        str:
    >>> f = get_requirements_filename('dev')
    >>> f
    'dev-requirements.txt'
    >>> os.remove(f)
    >>> f = get_requirements_filename()
    >>> f
    'requirements.txt'
    >>> os.remove(f)
    """

    envs = ('dev', 'development',) if env == 'dev' else ('prod', 'production',) if env == 'prod' else (
        'test',) if env == 'test' else (env,) if env else ('base',)
    paths = get_patterns(*envs)
    fname = get_env_requirement_file(*paths)
    # append_last_line(fname)
    return fname


def read_requirements(env=''):
    filename = get_requirements_filename(env)
    # with open(filename, 'rb+') as f:
    #     f.write((str(frozenrequirement).strip() + '\n').encode('utf-8'))
