from pip._internal.operations.freeze import FrozenRequirement
from pipm import operations


def test_get_distributions(mocker):
    class Obj(object):
        pass

    dists = []
    for i in range(10):
        obj = Obj()
        obj.project_name = 'pkg_' + str(i)
        dists.append(obj)

    mocker.patch.object(operations, 'get_installed_distributions', return_value=dists)
    assert set(operations.get_distributions().keys()) == {'pkg_' + str(i) for i in range(10)}


def test_get_frozen_reqs(patched_dists):
    freqs = operations.get_frozen_reqs()
    assert len(freqs) == patched_dists.cnt
    assert isinstance(list(freqs.values())[1], FrozenRequirement)


def test_get_orphaned_packages(patched_dists):
    freqs = operations.get_orphaned_packages(['pytest'])
    b = {'atomicwrites', 'attrs', 'more-itertools', 'wcwidth'}
    assert set(freqs) == b or set(freqs) == b.union({"pathlib2", })
