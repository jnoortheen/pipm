from pip._internal.operations.freeze import FrozenRequirement
from pipm.src import operations


def test_get_frozen_reqs(patched_dists):
    freqs = operations.get_frozen_reqs()
    assert len(freqs) == patched_dists.cnt
    assert isinstance(list(freqs.values())[1], FrozenRequirement)


def test_get_orphaned_packages(patched_dists):
    freqs = operations.get_orphaned_packages(["proj-0"])
    assert set(freqs) == {"proj-1"}
