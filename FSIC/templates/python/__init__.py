# -*- coding: utf-8 -*-
"""
python
======
Template Python code for FSIC models.

"""

import os


with open(os.path.join(os.path.dirname(__file__), 'model.txt')) as f:
    MODEL = f.read()
