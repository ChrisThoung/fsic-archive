# -*- coding: utf-8 -*-
"""
os
==
OS-related code.

"""


import os


package_path = os.path.split(os.path.dirname(__file__))[0]
templates = {
    'model': os.path.join('templates', 'derived.pyt'),
    }
