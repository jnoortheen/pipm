from invoke import task, Context


@task
def release(ctx, version):
    """
        create new tag and push to git and PyPI
    Args:
        ctx (Context):
    """
    ctx.run("git push")
    ctx.run("git tag {}".format(version))
    ctx.run("git push --tags")

    # dont forget to have this file
    # ~/.pypirc
    # [distutils]
    # index-servers =
    #  pypi

    # [pypi]
    # repository: https://upload.pypi.org/legacy/
    # username: jnoortheen
    # password: pwd
    # poetry config http-basic.pypi jnoortheen pwd
    ctx.run("poetry publish")


@task
def test(ctx):
    ctx.run("pytest --cov=pipm --cov-report term-missing tests/")
