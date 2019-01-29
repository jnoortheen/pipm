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


def _getdists(remove_count=0):
    """uses picle to get the frozen result packages"""
    with open(os.path.join(os.path.dirname(__file__), 'data', 'pkgs.proto2.pickle'), 'rb') as f:
        dists = pickle.loads(f.read())  # type: dict
        assert len(dists) == 23
        assert type(dists) == dict

        for d in dists:
            dists[d].requires = lambda: [Req('req_by_{}'.format(d)), Req('req_by_others'), ]
    if remove_count:
        cnt = 0
        for d in list(dists.keys()):
            cnt += 1
            dists.pop(d)
            if cnt >= remove_count:
                break
    return dists


@pytest.fixture
def patch_dists(mocker):
    def _patch_dist(remove=0):
        return mocker.patch.object(operations, 'get_distributions', return_value=_getdists(remove).copy())

    return _patch_dist


@pytest.fixture
def patched_dists(patch_dists):
    return patch_dists()


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
