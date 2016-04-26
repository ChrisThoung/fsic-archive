# -*- coding: utf-8 -*-
"""
helpers
=======
Variables and functions to provide access to underlying template strings.

"""


import os
from FSIC import __version__ as version


# Model template information
model_path = os.path.join(
    os.path.split(__file__)[0],
    'templates', 'derived.pyt')

with open(model_path, 'rt') as f:
    model = f.read()

model_dict = dict(
    class_name='ModelClass',
    module_name='ModuleName',
    module_description='Placeholder module docstring.',
    version_major=0,
    version_minor=1,
    version_patch=0,
    version_dev=''.__str__(),
    fsic_version="'" + version + "'",
    model_variables=[].__str__(),
    model_convergence_variables=[].__str__(),
    model_equations='pass',
)
model_dict['separator'] = '=' * len(model_dict['module_name'])
