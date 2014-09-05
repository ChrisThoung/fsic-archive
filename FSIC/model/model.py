# -*- coding: utf-8 -*-
"""
Model
=====
Core FSIC class to solve a macroeconomic model. Stock-Flow Consistent models
are implemented as derived classes from this one.

"""


from pandas import Series


class Model:
    """Base class for FSIC models."""

    def __init__(self):
        self.initialised = False
        self.solved = False

    def solve(self, start=None, end=None, max_iter=100, min_iter=0, tol=1.0e-8):
        """Solve the model.

        Parameters
        ==========
        start : Series index
            First period to solve (set to be the first period of `self.span` if
            equal to None)
        end : Series index
            Last period to solve (set to be the last period in `self.span` if
            equal to None)
        max_iter : integer
            The maximum number of iterations to solve over
        min_iter : integer
            The minimum number of iterations to solve over
        tol : float
            Tolerance to check convergence, based on the sum of squared
            differences between the endogenous variables between iterations

        See also
        ========
        solve_period()

        """
        # Check for initialisation
        if not self.initialised:
            raise ValueError('Model not yet initialised: call `initialise()`')
        # Set start and end periods
        if start is None:
            start = self.span[0]
        if end is None:
            end = self.span[-1]
        # Index start and end periods
        start = self.full_span.index(start)
        end = self.full_span.index(end)
        # Solve
        for i in range(start, end + 1):
            period = self.full_span[i]
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
            Tolerance to check convergence, based on the sum of squared
            differences between the endogenous variables between iterations

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
