import os
import pytest
from pipm import operations
import pickle


@pytest.fixture(scope='session')
def chdir(tmpdir_factory):
    tmpdir = tmpdir_factory.mktemp('test')
    os.chdir(tmpdir.strpath)
    return tmpdir


@pytest.fixture
def patch_dists(monkeypatch):
    with open(os.path.join(os.path.dirname(__file__), 'pkgs.pickle'), 'rb') as f:
        dists = pickle.loads(f.read())
    assert len(dists) == 23
    assert type(dists) == dict

    def getdists(**args):
        return dists

    monkeypatch.setattr(operations, 'get_distributions', getdists)

    return monkeypatch
