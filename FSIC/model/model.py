# -*- coding: utf-8 -*-
"""
Model
=====
Core FSIC class to solve a macroeconomic model. Stock-Flow Consistent models
are implemented as derived classes from this one.

"""


from pandas import PeriodIndex
from pandas import Series


class Model:
    """Base class for FSIC models."""

    def __init__(self):
        self.initialised = False
        self.solved = False

    def read_data(self, path):
        """Read and store the contents of the file in `path`.

        Parameters
        ==========
        path : string
            Location of data file

        Returns
        =======
        N/A

        """
        from FSIC.io.read import read
        data = read(path)
        for frame in data:
            self.update_data(frame)

    def update_data(self, data):
        """Store the contents of `data`.

        Parameters
        ==========
        data : pandas DataFrame
            Data to store; one column per variable, with name matching that of
            the intended model variable

        Returns
        =======
        N/A

        Notes
        =====
        The index of the DataFrame must match the index of the model
        variables. It is not necessary for all periods in the model to be
        covered by the DataFrame index.

        See also
        ========
        FSIC.parser.code.translate()

        """
        # Generate a set of statements for execution
        from FSIC.parser.code import translate
        expression = []
        for c in data.columns:
            # Translate the statement into one compatible with the model class
            e = ''.join([
                translate(c, period='') + '[data.index]',
                ' = data[\'', c, '\']'])
            e = e.replace('[]', '')
            expression.append(e)
        # Combine into a single string and call
        expression = '\n'.join(expression)
        exec(expression)

    def solve(self, start=None, end=None, max_iter=100, min_iter=0, tol=1.0e-8):
        """Solve the model.

        Parameters
        ==========
        start : Series index
            First period to solve. If `None`:
             - If `self.solve_from` is also `None`, solve from the first period
               in `self.span`
             - If `self.solve_from` is not `None`, solve from `self.solve_from`
        end : Series index
            Last period to solve. If `None`:
             - If `self.solve_to` is also `None`, solve to the last period in
               `self.span`
             - If `self.solve_to` is not `None`, solve to `self.solve_to`
        max_iter : integer
            The maximum number of iterations to solve over
        min_iter : integer
            The minimum number of iterations to solve over
        tol : float
            Tolerance to check convergence, using the sum of the squared
            differences between iterations of the endogenous variables

        See also
        ========
        solve_period() : user-defined function in derived class

        """
        # Check for initialisation
        if not self.initialised:
            raise ValueError('Model not yet initialised: call `initialise()`')
        # Set start and end periods
        if start is None:
            if self.solve_from is None:
                start = min(self.span)
            else:
                start = self.solve_from
        if end is None:
            if self.solve_to is None:
                end = max(self.span)
            else:
                end = self.solve_to
        # Solve
        for period in PeriodIndex(start=start, end=end):
            self.solve_period(
                period=period,
                max_iter=max_iter,
                min_iter=min_iter,
                tol=tol)
        # Update solution state
        self.solved = True

    def solve_period(self, period, max_iter=100, min_iter=0, tol=1.0e-8):
        """Solve for the current period.

        Parameters
        ==========
        period : Series index
            The identifier of the period to solve
        max_iter : integer
            The maximum number of iterations to solve over
        min_iter : integer
            The minimum number of iterations to solve over
        tol : float
            Tolerance to check convergence, using the sum of the squared
            differences between iterations of the endogenous variables

        """
        for i in range(max_iter):
            # Solve model equations
            before = self.get_endogenous_variable_values(period)
            self.solve_equations(period)
            after = self.get_endogenous_variable_values(period)
            # Test for convergence
            diff = (after - before).apply(lambda x: x * x)
            diff = diff.sum()
            if diff < tol and (i + 1) >= min_iter:
                num_iter = i + 1
                break
        else:
            num_iter = None
        self.iter[period] = num_iter
