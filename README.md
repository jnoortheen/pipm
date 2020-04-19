# pipm

[![Build Status](https://travis-ci.com/jnoortheen/pipm.svg?branch=master)](https://travis-ci.com/jnoortheen/pipm)

Python package management workflow using pip, requirements file & setup.cfg as its metadata.
(For the time being, for old world of 🐍)

# Installation

- Adviced to install only inside virtualenv

Install from PyPI

```
pip install pipm
```

**Note:**
- This tool manipulates all your requirements file. So be sure to use version control software or take backup of your files to keep track of changes.

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

1. Just a wrapper around the standard pip's `install/uninstall` command. So all the cli options will work
2. Handles multiple `requirements` files
3. No new set of files. requirements files contain pinned dependecies and setup.cfg contain abstract dependencies.

# Version compatibility

the package is versioned in accordance with `pip` major version number.
`pipm-9.*` will be compatible with `pip-9` and such.


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
    1. Additional options:
        the below saves to file when package name given otherwise equivalent to passing requirements file name.
        1. `--dev` - saves to development requirements
        1. `--prod` - saves to production requirements
        1. `--test` - saves to  testing requirements
        1. `--env <name>` - if you have any special set of requirements that belong to a separate file you could pass the name here.
        It will search for the matching one in the following pattern `<name>-requirements.txt` or
        `requirements/<name>.txt` or `requirements-<name>.txt`


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


# Alternatives and their problems (IMHO)

1. [pipenv](https://docs.pipenv.org/)
    - good for local development with only one virtual environment per project
    - Not good when we need to deploy over production server or keep multiple virtuals-envs
    - it is better to use `pew` alone instead of the shell command that comes with this
2. [pip-tools](https://github.com/jazzband/pip-tools)
    - another set of files to keep track of, additional commands to remember
3. [poetry](https://github.com/sdispater/poetry) 
    - more robust than `pipenv`
    - the problems I faced are related to installing dependencies in remote servers/docker environments. 
    - longer install/update times
    As the project matures this problem might get resolved. 


# TODOs:

 - rm will check whether a package is present in setup.cfg
