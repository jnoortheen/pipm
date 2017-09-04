# pipm

Python package management workflow using pip & requirements file as its metadata

# Installation

Install directly from the GitHub (No PyPI version yet)

```commandline
pip install git://github.com/jnoortheen/pipm.git@master#egg=pipm
```

# Usage

1. install
    - a wrapper around standard `pip install` command and accepts all the standard options
    
    1. Extra functionality
    - when package names are given it will be saved to the requirements.txt file in the current directory.
    If you have `requirements` directory structure with `base.txt` inside then that file will be used. Else it 
    will create one in the current directory.
    - when no package name is given then it is equivalent to `-r requirements.txt` and it will install all requirements
    from the current directory
    1. Extra options:
        1. `--dev` - saves to `dev-requirements.txt` or `requirements/dev.txt` or `requirements/development.txt`
        1. `--prod` - saves to `prod-requirements.txt` or `requirements/prod.txt` or `requirements/production.txt`
        1. `--test` - saves to  `test-requirements.txt` or `requirements/test.txt`
        1. `--env <name>` - if you have any special set of requirements that belong to a separate file you could pass the name here.
        It will search for the matching one in the following pattern `<name>-requirements.txt` or 
        `requirements/<name>.txt`
    