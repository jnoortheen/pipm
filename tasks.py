from invoke import task, Context, Result


@task
def release(c, upload=False):
    """
        create new tag and push to git and PyPI
    Args:
        c (Context):
    """
    notes = c.run(
        'git log $(git describe --tags --abbrev=0)..HEAD --pretty=format:"%h %s"',
        hide=True
    )  # type: Result
    from pipm import __version__
    c.run('git tag -a {0} -m "{1}"'.format(__version__, notes.stdout))
    c.run("git push --follow-tags")

    # dont forget to have this file
    # ~/.pypirc
    # [distutils]
    # index-servers =
    #  pypi
    if upload:
        c.run("python setup.py sdist upload")


@task
def test(c):
    c.run("pytest --cov=pipm --cov-report term-missing tests/")


@task
def generate_dist_stub(c):
    from pickle import Pickler
    from tests.conftest import DIST_DATA
    from pipm.operations import get_distributions
    with open(DIST_DATA, "wb") as f:
        Pickler(f, protocol=2).dump(get_distributions())
