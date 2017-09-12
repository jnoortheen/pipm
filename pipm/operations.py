from __future__ import absolute_import

import logging
import pip
from pip.utils import get_installed_distributions
from pip.utils import pkg_resources
from pkg_resources import RequirementParseError

logger = logging.getLogger(__name__)
try:
    reload
except NameError:
    from importlib import reload
except ImportError:
    from imp import reload


def get_installations(find_links=None, local_only=None, user_only=None, ):
    find_links = find_links or []

    dependency_links = []

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
        installations[req.name] = req
    return installations
