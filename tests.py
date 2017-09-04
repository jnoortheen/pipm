import unittest
import doctest
import pipm

def load_tests(loader, tests, ignore):
    tests.addTests(doctest.DocTestSuite(pipm))
    return tests
