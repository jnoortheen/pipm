# pipm

Python package management workflow using pip, requirements file & setup.cfg as its metadata. 
(For the time being and old world of python)

# Installation

- Adviced to install only inside virtualenv as this will replace pip executable

Install from PyPI

```
pip install six
pip install pipm
```

Or Install directly from the GitHub

```commandline
pip install -e git://github.com/jnoortheen/pipm.git@master#egg=pipm
```

**Note:**
- This tool manipulates all your requirements file. So be sure to use version control software or take backup of your files to keep track of changes. 

# Quickstart
All `pip` commands will work as it is, plus they will be saved to the requirements file. Both `pip` and `pipm` command
will work as the same. For some reason, if the pip command is not overridden, you could always rely on `pipm`.   

### install all your dependencies from the requirements file

- to install only from `requirements.txt` 

```pipm install```
- to install from all `*requirements*.txt`

```pipm install --all```

### installation
```pipm install pkg-name``` or 
```pip install pkg-name```

### installation as development dependency
```pipm install pkg-name --dev```


### installation as testing dependency
```pipm install pkg-name --test```

### removal 
```pipm uninstall pkg-name```

### update all your dependencies
```pipm update```

### including development dependencies
```pipm install --dev```


# Usage

1. install
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

1. uninstall 
    - a wrapper around standard `pip uninstall` command
    - alias `rm` is available
    - when uninstalling a package, this command also checks packages that are no longer required by any of the installed
    packages and removes them
    - ofcourse it removes the packages from `requirements` files

1. update
    - new command
    - equivalent to calling `pip install` with `--upgrade` flag
    - update a single package or the whole environment when no argument given.
    - by default the packages are updated interactively
        - set `--auto-update` to disable this

1. save/freeze
    - extends the standard freeze command to save the currently installed packages


# Features

1. Just a wrapper around the standard pip's `install/uninstall` command. So all the cli options will work
2. Handles multiple `requirements` files
3. No new set of files. requirements files contain pinned dependecies and setup.cfg contain abstract dependencies.

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

# Testing

- run `invoke test` from the root directory.

# Version compatibility

the package is versioned in accordance with `pip` major version number. 
`pipm-9.*` will be compatible with `pip-9` and such.

# Uninstallation Notes

- since pipm overwrites pip executable in path, please make sure that after removing `pipm`, 
install pip itself with `easy_install`

```commandline
pip uninstall pipm
easy_install pip
```

# Alternatives and their problems (IMHO)

1. [pipenv](https://docs.pipenv.org/) 
    - good for local development with only one virtual environment per project
    - Not good when we need to deploy over production server or keep multiple virtuals-envs
    - it is better to use `pew` alone instead of the shell command that comes with this
2. [pip-tools](https://github.com/jazzband/pip-tools)
    - another set of files to keep track of, additional commands to remember
3. [poetry](https://github.com/sdispater/poetry) 
    - better than pipenv and do not interfere much in environment management with pew
    - the problems I faced are related to installing dependencies in remote servers/docker environments. 
    As the project matures this problem might get resolved. 
        
