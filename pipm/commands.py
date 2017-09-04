from pkg_resources._vendor.packaging.specifiers import SpecifierSet
from pip.req import InstallRequirement
from pip.commands import InstallCommand
import pip
from .file import get_requirements_filename


class InstallCommandPlus(InstallCommand):
    def run(self, options, args):
        reqs = super(InstallCommandPlus, self).run(options, args)
        # consider appending to requirements.txt only
        if not options.requirements:
            for req in reqs.successfully_installed:  # type: InstallRequirement
                if not req.req.specifier:
                    if req.specifier:
                        req.req.specifier = req.specifier
                    elif req.installed_version:
                        req.req.specifier = SpecifierSet('==' + req.installed_version)
                if not req.req.extras and req.extras:
                    req.req.extras = req.extras
                if not req.req.marker and req.markers:
                    req.req.marker = req.markers
                if not req.req.url and req.link:
                    req.req.url = req.link if isinstance(req.link, str) else req.link.url

                # add these lines to requirements.txt
                try:
                    frozenrequirement = pip.FrozenRequirement.from_dist(req.get_dist(), [])
                except Exception:
                    frozenrequirement = pip.FrozenRequirement(req.name, req.req, req.editable)

                with open(get_requirements_filename(), 'ab+') as f:
                    f.write((str(frozenrequirement).strip() + '\n').encode('utf-8'))
        return reqs
