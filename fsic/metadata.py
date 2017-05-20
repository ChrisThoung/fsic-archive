# -*- coding: utf-8 -*-
"""
version
=======
FSIC version numbering follows the conventions of Semantic Versioning 2.0.0:
 - MAJOR: changes with backwards-incompatible modifications to the API
 - MINOR: for backwards-compatible additions to functionality
 - PATCH: for backwards-compatible bug fixes

Source: http://semver.org/spec/v2.0.0.html

"""

NAME = 'fsic'

MAJOR = 0
MINOR = 2
PATCH = 0
DEV = True

VERSION = '{}.{}.{}'.format(MAJOR, MINOR, PATCH)
if DEV:
    VERSION += '.dev'

DESCRIPTION = 'Tools for macroeconomic modelling'

LICENSE = 'BSD'

AUTHOR = 'Chris Thoung'
AUTHOR_EMAIL = 'chris.thoung@gmail.com'
URL = 'https://github.com/ChrisThoung/fsic'

COPYRIGHT = '2014-17, Chris Thoung'