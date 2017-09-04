import os


def append_last_line(filename):
    """
        create an empty line if one doesn't exist
    Args:
        filename:
    """
    with open(filename, 'ab+') as f:
        # check first byte. if it is empty then it may be an empty file
        if f.read(1) == b'' and f.read() == b'':
            return
        f.seek(-2, os.SEEK_END)
        if f.read(1) == b'\n':
            return
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
        open(filename, 'w').close()

    return filename


def get_patterns(*envs):
    """

    Args:
        *envs:

    Returns:
        list:

    >>> get_patterns('dev', 'development')
    ['dev-requirements.txt', 'requirements/dev.txt', 'development-requirements.txt', 'requirements/development.txt']
    >>> get_patterns('base')
    ['requirements.txt', 'requirements/base.txt']
    """
    patterns = []
    for env in envs:
        patterns.append('{}requirements.txt'.format('' if env == 'base' else env + '-'))
        patterns.append(os.path.join('requirements', '{}.txt'.format(env)))
    return patterns


def get_requirements_filename(dev=False, test=False, prod=False, env=''):
    """

    Args:
        dev:
        test:
        prod:
        env:

    Returns:
        str:
    >>> get_requirements_filename(dev=True)
    'dev-requirements.txt'
    >>> get_requirements_filename()
    'requirements.txt'
    """

    envs = ('dev', 'development',) if dev else ('prod', 'production',) if prod else ('test',) if test else (
        env,) if env else ('base',)
    paths = get_patterns(*envs)
    return get_env_requirement_file(*paths)
