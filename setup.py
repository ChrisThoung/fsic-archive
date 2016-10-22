#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FSIC
====
**FSIC** is a Python package for macroeconomic modelling.

"""

import os
from setuptools import setup


# Read some metadata from `fsic`
exec(open(os.path.join('fsic', 'metadata.py')).read())
LONG_DESCRIPTION = open('README.md').read()

CLASSIFIERS = [c.strip() for c in '''\
Development Status :: 2 - Pre-Alpha
Environment :: Console
Intended Audience :: Science/Research
License :: OSI Approved :: BSD License
Operating System :: OS Independent
Programming Language :: Python
Programming Language :: Python :: 3
Programming Language :: Python :: 3.3
Programming Language :: Python :: 3.4
Programming Language :: Python :: 3.5
Topic :: Scientific/Engineering
'''.split('\n') if len(c.strip())]


setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    license=LICENSE,
    classifiers=CLASSIFIERS,
    platforms='any',
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    url=URL,
    packages=['fsic',
              'fsic.analysis',
              'fsic.build',
              'fsic.classes',
              'fsic.cli',
              'fsic.io',
              'fsic.parser',
              'fsic.templates',
              'fsic.templates.python', ],
    package_data={
        'fsic.io.tests': [os.path.join('data', '*.csv'), ],
        'fsic.templates': [os.path.join('python', '*.txt'), ],
        'fsic.tests': [os.path.join('data', '*.csv'),
                       os.path.join('data', '*.txt'), ], },
    entry_points={
        'console_scripts': [
            'fsic=fsic.cli.script:interface', ], })
