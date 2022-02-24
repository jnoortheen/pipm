import logging
from pathlib import Path

import pkg_resources

from pip._internal.commands.freeze import DEV_PKGS
from pip._internal.metadata import BaseDistribution, get_environment
from pip._internal.operations.freeze import FrozenRequirement
from pip._internal.req import InstallRequirement
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


def get_dist(ireq: InstallRequirement) -> "BaseDistribution":
    return get_environment(None).get_distribution(ireq.req.name)


def _get_distributions():
    return get_environment(None).iter_installed_distributions()


def get_distributions() -> "dict[str, BaseDistribution]":
    def collect():
        for dist in _get_distributions():
            name = dist.canonical_name.lower()
            if name not in STD_PKGS:
                yield name, dist

    return dict(collect())


def get_comes_from(req):
    if req.comes_from:
        if isinstance(req.comes_from, str):
            comes_from = req.comes_from
        else:
            comes_from = req.comes_from.from_path()
        if comes_from:
            return f" (from {comes_from})"
    return ""


def get_installed_version(ireq: InstallRequirement):
    dist = get_dist(ireq)
    if dist:
        return str(dist.version)


def format_for_display(req: InstallRequirement):
    def parts():
        yield str(req.req.name)

        if req.local_file_path:
            new_version = Path(req.local_file_path).name

            installed = get_installed_version(req)
            if installed:
                yield f" ({installed} -> {new_version})"
            else:
                yield f" (installs {new_version})"

        yield get_comes_from(req)

    return "".join(parts())


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
