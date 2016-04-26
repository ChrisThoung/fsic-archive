# -*- coding: utf-8 -*-
"""
{module_name}
{separator}
{module_description}

"""


import pandas as pd
pd.options.mode.chained_assignment = None

from FSIC import Model


class {class_name}(Model):
    MAJOR = {version_major}
    MINOR = {version_minor}
    PATCH = {version_patch}
    DEV = {version_dev}
    VERSION = '.'.join(str(i) for i in [MAJOR, MINOR, PATCH]) + DEV
    FSIC_VERSION = {fsic_version}

    variables = {model_variables}
    convergence_variables = {model_convergence_variables}

    def initialise(self, *args, **kwargs):
        self._initialise(
            {class_name}.variables,
            *args,
            convergence_variables={class_name}.convergence_variables,
            **kwargs)

    def solve_system(self, period):
        {model_equations}
