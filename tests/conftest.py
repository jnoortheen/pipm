import os
import pytest


@pytest.fixture(scope='session')
def chdir(tmpdir_factory):
    tmpdir = tmpdir_factory.mktemp('test')
    os.chdir(tmpdir.strpath)
    return tmpdir
