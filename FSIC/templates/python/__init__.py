# -*- coding: utf-8 -*-
"""
python
======
Template Python code for FSIC models.

"""

import os


with open(os.path.join(os.path.dirname(__file__), 'model.txt')) as f:
    MODEL = f.read()

DEFAULT_FIELDS = {
    'name': 'FSICModel',
    'description': 'FSIC model class generated by `FSIC.build_model()`.',
    'docstring': 'FSIC model class.',
    'version': '0.1.0.dev',
    'python_code': 'raise NotImplementedError'}

MAIN_BLOCK = '''

import FSIC.cli.model
parser, handle_args = FSIC.cli.model.make_cli({name})

try:
    from IPython import get_ipython
    _ipython = get_ipython()
except ImportError:
    _ipython = False


if __name__ == '__main__' and not _ipython:
    handle_args(parser.parse_args())
'''
