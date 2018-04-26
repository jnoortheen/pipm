from pip._internal.operations.freeze import FrozenRequirement
from pipm import operations


def test_get_distributions(monkeypatch):
    def getdists(**args):
        class Obj(object):
            pass

        dists = []
        for i in range(10):
            obj = Obj()
            obj.project_name = 'pkg_' + str(i)
            dists.append(obj)
        return dists

    monkeypatch.setattr(operations, 'get_installed_distributions', getdists)
    assert set(operations.get_distributions().keys()) == {'pkg_' + str(i) for i in range(10)}


def test_get_frozen_reqs(patch_dists):
    freqs = operations.get_frozen_reqs()
    assert len(freqs) == 23
    assert isinstance(list(freqs.values())[1], FrozenRequirement)


def test_get_orphaned_packages(patch_dists):
    freqs = operations.get_orphaned_packages(['pytest'])
    assert set(freqs) == {'req_by_pytest', }
