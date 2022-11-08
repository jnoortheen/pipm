
**Deprecation Notice**: Since [PEP-621](https://peps.python.org/pep-0621/) is now accepted, it is advised to use `pyproject.toml` to store the Project's dependency list. Here are some projects supporting `PEP-621`
  - [pdm](https://github.com/pdm-project/pdm)
  - [pip-tools](https://github.com/jazzband/pip-tools)
  - [hatch](https://github.com/pypa/hatch)


# pipm

[![Build Status](https://travis-ci.com/jnoortheen/pipm.svg?branch=master)](https://travis-ci.com/jnoortheen/pipm)

Python package management using pip, requirements file & [setup.cfg](https://setuptools.pypa.io/en/latest/userguide/declarative_config.html).


# Installation

- Adviced to install only inside virtualenv

Install from PyPI

```
pip install pipm
```

**Note:**
- This tool manipulates all your requirements file. So be sure to use a version control software to keep track of the changes.

# Quickstart

- Both `pip` and `pipm` command will work as the same.
- Create a virtualenv for the project and install pipm with 
```sh
pip install pipm
``` 
- Create an alias as `alias pip=pipm` or use as it is - `pipm`

## I. Install

- install all your dependencies from the base requirements file (`requirements.txt`)
```sh
pipm install
pipm install --all  # *requirements*.txt - all environment -> test/prod/dev
```

## 2. Add new packages to project
```sh
pipm install pkg-name
pipm install pkg-name --dev # as development dependency
pipm install pkg-name --test # as testing dependency
```

## 3. Removal of packages
- Remove one or more packages. Their dependencies will also get uninstalled. No orphaned packages. 
```sh
pipm uninstall pkg-name
```

## 4. update all your dependencies in requirements.txt
```sh
pipm update
pipm update --dev
```

# Features

1. No new set of files. `*-requirements.txt` works like the lockfile with pinned versions 
2. Just a wrapper around the standard pip's `install/uninstall` command. So all the cli options will work
3. Handles multiple `requirements` files
  and [setup.cfg](https://setuptools.pypa.io/en/latest/userguide/declarative_config.html) stores abstract dependencies.


# Commands

## 1. install
 - a wrapper around standard `pip install` command and accepts all the standard options

 Below are the things that `pipm` brings to the table

1. Extra functionality
    - when package names are given it will be saved to the requirements.txt file in the current directory.
    If you have `requirements` directory structure with `base.txt` inside then that file will be used. Otherwise it
    will create one in the current directory.
    - when no package name is given then it is equivalent to `-r requirements.txt` and it will install all requirements
    from the current directory
2. Additional options:
    It will search for the matching one in the following pattern `<name>-requirements.txt` or
    `requirements/<name>.txt` or `requirements-<name>.txt`
    the below saves to file when package name given otherwise equivalent to passing requirements file name.
   1. `--dev` - saves to development requirements
   2. `--prod` - saves to production requirements
   3. `--test` - saves to  testing requirements
   4. `--doc` - saves to  documentation requirements
   5. `--env <name>` - if you have any special set of requirements that belong to a separate file you could pass the name here.


## 2. uninstall 
 - a wrapper around standard `pip uninstall` command
 - alias `rm` is available
 - when uninstalling a package, this command also checks packages that are no longer required by any of user installed
 packages and removes them
 - ofcourse it removes the packages from `requirements` files

## 3. update
 - new command
 - equivalent to calling `pip install` with `--upgrade` flag
 - update a single package or the whole environment when no argument given.
 - by default the packages are updated interactively
     - set `--auto-update` to disable this

## 4. save/freeze
 - extends the standard freeze command to save the currently installed packages

# Development
- clone the repository and create new virtualenv

```
git clone git@github.com:jnoortheen/pipm.git
cd pipm
pew new pipm -a .
pip install -r dev-requirements.txt
```

-  to test from local sources
```
pip install -e .
```

- Commit message should follow [this](https://udacity.github.io/git-styleguide/) style-guide.

## Testing

- run `invoke test` from the root directory.


# TODOs:

 - rm will check whether a package is present in setup.cfg
