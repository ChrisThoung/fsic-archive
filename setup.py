# -*- coding: utf-8 -*-


import os
from distutils.core import setup


# Version numbering follows the conventions of Semantic Versioning 2.0.0:
# 1. MAJOR - changes with backwards-incompatible modifications to the API
# 2. MINOR - for backwards-compatible additions to functionality
# 3. PATCH - for backwards-compatible bug fixes
# Source: http://semver.org/spec/v2.0.0.html
MAJOR = 0
MINOR = 0
PATCH = 0
for_release = False

VERSION = '%d.%d.%d' % (MAJOR, MINOR, PATCH)
if not for_release:
    VERSION += '.dev'

# Write package version.py
with open(os.path.join('fsic', 'version.py'), 'wt') as f:
    version_to_write = """\
MAJOR = '%d'
MINOR = '%d'
PATCH = '%d'
VERSION = '%d.%d.%d"""
    if not for_release:
        version_to_write += '.dev'
    version_to_write += '\''
    f.write(version_to_write % (MAJOR, MINOR, PATCH, MAJOR, MINOR, PATCH))

# Call setup()
setup(
    name='fsic',
    version=VERSION,
    description='Tools for Stock-Flow Consistent macroeconomic modelling',
    long_description='''
FSIC
====
**FSIC** (Flows and Stocks Integrated Consistently) is a Python package for the
specification, solution and analysis of Stock-Flow Consistent macroeconomic
models in the tradition of Wynne Godley.
''',
    license='BSD',
    author='Chris Thoung',
    author_email='chris.thoung@gmail.com',
    url='https://github.com/cthoung/fsic',
    packages=[
        'fsic',
        'fsic.model',
        'fsic.optimise',
        'fsic.optimise.tests',
        'fsic.parser',
        'fsic.parser.tests',
        'fsic.tools',
        'fsic.tools.tests',
        'fsic.utilities',
        'fsic.utilities.tests',
        ],
    package_data={
        'fsic': ['templates/*.py'],
        },
    scripts=[
        'scripts/fsic-build.py',
        ],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Console',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Scientific/Engineering',
        ],
    platforms=['Any'],
    )
