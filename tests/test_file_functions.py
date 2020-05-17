import os

from py._path.local import LocalPath

from pipm import file, file_utils


def test_append_last_line(tmpdir):
    p = tmpdir.mkdir("sub").join("hello.txt")
    p.write("content")
    file_utils._new_line(str(p))
    assert p.read() == "content\n"


def test_get_env_reqfile_case1(tmpdir):
    p = tmpdir.mkdir("sub").join("hello.txt")  # type: LocalPath
    p.write("content")
    paths = ["_estins.txt", p.strpath]

    # case 1: returns first existing path
    f = file_utils.get_env_reqfile(*paths)
    assert f == paths[1]


def test_get_env_reqfile_case2(chdir):
    # case 2: creates file inside folder
    fname = "requirements/some.txt"
    assert fname == file_utils.get_env_reqfile(
        fname, base_file_name="requirements/base.txt",
    )
    with open(fname) as f:
        cnt = f.read()
        assert cnt == "-r base.txt"
    assert os.path.exists(fname)


def test_get_req_filename(chdir):
    assert file_utils.get_req_filename("dev") == "dev-requirements.txt"
    assert {"dev-requirements.txt", "requirements.txt"} == set(os.listdir(os.curdir))


def test_get_req_filename_case2(chdir):
    """
        test it creates inside requirements directory
    """
    file_utils.get_req_filename()  # create requirements.txt
    rb = chdir.mkdir("requirements").join("base.txt")
    rb.write("test")
    assert file_utils.get_req_filename("test") == "requirements/test.txt"
    assert {"base.txt", "test.txt"} == set(
        os.listdir(os.path.join(os.curdir, "requirements"))
    )

    # test it return base name when dir exists
    assert file_utils.get_req_filename() == "requirements/base.txt"


def test_cluster_file_reqs(data_dir, pkg_ir_py, pkg_ir_six):
    # requirements from files
    _, reqs = file.get_parsed_requirements()

    # requirements without files
    reqs[pkg_ir_py.name] = pkg_ir_py
    reqs[pkg_ir_six.name] = pkg_ir_six

    file_reqs = file.cluster_to_file_reqs(reqs, "new")
    assert set(file_reqs.keys()) == {
        "dev-requirements.txt",
        "requirements.txt",
        "new-requirements.txt",
    }
    assert_names(
        file_reqs["requirements.txt"],
        ["requests", "FooProject", "pyactlab", "MyProject", "Foo2Project"],
    )
    assert_names(file_reqs["dev-requirements.txt"], ["some-content"])
    assert_names(file_reqs["new-requirements.txt"], ["py", "six"])


def assert_names(reqs, expected):
    assert [req.req.name for req in reqs] == expected


def test_parse_comes_from(chdir):
    forig = "tests/fixtures/requirements.txt"
    fname, line = file_utils.parse_comes_from("-r {} (line 11)".format(forig), "dev")
    assert fname == forig
    assert line == 11


def test_parse_comes_from_case_nofile(chdir):
    fname, line = file_utils.parse_comes_from(None, "dev")
    assert fname == file_utils.get_req_filename("dev")
    assert line is None


def test_uniq_reqs(chdir, pkg_ir_six, pkg_ir_py):
    ireqs = [pkg_ir_six, pkg_ir_py] + [pkg_ir_six]
    ireqs = file._uniq_resources(ireqs)
    assert len(ireqs) == 2


def test_get_requirement_files(chdir):
    os.mkdir("requirements")
    base_fname = os.path.join("requirements", "base.txt")
    open(base_fname, "wb").close()
    file_utils.get_req_filename("dev")
    file_utils.get_req_filename("test")
    assert file.get_req_filenames() == {
        "requirements/development.txt",
        "requirements/base.txt",
        "requirements/test.txt",
    }


def test_get_requirement_files_case2(chdir):
    file_utils.get_req_filename("dev")
    file_utils.get_req_filename("test")
    assert file.get_req_filenames() == {
        "dev-requirements.txt",
        "requirements.txt",
        "test-requirements.txt",
    }


def test_file_save_method(chdir, patch_dists):
    # save requirements to file
    m = patch_dists()
    file.save()
    _, reqs = file.get_parsed_requirements()
    assert len(reqs) == m.cnt

    # check it is getting removed
    m = patch_dists(2)
    file.save()
    _, reqs = file.get_parsed_requirements()
    assert len(reqs) == m.cnt


def test_get_patterns():
    assert set(file_utils.get_patterns("dev", "development")) == {
        "dev-requirements.txt",
        "requirements/dev.txt",
        "requirements-dev.txt",
        "development-requirements.txt",
        "requirements/development.txt",
        "requirements-development.txt",
    }
    assert file_utils.get_patterns("base") == [
        "requirements.txt",
        "requirements/base.txt",
    ]
