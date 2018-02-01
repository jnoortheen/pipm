
pipm
====

Python package management workflow using pip & requirements file as its metadata. (For the time being until ``Pipfile`` 
is mature.)

Installation
============

Install from PyPI

.. code-block::

   pip install pipm

Or Install directly from the GitHub

.. code-block:: commandline

   pip install -e git://github.com/jnoortheen/pipm.git@master#egg=pipm

Quickstart
==========

All ``pip`` commands will work as it is, plus they will be saved to the requirements file. Both ``pip`` and ``pipm`` command
will work as the same. For some reason, if the pip command is not overridden, you could always rely on ``pipm``. 

warning
-------


* the ``pip`` command will be replaced by the one that comes with this package. There is no functionality gets 
  affected other than manipulating the requirements files. So when you uninstall ``pipm`` the ``pip`` command will also get removed. To remedy this, just install ``pip`` again using ``easy_install pip``
* this tool manipulates all your requirements file. So be sure to use version control software or take backup of your files to keep track of changes. 

installation
^^^^^^^^^^^^

``pipm install pkg-name`` or 
``pip install pkg-name``

installation as development dependency
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

``pipm install pkg-name --dev``

installation as testing dependency
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

``pipm install pkg-name --test``

removal
^^^^^^^

``pipm uninstall pkg-name``

update all your dependencies
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

``pipm update``

install all your dependencies from the requirements file
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

``pipm install``

including development dependencies
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

``pipm install --dev``

Usage
=====


#. 
   install


   * 
     a wrapper around standard ``pip install`` command and accepts all the standard options

     Below are the things that ``pipm`` brings to the table

   * 
     Extra functionality


     * when package names are given it will be saved to the requirements.txt file in the current directory.
       If you have ``requirements`` directory structure with ``base.txt`` inside then that file will be used. Otherwise it 
       will create one in the current directory.
     * when no package name is given then it is equivalent to ``-r requirements.txt`` and it will install all requirements
       from the current directory

   * Additional options:
      the below saves to file when package name given otherwise equivalent to passing requirements file name.

     #. ``--dev`` - saves to development requirements
     #. ``--prod`` - saves to production requirements
     #. ``--test`` - saves to  testing requirements
     #. ``--env <name>`` - if you have any special set of requirements that belong to a separate file you could pass the name here.
        It will search for the matching one in the following pattern ``<name>-requirements.txt`` or 
        ``requirements/<name>.txt`` or ``requirements-<name>.txt``

#. 
   uninstall 


   * a wrapper around standard ``pip uninstall`` command
   * alias ``rm`` is available
   * when uninstalling a package, this command also checks packages that are no longer required by any of the installed
     packages and removes them
   * ofcourse it removes the packages from ``requirements`` files

#. 
   update


   * new command
   * equivalent to calling ``pip install`` with ``--upgrade`` flag
   * update a single package or the whole environment when no argument given.
   * by default the packages are updated interactively

     * set ``--auto-update`` to disable this

#. 
   save/freeze


   * extends the standard freeze command to save the currently installed packages

Features
========


#. Just a wrapper around the standard pip's ``install`` & ``uninstall`` command. So all the cli options will work
#. Handles multiple ``requirements`` files

Development
===========


* clone the repository and create new virtualenv

.. code-block::

   git clone git@github.com:jnoortheen/pipm.git
   cd pipm
   pew new pipm -a .


* 
  install development requirements

  .. code-block::

     pip install -r dev-requirements.txt

* 
  to test from local sources

  .. code-block::

     pip install -e .

Testing
=======


* After installing ``text-requirements.txt`` just run ``invoke test`` from the root directory.

``Note``\ : last tested with pip 9.0.1
