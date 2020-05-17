import os
from collections import namedtuple
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
DIST_DATA = os.path.join(DIRNAME, "data")
DIST_PKG_COUNT = 10


@pytest.fixture
def data_dir():
    dirname = os.path.abspath(os.curdir)
    os.chdir(DIST_DATA)
    yield
    os.chdir(dirname)


Req = namedtuple("Req", ["name"])


def distribution_factory(proj):
    return Distribution(
        project_name=proj, location=".venv/lib/python/{}".format(proj), version="1.0.0"
    )


@pytest.fixture
def patch_dists(mocker):
    def _patch_dist(remove=0):
        dists = {}
        for i in range(DIST_PKG_COUNT - remove):
            proj = "proj-{}".format(i)
            dists[proj] = distribution_factory(proj)

        m = mocker.patch.object(operations, "get_distributions", return_value=dists)
        m.cnt = len(dists)
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
def requirement_set_factory(install_requirement_factory):
    def _factory(*reqs):
        # type: (List[str]) -> 'RequirementSet'
        from pipm.file import RequirementSet

        req_set = RequirementSet()

        for r in reqs:
            req_set.add_requirement(install_requirement_factory(r))
        return req_set

    return _factory
