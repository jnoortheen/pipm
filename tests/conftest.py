import functools
import os
from collections import namedtuple

import pytest
from pipm import operations
import pickle


@pytest.fixture
def chdir(tmpdir_factory):
    tmpdir = tmpdir_factory.mktemp('test')
    os.chdir(tmpdir.strpath)
    return tmpdir


Req = namedtuple('Req', ['name'])


def dist_requires(d):
    return [Req('req_by_{}'.format(d)), Req('req_by_others'), ]


@pytest.fixture
def patch_dists(monkeypatch):
    with open(os.path.join(os.path.dirname(__file__), 'pkgs.pickle'), 'rb') as f:
        dists = pickle.loads(f.read())
    assert len(dists) == 23
    assert type(dists) == dict

    for d in dists:
        dists[d].requires = functools.partial(dist_requires, d)

    def getdists(**args):
        return dists

    monkeypatch.setattr(operations, 'get_distributions', getdists)

    return monkeypatch
