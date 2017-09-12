import codecs
import os

from py._path.local import LocalPath

from pipm import file

REQS_STR = """\
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
Foo2Project == 1.2 --hash=sha256:2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824 \
                  --hash=sha256:486ea46224d1bb4fb680f34f7c9ad96a8f24ec88be73ea8e5a6c65260e9cb8a7a
"""
DEV_REQS_STR = """\
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


def test_get_env_reqfile_case2(chdir):
    # case 2: creates file
    fname = 'some-requirements.txt'
    assert fname == file.get_env_reqfile(fname, base_file_name='requirements/base.txt', )
    with open(fname) as f:
        cnt = f.read()
        assert cnt == '-r base.txt'
    assert os.path.exists(fname)


def test_get_req_filename(chdir):
    """

    Args:
        tmpdir (LocalPath): fixture

    """
    assert file.get_req_filename('dev') == 'dev-requirements.txt'
    assert file.get_req_filename() == 'requirements.txt'


def test_parse_simple(chdir):
    fname = file.get_req_filename()
    with codecs.open(fname, 'w', 'utf-8') as f:
        f.write(REQS_STR)

    # single file parsing
    install_reqs = file.parse()
    for r in install_reqs:
        print(r)
    assert len(install_reqs) == 5


def test_parse_nested(chdir):
    # nested file parsing
    with codecs.open(file.get_req_filename(), 'w', 'utf-8') as f:
        f.write(REQS_STR)
    fname = file.get_req_filename('dev')
    with codecs.open(fname, 'w', 'utf-8') as f:
        f.write(DEV_REQS_STR)
    install_reqs = file.parse('dev')
    assert len(install_reqs) == 6


def test_cluster_file_reqs(chdir):
    with codecs.open(file.get_req_filename(), 'w', 'utf-8') as f:
        f.write(REQS_STR)
    fname = file.get_req_filename('dev')
    with codecs.open(fname, 'w', 'utf-8') as f:
        f.write(DEV_REQS_STR)
    install_reqs = file.parse('dev')
    file_reqs = file._cluster_to_file_reqs(install_reqs, 'div')
    assert set(file_reqs.keys()) == {'dev-requirements.txt', 'requirements.txt'}


def test_parse_comes_from(chdir):
    forig = 'tests/fixtures/requirements.txt'
    fname, line = file.parse_comes_from('-r {} (line 11)'.format(forig), 'dev')
    assert fname == forig
    assert line == 11


def test_parse_comes_from_case_nofile(chdir):
    fname, line = file.parse_comes_from(None, 'dev')
    assert fname == file.get_req_filename('dev')
    assert line is None


def test_uniq_reqs(chdir):
    fname = file.get_req_filename()
    with codecs.open(fname, 'w', 'utf-8') as f:
        f.write(REQS_STR)
    install_reqs = file.parse()
    ireqs = install_reqs + install_reqs
    ireqs = file._uniq_resources(ireqs)
    assert len(ireqs) == 5


def test_get_requirement_files(tmpdir):
    reqf = tmpdir.mkdir('reqf')
    os.chdir(reqf.strpath)
    os.mkdir('requirements')
    base_fname = os.path.join('requirements', 'base.txt')
    open(base_fname, 'wb').close()
    file.get_req_filename('dev')
    file.get_req_filename('test')
    assert file.get_req_filenames() == {
        'requirements/development.txt',
        'requirements/base.txt',
        'requirements/test.txt',
    }
