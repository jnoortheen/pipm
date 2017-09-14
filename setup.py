import codecs
import os
import re
import sys

from setuptools import setup, find_packages

import pipm

here = os.path.abspath(os.path.dirname(__file__))


def read(*parts):
    # intentionally *not* adding an encoding option to open, See:
    #   https://github.com/pypa/virtualenv/issues/201#issuecomment-3145690
    return codecs.open(os.path.join(here, *parts), 'r').read()


tests_require = read('test-requirements.txt').splitlines()[1:]

setup(
    name="pipm",
    version=pipm.__version__,
    description="Wrapper around pip commands to auto save/delete requirements",
    long_description=read('README'),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Topic :: Software Development :: Build Tools",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: Implementation :: PyPy"
    ],
    keywords='easy_install distutils setuptools egg virtualenv requirements',
    author='noortheen',
    author_email='jnoortheen@gmail.com',
    url='https://github.com/jnoortheen/pipm',
    license='MIT',
    packages=find_packages(
        exclude=["tests*", ],
    ),
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "pipm=pipm:main",
        ],
    },
    tests_require=tests_require,
    python_requires='>=2.7,!=3.0.*,!=3.1.*,!=3.2.*',
    extras_require={
        'testing': tests_require,
    },
)
