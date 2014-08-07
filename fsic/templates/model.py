# -*- coding: utf-8 -*-
"""
___NAME___
___MODULE_DOCSTRING___

"""


import argparse

import numpy as np
from pandas import Series, DataFrame

from fsic import __version__ as version

from fsic.model.model import Model


try:
    from IPython import get_ipython
except:
    def get_ipython():
        return None


class ___MODEL___(Model):
    """___SHORT_DESCRIPTION___

    ___LONG_DESCRIPTION___

    """

    def initialise(self, span, default=0):
        """Initialise the model for solution.

        Parameters
        ==========
        span : list
            The index to set the span of the model (used as the index for
            individual variable Series objects)
        default : float
            Value to initialise variable Series objects with

        """
        ___INITIALISE___

    def solve_equations(self, period):
        """Solve the model equations for `period`.

        Parameters
        ==========
        period : Series index
            The identifier of the period to solve

        """
        ___SOLVE_EQUATIONS___

    def get_endogenous_variable_values(self, period):
        """Return the current values of the endogenous variables.

        Parameters
        ==========
        period : Series index
            The identifier of the period to solve

        Returns
        =======
        values : pandas Series
            Endogenous variable values for the current `period`

        """
        ___GET_ENDOGENOUS_VARIABLE_VALUES___

    def get_results(self):
        """Return the results from the model solution.

        Parameters
        ==========
        N/A

        Returns
        =======
        results : DataFrame
            Solution results

        """
        ___GET_RESULTS___


parser = argparse.ArgumentParser(
    description='___SHORT_DESCRIPTION___.',
    fromfile_prefix_chars='@')
parser.add_argument(
    '-V', '--version',
    action='version',
    version=version)

parser.add_argument(
    '-o', '--output',
    nargs='+',
    metavar='OUTPUT',
    default=None,
    type=str,
    required=False,
    help='list of output files for model results')


if __name__ == '__main__' and get_ipython() == None:
    args = parser.parse_args()
