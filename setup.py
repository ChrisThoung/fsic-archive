# -*- coding: utf-8 -*-


from distutils.core import setup


# Version numbering follows the conventions of Semantic Versioning 2.0.0:
# 1. MAJOR - changes with backwards-incompatible modifications to the API
# 2. MINOR - for backwards-compatible additions to functionality
# 3. PATCH - for backwards-compatible bug fixes
# Source: http://semver.org/spec/v2.0.0.html
MAJOR = 0
MINOR = 0
PATCH = 0
VERSION = '%d.%d.%d' % (MAJOR, MINOR, PATCH)


setup(
    name='fsic',
    version=VERSION,
    description='Tools for Stock-Flow Consistent macroeconomic modelling',
    license='BSD',
    author='Chris Thoung',
    author_email='chris.thoung@gmail.com',
    url='https://github.com/cthoung/fsic',
    packages=[
        'fsic',
        'fsic.parser',
        'fsic.parser.tests',
        ],
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
        'Programming Language :: Python :: 3.4',
        'Topic :: Scientific/Engineering',
        ],
    )
