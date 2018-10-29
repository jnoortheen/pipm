from collections import namedtuple

import functools
import os
import pickle
import pytest
from typing import List

from pipm import operations


@pytest.fixture
def chdir(tmpdir_factory):
    tmpdir = tmpdir_factory.mktemp('test')
    os.chdir(tmpdir.strpath)
    return tmpdir


Req = namedtuple('Req', ['name'])


def getdists(remove_count=None, **args):
    """uses picle to get the frozen result packages"""
    with open(os.path.join(os.path.dirname(__file__), 'data', 'pkgs.proto2.pickle'), 'rb') as f:
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


@pytest.fixture
def config(chdir):
    setup_cfg_str = """\
[options]
install_requires = 
	six~=1.11.0

[options.extras_require]
dev = 
	pytest~=3.7.2
"""
    from pipm import setup_cfg
    with open(setup_cfg.SETUP_FILE_NAME, "w") as f:
        f.write(setup_cfg_str)


@pytest.fixture
def requirement_set_factory():
    def _factory(*reqs):
        # type: (List[str]) -> 'RequirementSet'
        from pipm.file import RequirementSet
        from pip._internal.req.constructors import install_req_from_line
        req_set = RequirementSet()

        for r in reqs:
            req = install_req_from_line(r)
            req.is_direct = True
            req_set.add_requirement(req)
        return req_set

    return _factory
