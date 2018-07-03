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


def getdists(remove_count=None, **args):
    with open(os.path.join(os.path.dirname(__file__), 'data', 'pkgs.pickle'), 'rb') as f:
        dists = pickle.loads(f.read())  # type: dict
        assert len(dists) == 23
        assert type(dists) == dict

        if remove_count:
            cnt = 0
            for d in list(dists.keys()):
                cnt += 1
                dists.pop(d)
                if cnt >= remove_count:
                    break

    def dist_requires(d):
        return [Req('req_by_{}'.format(d)), Req('req_by_others'), ]

    for d in dists:
        dists[d].requires = functools.partial(dist_requires, d)

    return dists


@pytest.fixture
def patch_dists(monkeypatch):
    monkeypatch.setattr(operations, 'get_distributions', getdists)

    return monkeypatch
