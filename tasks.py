from invoke import task, Context, Result


@task
def release(ctx, upload=False):
    """
        create new tag and push to git and PyPI
    Args:
        ctx (Context):
    """
    notes = ctx.run(
        'git log $(git describe --tags --abbrev=0)..HEAD --pretty=format:"%h %s"',
        hide=True
    )  # type: Result
    from pipm import __version__
    ctx.run('git tag -a {0} -m "{1}"'.format(__version__, notes.stdout))
    ctx.run("git push --follow-tags")

    # dont forget to have this file
    # ~/.pypirc
    # [distutils]
    # index-servers =
    #  pypi
    if upload:
        ctx.run("python setup.py sdist upload")


@task
def test(ctx):
    ctx.run("pytest --cov=pipm --cov-report term-missing tests/")
