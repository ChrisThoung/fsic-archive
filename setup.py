#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FSIC
====
**FSIC** (Flows and Stocks Integrated Consistently) is a Python package for the
specification, solution and analysis of Stock-Flow Consistent macroeconomic
models in the tradition of Wynne Godley.

"""

import os
from distutils.core import setup


# Read some metadata from FSIC
exec(open(os.path.join('FSIC', 'metadata.py')).read())
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
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    url=URL,
    packages=['FSIC'],
    package_data={'FSIC.templates': [os.path.join('python', '*.txt')]},
    scripts=[os.path.join('scripts', 'fsic.py')],
    platforms='any')
