import os
from collections import namedtuple
from distutils.dir_util import copy_tree
from typing import List

import pytest
from pip._vendor.pkg_resources import Distribution

from pipm import operations


@pytest.fixture
def chdir(tmpdir_factory):
    tmpdir = tmpdir_factory.mktemp("test")
    os.chdir(tmpdir.strpath)
    return tmpdir


DIRNAME = os.path.dirname(__file__)
DATA_DIR = os.path.join(DIRNAME, "data")
DIST_PKG_COUNT = 10


@pytest.fixture
def data_dir(chdir):
    copy_tree(DATA_DIR, str(chdir))


Req = namedtuple("Req", ["name"])


def distribution_factory(proj):
    return Distribution(
        project_name=proj, location=".venv/lib/python/{}".format(proj), version="1.0.0"
    )


@pytest.fixture
def patch_dists(mocker):
    def _patch_dist(remove=0):
        dists = {}
        cnt = DIST_PKG_COUNT - remove
        for i in range(cnt):
            proj = "proj-{}".format(i)
            dists[proj] = distribution_factory(proj)  # type: Distribution

        # update requires method
        prev_dist = None
        for name, dist in dists.items():
            if prev_dist is None:
                prev_dist = dist
            else:
                mocker.patch.object(
                    prev_dist, "requires", return_value=[dist.as_requirement()]
                )
                prev_dist = dist
        m = mocker.patch.object(operations, "get_distributions", return_value=dists)
        m.cnt = cnt
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
def install_requirement_factory():
    def _factory(r):
        from pip._internal.req.constructors import install_req_from_line

        req = install_req_from_line(r)
        req.is_direct = True
        return req

    return _factory


@pytest.fixture
def pkg_ir_py(install_requirement_factory):
    return install_requirement_factory("py==1.0.0")


@pytest.fixture
def pkg_ir_six(install_requirement_factory):
    return install_requirement_factory("six~=1.11.0")


@pytest.fixture
def requirement_set_factory(install_requirement_factory):
    def _factory(*reqs):
        # type: (List[str]) -> 'RequirementSet'
        from pipm.file import RequirementSet

        req_set = RequirementSet()

        for r in reqs:
            req_set.add_requirement(
                install_requirement_factory(r) if isinstance(r, str) else r
            )
        return req_set

    return _factory
