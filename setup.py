#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup  # NOQA


if sys.argv[-1] == "publish":
    os.system("python setup.py sdist upload")
    sys.exit()

required = [
    "requests>=1.2.3",
    "python-dateutil>=2.6.0",
]


def get_version(*file_paths):
    """Retrieves the version from dj_snap_utils/__init__.py"""
    filename = os.path.join(os.path.dirname(__file__), *file_paths)
    version_file = open(filename).read()
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


version = get_version("heroku3", "__init__.py")


setup(
    name="heroku3",
    version=version,
    description="Heroku API Wrapper.",
    long_description=open("README.rst").read() + "\n\n" + open("HISTORY.rst").read(),
    long_description_content_type="text/x-rst",
    author="Martin Moss",
    author_email="martin_moss@btinternet.com",
    url="https://github.com/martyzz1/heroku3.py",
    download_url="https://github.com/martyzz1/heroku3.py/tarball/v4.0.3",
    packages=["heroku3"],
    package_data={"": ["LICENSE",]},
    include_package_data=True,
    install_requires=required,
    license="MIT",
    classifiers=(
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
    ),
)
