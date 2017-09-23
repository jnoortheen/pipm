# pipm

Python package management workflow using pip & requirements file as its metadata. (For the time being until `Pipfile` 
is mature enough or the `pipenv` is fast enough to use.)

# Installation

Install from PyPI

```
pip install pipm
```

Or Install directly from the GitHub

```commandline
pip install -e git://github.com/jnoortheen/pipm.git@master#egg=pipm
```

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
    1. Additions options:
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


# Features

1. Just a wrapper around the standard pip's `install` & `uninstall` command. So all the cli options will work
1. Handles multiple `requirements` files
 
# Testing

- After installing `requirements` just run `invoke test` from the root directory.

``Note``: last tested with pip 9.0.1