from invoke import task, Context

from pipm import __version__


@task
def release(ctx):
    """
        create new tag and push to git and PyPI
    Args:
        ctx (Context):
    """
    ctx.run('git push')
    ctx.run('git tag {}'.format(__version__.__version__))
    ctx.run('git push --tags')

    # dont forget to have this file
    # ~/.pypirc
    # [distutils]
    # index-servers =
    #  pypi

    # [pypi]
    # repository: https://upload.pypi.org/legacy/
    # username: jnoortheen
    # password: pwd
    ctx.run('python setup.py sdist upload')


@task
def test(ctx):
    ctx.run('pytest --cov=pipm --cov-report term-missing tests/')
