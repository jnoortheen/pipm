import os
import pickle
from collections import namedtuple
from typing import List

import pytest

from pipm import operations


@pytest.fixture
def chdir(tmpdir_factory):
    tmpdir = tmpdir_factory.mktemp("test")
    os.chdir(tmpdir.strpath)
    return tmpdir


Req = namedtuple("Req", ["name"])

DIST_DATA = os.path.join(os.path.dirname(__file__), "data", "pkgs.proto2.pickle")
DIST_PKG_COUNT = 37


def _getdists(remove_count=0):
    """uses picle to get the frozen result packages"""
    with open(DIST_DATA, "rb") as f:
        dists = pickle.loads(f.read())  # type: dict
        assert len(dists) == DIST_PKG_COUNT
        assert type(dists) == dict

    for cnt, d in enumerate(list(dists.keys())):
        if cnt >= remove_count:
            break
        dists.pop(d)
    return dists


@pytest.fixture
def patch_dists(mocker):
    def _patch_dist(remove=0):
        m = mocker.patch.object(
            operations, "get_distributions", return_value=_getdists(remove).copy()
        )
        m.cnt = DIST_PKG_COUNT
        return m

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
