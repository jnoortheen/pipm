from __future__ import absolute_import

import logging
from pip._internal.operations.freeze import FrozenRequirement
from pip._internal.compat import stdlib_pkgs
from pip._internal.commands.freeze import DEV_PKGS
from pip._internal.utils import misc
from pip._internal.utils.misc import get_installed_distributions
import pkg_resources
from six.moves import reload_module

DEV_PKGS = DEV_PKGS.union({'pipm', })
logger = logging.getLogger(__name__)

STD_PKGS = stdlib_pkgs.union(DEV_PKGS)


def get_dependency_links():
    dep_links = []
    reload_module(pkg_resources)

    for dist in pkg_resources.working_set:
        if dist.has_metadata('dependency_links.txt'):
            dep_links.extend(
                dist.get_metadata_lines('dependency_links.txt')
            )
    return dep_links


def get_frozen_reqs():
    dependency_links = get_dependency_links()
    installations = {}

    for _, dist in get_distributions().items():
        try:
            req = FrozenRequirement.from_dist(
                dist,
                dependency_links
            )
        except pkg_resources.RequirementParseError:
            logger.warning("Could not parse requirement: %s", dist.project_name)
            continue
        installations[req.name] = req

    return installations


def get_distributions():
    """

    Returns:
        dict:
    """

    reload_module(misc.pkg_resources)
    reload_module(misc)
    return {dist.project_name.lower(): dist for dist in
            get_installed_distributions(local_only=None, skip=STD_PKGS, user_only=None)}


def get_orphaned_packages(pkgs):
    """
        return list of packages that is only required by the pkgs given but not other installed packages
    Args:
        pkgs (list):

    Returns:
        list:
    """

    dists = get_distributions()
    removed_packages = []
    for pkg in pkgs:  # type: str
        pkgl = pkg.lower()
        if pkgl in dists:
            removed_packages.append(dists.pop(pkgl))

    orphaned_pkgs = set()
    for dist in removed_packages:  # type: pkg_resources.DistInfoDistribution
        for r in dist.requires():
            orphaned_pkgs.add(r.name)

    all_requires = set()
    for dist in dists:
        for r in dists[dist].requires():
            all_requires.add(r.name)

    orphaned_pkgs = orphaned_pkgs.difference(all_requires)
    return list(orphaned_pkgs.difference(set(STD_PKGS)))
