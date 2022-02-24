## 22.2.0 (2022-02-24)

### Feat

- use commitizen to provide setup.py version

## 22.1.0 (2022-02-24)

### Refactor

- use pyupgrade to update codebase to py3.7+
- move src into separate package

### Feat

- use github for ci env
- vendor pip 22.0.3

## 20.1 (2021-02-02)

### Refactor

- drop py2 support

### Fix

- invalid git+ssh url generated from pip-freeze

### Feat

- use twine for uploading packages

## 20.2.4 (2020-11-24)

## 20.2.0 (2020-08-10)

### Feat

- update for pip20.2

## 20.1.0 (2020-05-17)

### Feat

- support pip~=20.1 versions
- replace pickle based testing for distributions
- add pycrunch test runner
- migrate interactive update feature for pip-20
- add support for pip~=20

### Fix

- py2 vs py3 compatibility
- add requirements to setup.cfg correctly
- failed to upload to pypi with md format

### Refactor

- update tests
- split file module

## 19.3.5 (2019-10-23)

## 19.3.4 (2019-10-23)

### Fix

- ensure latest pip version installed while testing in travis

## 19.3.3 (2019-10-23)

### Fix

- update travis pip version closes #4

## 19.3.2 (2019-10-23)

### Refactor

- black format

## 19.3.1 (2019-10-22)

### Refactor

- black format
- update commands.py for pip 19.3.1

### Feat

- update __main__.py for pip 19.3.1

## 19.0.0 (2019-01-29)

### Feat

- updates for pip-19

## 18.6.2 (2018-12-27)

## 18.6.1 (2018-12-27)

### Fix

- correct annotation for py2

### Feat

- add ability to update requirements based on setup.cfg

## 18.5.1 (2018-11-27)

### Fix

- handle error when installed_version is None

## 18.5 (2018-10-31)

### Feat

- case-insensitive sorting in setup.cfg

## 18.4.1 (2018-10-31)

## 18.4 (2018-10-29)

### Refactor

- save setup.cfg requirements in sorted manner

## 18.3 (2018-10-29)

### Fix

- Py2 compatibility issues of configparser closes #2

## 18.2.0 (2018-10-29)

### Refactor

- update py27 conflicting usage of configparser
- update py27 conflicting requirements

## 18.1 (2018-10-05)

### Feat

- updated for pip 18.1

## 18.0.2 (2018-10-02)

## 18.0.1 (2018-10-02)

### Fix

- getting version from package

## 18.0.0 (2018-10-01)

### Feat

- add check that pipm is run inside virtualenv only
- remove requirements from setup.cfg after uninstall

## 10.4.4 (2018-09-19)

### Feat

- remove pyproject.toml and use setup.py
- update invoke tasks

## 10.4.3 (2018-08-21)

### Feat

- bumping version to 10.4.3
- use poetry for managing project dependencies

## 10.4.2 (2018-07-09)

### Fix

- updating setup.cfg extra requires section

## 10.4.1 (2018-07-09)

### Fix

- requiring six to be installed before package
- requiring six to be installed before package

## 10.4.0 (2018-07-08)

### Fix

- saving requirements to files

## 10.3.0 (2018-07-04)

### Feat

- add ability to save abstract meta data to setup.cfg fixes #1
- adding six to project

### Refactor

- remove unused file patched request

## 10.2.0 (2018-07-03)

### Fix

- correct python2 errors

## 10.1.0 (2018-06-10)

### Fix

- correct interactive-update option for pip-10.0

## 10.0.0 (2018-04-26)

### Feat

- update for pip>=10.0.0

## 9.0.0 (2018-04-26)

### Feat

- introducing version based compatibility with pip

## 1.1.0 (2018-02-02)

## 1.0.1 (2018-02-02)

## 1.0 (2018-02-02)

### Refactor

- update readme
- adding alias u for update command

### Feat

- adding ability to interactively update packages

## 0.9.3 (2017-12-19)

## 0.9.2 (2017-12-18)

## 0.9.1 (2017-12-18)

### Feat

- do not add pipm to requirements

## 0.9 (2017-12-01)

### Feat

- override default pip script
- add --all argument to install command

## 0.8 (2017-11-15)

### Feat

- extend freeze mtheod to save on freeze

## 0.7.2 (2017-10-05)

### Feat

- call save after every install even when nothing installed

## 0.7.1 (2017-09-23)

### Fix

- return correct base file name when requirements dir is present

## 0.7 (2017-09-23)

### Feat

- adding rm command for uninstall

### Fix

- saving requirement to a new file

## 0.6.5 (2017-09-23)

### Fix

- correct get_orphaned_pkg method

### Feat

- using invoke script instead of fabric

## 0.6.4 (2017-09-23)

### Refactor

- regression and add more tests

## 0.6.3 (2017-09-17)

### Fix

- correctly create requirement line in additional req files

## 0.6.2 (2017-09-17)

## 0.6.1 (2017-09-16)

## 0.6 (2017-09-15)

### Feat

- uploading package to PyPI

## 0.5 (2017-09-12)

## 0.4 (2017-09-12)

### Feat

- update uninstall command to remove orphaned packages
- adding update command

## 0.3 (2017-09-12)

### Feat

- update save method to strip empty lines
- update pipm save requirements file method
- adding separate method to call the main process
- adding pip/opertations/freeze.py
- update save_req method on commands
- adding save file function
- pump version

## 0.2 (2017-09-08)

### Refactor

- update pipm.file functions

### Feat

- improve installcommandplus

### Fix

- recursive paths

## 0.1 (2017-09-04)

### Feat

- adding installcommand
- create pipm package
