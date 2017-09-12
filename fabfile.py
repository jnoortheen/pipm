from fabric.api import task
from fabric.operations import local

import pipm


@task
def release():
    local('git tag {}'.format(pipm.__version__))
    local('git push')
    local('git push --tags')


@task
def test():
    local('pytest --cov=pipm tests/')
