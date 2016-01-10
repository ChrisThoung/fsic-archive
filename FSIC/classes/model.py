# -*- coding: utf-8 -*-
"""
model
=====
Defines the Model class, a base class for FSIC models. Macroeconomic models are
implemented as derived classes of this one.

"""


from pandas import DataFrame
from pandas import Period, PeriodIndex


class Model(object):
    """Base class for FSIC models.

    The derived class must include the following functions:
     - solve_system(self, period)

    """

    def __init__(self):
        self.solve_from = None
        self.solve_to = None
        self.data = None
        self.convergence_variables = None

    def _initialise(self, variables, start, end, solve_from=None, solve_to=None, convergence_variables=None, default=0.0):
        # Generate DataFrame index: use pandas PeriodIndex if possible
        try:
            index = PeriodIndex(start=Period(start), end=Period(end))
        except ValueError:
            index = range(start, end + 1)
        # Similarly, convert solve_{from,to} to pandas Period objects
        try:
            solve_from = Period(solve_from)
            solve_to = Period(solve_to)
        except ValueError:
            pass
        self.solve_from = solve_from
        self.solve_to = solve_to
        # Initialise the DataFrame
        if not isinstance(variables, dict):
            variables = {v: default for v in variables}
        self.data = DataFrame(variables, index=index)
        self.data['iter'] = 0
        self.data['conv'] = 0
        # Store convergence variables
        if convergence_variables is None:
            self.convergence_variables = list(variables.keys())
        else:
            self.convergence_variables = convergence_variables
        # Initialise Series views on DataFrame
        for v in self.data.columns:
            exec('self.{var} = self.data["{var}"]'.format(var=v))

    def solve(self, start=None, end=None, **kwargs):
        # Use default values if no start or end arguments
        if start is None:
            if self.solve_from is None:
                start = min(self.data.index)
            else:
                start = self.solve_from
        if end is None:
            if self.solve_to is None:
                end = max(self.data.index)
            else:
                end = self.solve_to
        # Generate solution span: use pandas PeriodIndex is possible
        try:
            span = PeriodIndex(start=Period(start), end=Period(end))
        except ValueError:
            span = range(start, end + 1)
        # Solve period by period
        for period in span:
            self.solve_period(period, **kwargs)

    def solve_period(self, period, max_iter=100, min_iter=0, tol=1.0e-8):
        # Prefer a pandas Period object if possible
        try:
            period = Period(period)
        except ValueError:
            pass
        # Solve to convergence
        converged = 0
        for i in range(max_iter):
            before = self.data.ix[period, self.convergence_variables]
            self.solve_system(period)
            after = self.data.ix[period, self.convergence_variables]
            if i > min_iter:
                sum_sq_diffs = ((after - before) ** 2).sum()
                if sum_sq_diffs < tol:
                    converged = 1
                    break
        # Store iteration and convergence results
        self.iter[period] = i + 1
        self.conv[period] = converged
