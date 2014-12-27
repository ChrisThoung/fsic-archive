# -*- coding: utf-8 -*-
"""
___NAME___
___MODULE_DOCSTRING___

___FSIC_VERSION___

"""


import argparse
import os

import numpy as np
from pandas import Period, PeriodIndex
from pandas import Series, DataFrame
import pandas as pd

from FSIC import __version__ as version

from FSIC.model.model import Model
from FSIC.settings import dtype
import FSIC.cli.parsers


# Define ___MODEL___ class
class ___MODEL___(Model):
    """___SHORT_DESCRIPTION___

    ___LONG_DESCRIPTION___

    """

    def __init__(self):
        Model.__init__(self)
        ___MODEL_VERSION___

    def initialise(self, span, solve_from=None, default=0.0):
        """Initialise the model for solution.

        Parameters
        ==========
        span : pandas PeriodIndex object
            The index to set the span of the model (also used to initialise the
            Series objects for the individual variables)
        solve_from : pandas PeriodIndex object or `None`
            The index to set the first period of the model to be solved. This
            may be necessary to supply enough lags for dynamic models
        default : float
            Value to initialise variable Series objects with

        Notes
        =====
        Variable-initialisation statements take the form (using the variable C_d
        as an example):
            self.C_d = Series(default, index=self.span, dtype=np.float64)

        Note that, in the calls below, the value passed as an argument to
        `dtype` is imported from FSIC, to centralise the preferred numeric
        variable type. The `index` argument `self.span` is the same as the
        function argument `span`

        """
        # Store arguments
        self.span = span
        self.solve_from = solve_from
        # Initialise `iter`
        self.iter = Series(default, index=self.span, dtype=dtype)
        # Initialise model variables
        ___INITIALISE___
        # Update solution-state variables
        self.initialised = True
        self.solved = False

    def solve_equations(self, period):
        """Solve the model equations for `period`.

        Parameters
        ==========
        period : Series index
            The identifier of the period to solve

        Notes
        =====
        Equation statements take the form (usng the variable C_s as an example):
            self.C_s[period] = self.C_d[period]

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

        Notes
        =====
        Endogenous variable value-extraction statements take the form (using the
        variable C_d as an example):
            values['C_d'] = self.C_d[period]

        """
        values = {}
        ___GET_ENDOGENOUS_VARIABLE_VALUES___
        return Series(values)

    def get_results(self):
        """Return the results from the model solution.

        Parameters
        ==========
        N/A

        Returns
        =======
        results : DataFrame
            Solution results

        Notes
        =====
        The code to form a results DataFrame takes the following form:
            results = DataFrame({
                'C_d': self.C_d,
                'C_s': self.C_s,})

        """
        ___GET_RESULTS___
        results['iter'] = self.iter
        return results


# Create top-level parser
parser = argparse.ArgumentParser(
    description='___SHORT_DESCRIPTION___',
    fromfile_prefix_chars='@',
    formatter_class=argparse.RawDescriptionHelpFormatter)

model_version = ___MODEL___()
parser.add_argument(
    '-V', '--version',
    action='version',
    version='''\
Model version: %s
Built under FSIC version: %s
FSIC version installed: %s
''' % (model_version.VERSION, model_version.FSIC_BUILD, version))
del model_version

# Add sub-parsers
subparsers = parser.add_subparsers(
    title='commands',
    dest='command')
# 'Solve' sub-parser
subparsers = FSIC.cli.parsers.add_subparser_solve(subparsers)


# Import get_ipython() from IPython as a check for an interactive shell
try:
    from IPython import get_ipython
except ImportError:
    def get_ipython():
        return None


if __name__ == '__main__' and get_ipython() == None:
    # Parse arguments
    args = parser.parse_args()

    if args.command == 'solve':
        # Setup model
        model = ___MODEL___()
        start, end = args.span
        span = PeriodIndex(start=start, end=end)
        model.initialise(span=span, solve_from=Period(args.solve_from))

        if args.input is not None:
            if model.initialised:
                data = model.get_results()
                for i in args.input:
                    if i.endswith('.csv'):
                        data = pd.read_csv(i, dtype=dtype)
                        data = data.fillna(0)
                    else:
                        ext = os.path.splitext(i)[1]
                        raise ValueError(
                            'Unrecognised input file extension: \'%s\''
                            % (ext))
                    # Update data frame index
                    data.index = data['period']
                    del data['period']
                    # Update model data
                    model.update_data(data)

        if args.define:
            parameters = []
            for a in args.define:
                for d in a:
                    d = d.split('=')
                    if len(d) != 2:
                        raise ValueError(
                            'Error in `define` argument: \'%s\'; '
                            'must be a parameter name and value '
                            'separated by an equals sign e.g. W=1' % (d))
                    p, v = d
                    c = 'model.%s.ix[:] = %f' % (p, float(v))
                    parameters.append(c)
            parameters = '\n'.join(parameters)
            exec(parameters)

        if args.set:
            expressions = []
            for a in args.set:
                for x in a:
                    x = 'model.' + x.replace('[', '.ix[')
                    expressions.append(x)
            expressions = '\n'.join(expressions)
            exec(expressions)

        # Solve
        if model.initialised:
            model.solve()

        # Write results
        if args.output is not None:
            if model.initialised:
                results = model.get_results()
                output_files = args.output
                output_files = [o.strip() for o in output_files]
                for o in output_files:
                    if o.endswith('.csv'):
                        results.to_csv(o)
                    else:
                        ext = os.path.splitext(o)[1]
                        raise ValueError(
                            'Unrecognised output file extension: \'%s\''
                            % (ext))
            else:
                raise ValueError(
                    'Model not solved: no results to save')
