# -*- coding: utf-8 -*-
"""
python
======
Template Python code for FSIC models.

"""

import os


with open(os.path.join(os.path.dirname(__file__), 'model.txt')) as f:
    MODEL = f.read()

DEFAULT_CONTENTS = {
    'name': 'FSICModel',
    'description': 'FSIC model class generated by `FSIC.build_model()`.',
    'docstring': 'FSIC model class.',
    'version': '0.1.0.dev',
    'python_code': 'raise NotImplementedError'}
