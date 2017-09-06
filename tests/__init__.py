import unittest
import doctest
from unittest import TestSuite

import pipm.commands
import pipm.file

suite = TestSuite()
suite.addTest(doctest.DocTestSuite(pipm.commands))
suite.addTest(doctest.DocTestSuite(pipm.file))

unittest.TextTestRunner(verbosity=2).run(suite)
