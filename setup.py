#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup # NOQA


if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

required = [
    'requests>=1.2.3',
    'python-dateutil>=2.6.0',
]


setup(
    name='heroku3',
    version='3.4.0',
    description='Heroku API Wrapper.',
    long_description=open('README.rst').read() + '\n\n' +
                     open('HISTORY.rst').read(),
    author='Martin Moss',
    author_email='martin_moss@btinternet.com',
    url='https://github.com/martyzz1/heroku3.py',
    download_url='https://github.com/martyzz1/heroku3.py/tarball/v3.4.0',
    packages=['heroku3'],
    package_data={'': ['LICENSE', ]},
    include_package_data=True,
    install_requires=required,
    license='MIT',
    classifiers=(
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ),
)
