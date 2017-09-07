import unittest

import os

from pipm import InstallCommandPlus
from pipm.file import get_req_filename
from pip.req.req_install import InstallRequirement


class TestInstallCommand(unittest.TestCase):
    def test_fill_args_when_no_args_given(self):
        f = get_req_filename()
        cmd = InstallCommandPlus()
        opts, args = cmd.parse_args([])
        self.assertEqual(opts.requirements, [f, ])
        os.remove(f)

    def test_saves_requirements_to_file(self):
        cmd = InstallCommandPlus()
        opts, args = cmd.parse_args(['pyreqs', '--dev'])
        fname = get_req_filename(opts.req_environment)
        reqs_sample = """pkg_one==1.0.1\npkg_two==2.0.1"""
        reqs = [InstallRequirement.from_line(line) for line in reqs_sample.splitlines(False)]
        cmd._save_requirements(fname, *reqs)
        try:
            with open(fname) as f:
                self.assertEqual(f.read().strip(), "-r requirements.txt\n" + reqs_sample)
        finally:
            os.remove(fname)
            os.remove(get_req_filename())


if __name__ == '__main__':
    unittest.main()
