import logging

import pkg_resources

from pip._internal.commands.freeze import DEV_PKGS
from pip._internal.metadata import BaseDistribution, get_environment
from pip._internal.operations.freeze import FrozenRequirement
from pip._internal.utils.compat import stdlib_pkgs

# DEV_PKGS = DEV_PKGS.union({"pipm"})
logger = logging.getLogger(__name__)

STD_PKGS = stdlib_pkgs.union(DEV_PKGS)


def get_frozen_reqs():
    installations = {}

    for _, dist in get_distributions().items():
        try:
            req = FrozenRequirement.from_dist(dist)
        except pkg_resources.RequirementParseError:
            logger.warning("Could not parse requirement: %s", dist.canonical_name)
            continue
        installations[req.name] = req

    return installations


def _get_distributions():
    return get_environment(None).iter_installed_distributions()


def get_distributions() -> "dict[str, BaseDistribution]":
    def collect():
        for dist in _get_distributions():
            name = dist.canonical_name.lower()
            if name not in STD_PKGS:
                yield name, dist

    return dict(collect())


def get_orphaned_packages(pkgs: "list[str]"):
    """
        return list of packages that is only required by the pkgs given but not other installed packages
    Args:
        pkgs (list):

    Returns:
        list:
    """

    dists = get_distributions()
    orphaned_pkgs = set()
    for pkg in pkgs:
        pkgl = pkg.lower()
        if pkgl in dists:
            removed_pkg = dists.pop(pkgl)
            for r in removed_pkg.iter_dependencies():
                orphaned_pkgs.add(r.name)

    all_requires = set()
    for dist in dists:
        for r in dists[dist].iter_dependencies():
            all_requires.add(r.name)

    orphaned_pkgs = orphaned_pkgs.difference(all_requires)
    return list(orphaned_pkgs.difference(set(STD_PKGS)))
