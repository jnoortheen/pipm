import os

import posixpath

from datetime import datetime
from fabric.api import cd, env, run, sudo, task, get
from fabric.context_managers import settings
from fabric.contrib import django
from fabric.contrib.files import exists
from fabric.operations import local
import pipm


@task
def release():
    local('git tag {}'.format(pipm.__version__))
    local('git push')
    local('git push --tags')
