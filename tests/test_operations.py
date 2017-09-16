import os

from pip import FrozenRequirement

from pipm import operations
import pickle


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


def test_get_frozen_reqs(monkeypatch):
    with open(os.path.join(os.path.dirname(__file__), 'pkgs.pickle'), 'rb') as f:
        dists = pickle.loads(f.read())
    assert len(dists) == 23
    assert type(dists) == dict

    def getdists(**args):
        return dists

    monkeypatch.setattr(operations, 'get_distributions', getdists)

    freqs = operations.get_frozen_reqs()
    assert len(freqs) == 23
    assert isinstance(list(freqs.values())[1], FrozenRequirement)


def test_get_orphaned_packages(monkeypatch):
    with open(os.path.join(os.path.dirname(__file__), 'pkgs.pickle'), 'rb') as f:
        dists = pickle.loads(f.read())
    assert len(dists) == 23

    def getdists(**args):
        return dists

    monkeypatch.setattr(operations, 'get_distributions', getdists)

    freqs = operations.get_orphaned_packages(['pytest'])
    assert set(freqs) == {'py', }
