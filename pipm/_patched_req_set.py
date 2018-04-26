from pip._internal.req.req_set import logger, indent_log, RequirementSet


class PatchedRequirementSet(RequirementSet):
    interactive_install = False

    def install(self, install_options, global_options=(), *args, **kwargs):
        """
        Install everything in this set (after having downloaded and unpacked
        the packages)
        """
        to_install = self._to_install()

        if to_install:
            logger.info(
                'Installing collected packages: %s',
                ', '.join([req.name for req in to_install]),
            )

        with indent_log():
            for requirement in to_install:
                # patch 1: start
                if self.__class__.interactive_install:
                    want_to_install = input('Do you want to update {}? [Y/n]'.format(requirement.req))
                    if str(want_to_install).lower() in {'no', 'n', }:
                        continue
                # patch 1: end

                if requirement.conflicts_with:
                    logger.info(
                        'Found existing installation: %s',
                        requirement.conflicts_with,
                    )
                    with indent_log():
                        requirement.uninstall(auto_confirm=True)
                try:
                    requirement.install(
                        install_options,
                        global_options,
                        *args,
                        **kwargs
                    )
                except:
                    # if install did not succeed, rollback previous uninstall
                    if (requirement.conflicts_with and not
                    requirement.install_succeeded):
                        requirement.rollback_uninstall()
                    raise
                else:
                    if (requirement.conflicts_with and
                            requirement.install_succeeded):
                        requirement.commit_uninstall()
                requirement.remove_temporary_source()

        self.successfully_installed = to_install
