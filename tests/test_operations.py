from pipm import operations


def getdists():
    class Obj(object):
        pass

    dists = []
    for i in range(10):
        obj = Obj()
        obj.project_name = 'pkg_' + str(i)
        dists.append(obj)
    return dists


def test_get_distributions(monkeypatch):
    monkeypatch.setattr(operations, 'get_installed_distributions', getdists)
    assert set(operations.get_distributions().keys()) == {'pkg_' + str(i) for i in range(10)}


def test_get_frozen_reqs():
    freqs = operations.get_frozen_reqs()
    assert len(freqs) == 22
