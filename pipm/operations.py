from __future__ import absolute_import

import logging
import pip
from pip.utils import get_installed_distributions
from pip.utils import pkg_resources
from pkg_resources import RequirementParseError, DistInfoDistribution
from pip.compat import stdlib_pkgs
from pip.commands.freeze import DEV_PKGS

logger = logging.getLogger(__name__)
try:
    reload
except NameError:
    from importlib import reload
except ImportError:
    from imp import reload


def get_frozen_reqs(find_links=None, local_only=None, user_only=None, ):
    find_links = find_links or []

    dependency_links = []
    skip = stdlib_pkgs + DEV_PKGS

    reload(pkg_resources)

    for dist in pkg_resources.working_set:
        if dist.has_metadata('dependency_links.txt'):
            dependency_links.extend(
                dist.get_metadata_lines('dependency_links.txt')
            )
    for link in find_links:
        if '#egg=' in link:
            dependency_links.append(link)
    installations = {}

    for dist in get_installed_distributions(local_only=local_only,
                                            skip=(),
                                            user_only=user_only):
        try:
            req = pip.FrozenRequirement.from_dist(
                dist,
                dependency_links
            )
        except RequirementParseError:
            logger.warning(
                "Could not parse requirement: %s",
                dist.project_name
            )
            continue
        if req.name not in skip:
            installations[req.name] = req
    return installations


def get_distributions():
    reload(pkg_resources)

    return {dist.project_name.lower(): dist for dist in get_installed_distributions()}


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
        removed_packages.append(dists.pop(pkg.lower()))

    orphaned_pkgs = set()
    for dist in removed_packages:  # type: DistInfoDistribution
        for r in dist.requires():
            orphaned_pkgs.add(r.name)

    all_requires = set()
    for dist in dists:
        for r in dists[dist].requires():
            all_requires.add(r.name)

    return list(orphaned_pkgs.difference(all_requires))
