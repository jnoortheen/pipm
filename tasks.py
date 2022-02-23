import glob
import shutil

from invoke import task, Context, Result


@task
def pkg_release(c):
    c.run("rm dist/*")
    c.run("python setup.py sdist bdist_wheel")
    c.run("twine upload dist/* --skip-existing --verbose")


@task
def release(c, upload=False):
    """
        create new tag and push to git and PyPI
    Args:
        c (Context):
    """
    notes = c.run(
        'git log $(git describe --tags --abbrev=0)..HEAD --pretty=format:"%h %s"',
        hide=True,
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
        pkg_release(c)


@task
def test(c):
    c.run("pytest --cov=pipm --cov-report term-missing tests/")


@task
def vendor(c):
    target = "pipm/_vendor"
    c.run(f"pip install pip --target={target} --upgrade")
    shutil.rmtree(f"{target}/bin", ignore_errors=True)

    dist = glob.glob(f"{target}/*.dist-info")
    if dist:
        shutil.rmtree(dist[0], ignore_errors=True)
