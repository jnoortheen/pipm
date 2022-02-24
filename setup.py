import codecs
import os
import json

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))


def get_version():
    cz_conf = os.path.join(here, ".cz.json")
    with open(cz_conf) as fr:
        config = json.loads(fr.read())
        return config["commitizen"]["version"]


def read(*parts):
    # intentionally *not* adding an encoding option to open, See:
    #   https://github.com/pypa/virtualenv/issues/201#issuecomment-3145690
    return codecs.open(os.path.join(here, *parts), "r").read()


setup(
    name="pipm",
    version=get_version(),
    description="Wrapper around pip commands to auto-update requirements file",
    long_description="Checkout the README https://github.com/jnoortheen/pipm",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Topic :: Software Development :: Build Tools",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: Implementation :: PyPy",
    ],
    keywords="easy_install distutils setuptools egg virtualenv requirements",
    author="noortheen",
    author_email="jnoortheen@gmail.com",
    url="https://github.com/jnoortheen/pipm",
    homepage="https://github.com/jnoortheen/pipm",
    license="MIT",
    packages=find_packages(exclude=["tests*"]),
    include_package_data=True,
    entry_points={"console_scripts": ["pipm=pipm.__main__:main"]},
    python_requires="!=3.0.*,!=3.1.*,!=3.2.*",
    # tests_require=tests_require,
    install_requires=["pip>=20.1", 'typing;python_version<"3.6"']
    # extras_require={
    #     'testing': tests_require,
    # },
)
