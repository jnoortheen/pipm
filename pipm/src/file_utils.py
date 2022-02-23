import errno
import os


def _new_line(filename):
    """
        append `\n` to the end of the file if it doesn't exist
    Args:
        filename:
    """
    with open(filename, "ab+") as f:
        # check for empty file
        f.seek(0)
        if f.read(1) == b"" and f.read() == b"":
            return
        try:
            f.seek(-1, os.SEEK_END)
            if f.read(1) != b"\n":
                f.write(b"\n")
        except OSError:
            pass


def get_patterns(*envs):
    """

    Args:
        *envs:

    Returns:
        list:
    """
    patterns = []
    for env in envs:
        patterns.append("{}requirements.txt".format("" if env == "base" else env + "-"))
        patterns.append(os.path.join("requirements", "{}.txt".format(env)))
        if env != "base":
            patterns.append("requirements-{}.txt".format(env))
    return patterns


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
        return comes_from[1], int(comes_from[3].strip(")"))
    filename = get_req_filename(env)
    return filename, None


def get_req_filename(env=""):
    """

    Args:
        env:

    Returns:
        str:
    """
    BASE_PTRN = ("base",)
    DEV_PTRN = ("dev", "development")
    TEST_PTRN = ("test",)
    PROD_PTRN = ("prod", "production")

    envs = (
        DEV_PTRN
        if env == "dev"
        else PROD_PTRN
        if env == "prod"
        else TEST_PTRN
        if env == "test"
        else (env,)
        if env
        else BASE_PTRN
    )
    paths = get_patterns(*envs)

    fname = get_env_reqfile(
        *paths,
        base_file_name="" if not env else get_env_reqfile(*get_patterns(*BASE_PTRN))
    )
    _new_line(fname)
    return fname


def get_env_reqfile(*paths, **kw):
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
    base_file_name = kw.get("base_file_name", "")
    requirements_dir = os.path.join("requirements", "")
    for path in paths:
        if os.path.exists(path):
            if path == "requirements.txt":
                base_path = os.path.join("requirements", "base.txt")
                if os.path.exists(base_path):
                    return base_path
            return path

    # create file if it doesnt exist
    filename = paths[0]  # prefer the first pattern in the list

    # if requirements directory exists then prefer creating files inside that one
    if os.path.exists(os.path.join(os.curdir, "requirements")):
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
        with open(filename, "wb") as f:
            if base_file_name:
                if filename != base_file_name:
                    f.write(
                        "-r {}".format(
                            "base.txt"
                            if requirements_dir in filename
                            else base_file_name
                        ).encode("utf-8")
                    )

    return filename
