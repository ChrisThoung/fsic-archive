# -*- coding: utf-8 -*-


import os
from distutils.core import setup


# Version numbering follows the conventions of Semantic Versioning 2.0.0:
# 1. MAJOR - changes with backwards-incompatible modifications to the API
# 2. MINOR - for backwards-compatible additions to functionality
# 3. PATCH - for backwards-compatible bug fixes
# Source: http://semver.org/spec/v2.0.0.html
MAJOR = 0
MINOR = 1
PATCH = 0
for_release = False

VERSION = '%d.%d.%d' % (MAJOR, MINOR, PATCH)
if not for_release:
    VERSION += '.dev'

# Write package version.py
with open(os.path.join('FSIC', 'version.py'), 'wt') as f:
    version_to_write = '''\
# -*- coding: utf-8 -*-


MAJOR = %d
MINOR = %d
PATCH = %d
DEV = %s
VERSION = \'%d.%d.%d'''
    if for_release:
        in_development = 'False'
    else:
        in_development = 'True'
        version_to_write += '.dev'
    version_to_write += '\'\n'
    f.write(version_to_write % (MAJOR, MINOR, PATCH, in_development,
                                MAJOR, MINOR, PATCH))

# Write other package settings
with open(os.path.join('FSIC', 'settings.py'), 'wt') as f:
    f.write('''\
# -*- coding: utf-8 -*-


import numpy as np


dtype = np.float64
''')

# Call setup()
setup(
    name='FSIC',
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
        'FSIC',
        'FSIC.cli',
        'FSIC.cli.tests',
        'FSIC.io',
        'FSIC.io.tests',
        'FSIC.model',
        'FSIC.model.tests',
        'FSIC.optimise',
        'FSIC.optimise.tests',
        'FSIC.parser',
        'FSIC.parser.tests',
        'FSIC.tools',
        'FSIC.tools.tests',
        'FSIC.utilities',
        'FSIC.utilities.tests',
        ],
    package_data={
        'FSIC': ['templates/*.py'],
        'FSIC.io.tests': ['data/*.csv', 'data/*.tsv'],
        'FSIC.model.tests': ['data/*.*'],
        },
    scripts=[
        'scripts/fsic.py',
        ],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Console',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Scientific/Engineering',
        ],
    platforms=['Any'],
    )
