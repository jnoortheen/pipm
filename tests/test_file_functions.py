import os

import py
import pytest
import codecs

from py._path.local import LocalPath

from pipm import file

reqs = """\
# standard package name alone
requests
# package with more options
FooProject >= 1.2 --global-option="--no-user-cfg" \
                  --install-option="--prefix='/usr/local'" \
                  --install-option="--no-compile"
# git install from link
-e git+https://github.com/d0c-s4vage/pyactlab.git@feather-master#egg=pyactlab
-e git+git@git.myproject.org:MyProject#egg=MyProject
# with hash
FooProject == 1.2 --hash=sha256:2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824 \
                  --hash=sha256:486ea46224d1bb4fb680f34f7c9ad96a8f24ec88be73ea8e5a6c65260e9cb8a7a
"""
dev_reqs = """\
-r requirements.txt

some_content==0.1.0 # with inline comment you need to write this back
"""


def test_append_last_line(tmpdir):
    p = tmpdir.mkdir("sub").join("hello.txt")
    p.write("content")
    file._new_line(p)
    assert p.read() == "content\n"


def test_get_env_reqfile_case1(tmpdir):
    p = tmpdir.mkdir("sub").join("hello.txt")  # type: LocalPath
    p.write('content')
    paths = ['_estins.txt', p.strpath]

    # case 1: returns first existing path
    f = file.get_env_reqfile(*paths)
    assert f == paths[1]


def test_get_env_reqfile_case2():
    # case 2: creates file
    fname = 'some-requirements.txt'
    assert fname == file.get_env_reqfile(fname, base_file_name='requirements/base.txt', )
    with open(fname) as f:
        cnt = f.read()
        assert cnt == '-r base.txt'
    assert os.path.exists(fname)
    os.remove(fname)


def test_get_req_filename(tmpdir):
    """

    Args:
        tmpdir (LocalPath): fixture

    """
    os.chdir(tmpdir.strpath)
    assert file.get_req_filename('dev') == 'dev-requirements.txt'
    assert file.get_req_filename() == 'requirements.txt'


def test_parse(tmpdir):
    os.chdir(tmpdir.strpath)
    fname = file.get_req_filename()
    with codecs.open(fname, 'w', 'utf-8') as f:
        f.write(reqs)

    # single file parsing
    install_reqs = file.parse()
    assert len(install_reqs) == 4

    # nested file parsing
    fname = file.get_req_filename('dev')
    with codecs.open(fname, 'w', 'utf-8') as f:
        f.write(dev_reqs)
    install_reqs = file.parse('dev')
    assert len(install_reqs) == 5
