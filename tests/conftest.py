import os
from collections import namedtuple, OrderedDict
from distutils.dir_util import copy_tree

import pytest

# patch sys.path
import pipm  # noqa
import sys

print(f"path: {sys.path} debug")

from pip._internal.metadata.pkg_resources import Distribution

from pipm.src import operations


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


def distribution_factory(proj, mocker, parent: "Distribution | None" = None):
    def new_dist():
        from pip._vendor.pkg_resources import Distribution as PD

        dist = PD(
            project_name=proj,
            location=".venv/lib/python/{}".format(proj),
            version="1.0.0",
        )
        if parent is not None:
            mocker.patch.object(
                parent._dist,
                "requires",
                return_value=[dist.as_requirement()],
            )
        return dist

    return Distribution(new_dist())


@pytest.fixture
def patch_dists(mocker):
    def _patch_dist(cnt=10):
        dists = OrderedDict()

        # update requires method
        prev_dist = None
        for i in range(cnt):
            proj = "proj-{}".format(i)
            dists[proj] = prev_dist = distribution_factory(proj, mocker, prev_dist)

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
    from pipm.src import setup_cfg

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
