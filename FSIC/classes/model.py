# -*- coding: utf-8 -*-
"""
model
=====
Base `Model` class for `FSIC` models.

"""

import sys

import numpy as np

from pandas import Index, Period, PeriodIndex
from pandas import Series, DataFrame

import pandas as pd
pd.set_option('mode.chained_assignment', None)

from FSIC.exceptions import FSICError
from FSIC.functions import indicator_types, indicator_matrix
from FSIC.utilities import locate_in_index


class Model(object):
    """FSIC base class for economic models.

    Attributes
    ----------
    variables : list; `None` at instantiation
        The list of variables that make up the model
        Defaults to `VARIABLES` on call to `initialise()`
    parameters : list; `None` at instantiation
        The list of parameter variables in the model
        Defaults to `PARAMETERS` on call to `initialise()`
    errors : list; `None` at instantiation
        The list of equation error variables in the model
        Defaults to `ERRORS` on call to `initialise()`
    convergence_variables : list; `None` at instantiation
        The list of variables to check for convergence when solving the
        model
        Defaults to `CONVERGENCE_VARIABLES` on call to `initialise()`
    start_offset, end_offset : int; `None` at instantiation
        Number of periods at the start and end of the solution span to skip
        when solving the model (typically to account for leads and lags, but
        available as a user option)
        Default to `START_OFFSET` and `END_OFFSET` on call to `initialise()`
    data : `pandas` `DataFrame`; `None` at instantiation
        Model database, with:
         - index: time (periods, whether as integer `Index`
                  or `pandas` `PeriodIndex`)
         - columns: (typically) the elements in `variables`, `parameters` and
                    `errors` (if not already in `variables`) plus:

                     - 'status' (str, initialised to '-') :
                           solution information for each period
                     - 'iterations' (int, initialised to -1) :
                           number of iterations during solution
                     - 'converged' (bool, initialised to `False`) :
                           whether the solution converged for that period or
                           not

    """

    VARIABLES = None
    PARAMETERS = None
    AUTOMATIC = None
    ERRORS = None

    CONVERGENCE_VARIABLES = None

    START_OFFSET = 0
    END_OFFSET = 0

    VERSION = '0.1.0.dev'


    def __init__(self, *args, **kwargs):
        self.variables = None
        self.parameters = None
        self.automatic = None
        self.errors = None

        self.convergence_variables = None

        self.start_offset = None
        self.end_offset = None

        self.data = None

        # Default to Python Gauss-Seidel solver
        self._solver = self._solver_gauss_seidel_python

        if len(args) or len(kwargs):
            self.initialise(*args, **kwargs)


    def initialise(self,
                   start=None, end=None,
                   solve_from=None, solve_to=None,
                   index=None,
                   data=None,
                   variables=None, parameters=None, automatic=None, errors=None,
                   convergence_variables=None,
                   default_value=0.0,
                   exceptions='ignore') -> None:
        """Initialise the model variable, `self.data`, for solution.

        Parameters
        ----------
        start : int or valid argument to `pandas` `Period` class,
                default `None`
            The first period in the index, if passed. Has precedence over all
            other arguments relating to the start period
        end : int or valid argument to `pandas` `Period` class,
              default `None`
            The last period in the index, if passed. Has precedence over all
            other arguments relating to the end period

        solve_from : int or valid argument to `pandas` `Period` class,
                     default `None`
            The first period for solution, if passed. This may differ from the
            intended start period of the index, owing to lagged variables or if
            the user wants to restrict the period of solution. If set, and
            `start` is not set, then the start period of the index will be:
              `solve_from` - `self.START_OFFSET`
        solve_to : int or valid argument to `pandas` `Period` class,
                   default `None`
            The last period for solution, if passed. This may differ from the
            intended last period of the index, owing to leading variables or if
            the user wants to restrict the period of solution. If set, and
            `end` is not set, then the end period of the final index will be:
              `solve_to` + `self.END_OFFSET`

        index : `pandas` index-like (including a list)
            Object to use as the index. Has precedence over `solve_from` and
            `solve_to` if the span of this variable encompasses the implied
            start and end periods. Also provides the means to pass a non-time
            index (provided that the model is not dynamic; the class will
            throw an exception if this is not the case)

        data : `pandas` `Series` or `DataFrame` object, default `None`
            Object to use to form the final index, if passed. Has precedence
            over `solve_from` and `solve_to` if the index of `data` encompasses
            the implied start or end periods.

        variables : list of strings, default `None`
            Variables to include in the columns of `self.data`. If `None`,
            default to `VARIABLES`. Final DataFrame columns consist of the
            union of `variables`, `parameters` and `errors`, plus 'iterations',
            'converged' and 'status'
        parameters : list of strings, default `None`
            Parameter variables of the model. If `None`, default to
            `PARAMETERS`. Final DataFrame columns consist of the union of
            `variables`, `parameters` and `errors`, plus 'iterations',
            'converged' and 'status'
        automatic : list of strings, default `None`
            Variables to generate automatically, for example, dummy and step
            variables, and time trends.
        errors : list of strings, default `None`
            Error variables of the model. If `None`, default to `ERRORS`. Final
            DataFrame columns consist of the union of `variables`, `parameters`
            and `errors`, plus 'iterations', 'converged' and 'status'

        convergence_variables : list of strings, default `None`
            List of variables to check for convergence during solution. If
            `None`, default to `CONVERGENCE_VARIABLES`. If
            `CONVERGENCE_VARIABLES` is `None`, use `variables` instead

        default_value : numeric
            Default fill value for new `DataFrame` (if not in `data`, if
            supplied)

        exceptions : str {'strict', 'ignore', }, default 'ignore'
            Stringency of error handling. If:
             - 'strict': throw an exception if any automatic variables cannot
                         be created
             - 'ignore': set to zero any variables that cannot be created

        Notes
        -----
        This method initialises:
         - `self.data` (`DataFrame`) :
               The model database, with additional columns 'status',
               'iterations' and 'converged'
         - `self.start_offset`, `self.end_offset` (int) :
               The number of periods at the start and end to skip by default
               during solution (typically to account for leads and lags)
         - `self.variables`, `self.parameters`, `self.errors` (list) :
               The lists of variables that comprise the model (whether set by
               default from the class definition, or as arguments to this
               method)
         - `self.convergence_variables` (list) :
               The list of variables to check for convergence during solution

        The initialisation of `self.data` is as follows:
         - rows (index): assembled from `start`, `end`, `solve_from`,
                         `solve_to` and `data` (see `_make_index()` for
                         details)
         - columns: where supplied, the union of `variables`, `parameters`,
                    `errors`, the columns of `data`, `automatic` and
                    `['status', 'iterations', 'converged']` ; `VARIABLES`,
                    `PARAMETERS`, `ERRORS` and `AUTOMATIC` otherwise. Automatic
                    variables are initialised separately to the other variables

        The order of assignment of the list of convergence variables
        (`self.convergence_variables`) is:
         - `convergence_variables`, if passed
         - `CONVERGENCE_VARIABLES`, if not `None`
         - `self.variables` otherwise

        """
        # Make `DataFrame` index and find offsets
        if index is None:
            index = self._make_index(start, end,
                                     solve_from, solve_to,
                                     data)
            if solve_from:
                self.start_offset = locate_in_index(index, solve_from)
            else:
                self.start_offset = self.START_OFFSET

            if solve_to:
                self.end_offset = (len(index) - 1) - locate_in_index(index, solve_to)
            else:
                self.end_offset = self.END_OFFSET
        else:
            try:
                self._make_index(index[0], index[-1],
                                 solve_from, solve_to,
                                 data)
            except ValueError:
                if self.START_OFFSET != 0 or self.END_OFFSET != 0:
                    raise FSICError('`index` argument is a non-time index, '
                                    'but model offsets ({}, {}) '
                                    'suggest a dynamic model'.format(
                                        self.START_OFFSET, self.END_OFFSET))

        # Form combined list of variables, using class attributes as defaults
        def assign_or_use_default(arg, default):
            """Return default (or empty list) if `arg` not set."""
            if arg is not None:
                return arg
            else:
                return default or []

        self.variables = assign_or_use_default(variables, self.VARIABLES)
        self.parameters = assign_or_use_default(parameters, self.PARAMETERS)
        self.errors = assign_or_use_default(errors, self.ERRORS)

        columns = []
        for item in self.variables + self.parameters + self.errors:
            if item not in columns:
                columns.append(item)

        # Form model `DataFrame`
        if data is not None:
            # Match index types
            if type(data.index) != type(index):
                assert type(index) is PeriodIndex
                data.index = self._make_index(start=data.index[0],
                                              end=data.index[-1])
                assert type(data.index) is PeriodIndex
            # Preserve all columns in `data`, even if not in the list of model
            # variables
            for col in data.columns:
                if col not in columns:
                    columns.append(col)
            self.data = data.reindex(index=index, columns=columns,
                                     fill_value=default_value)
        else:
            self.data = DataFrame(default_value,
                                  index=index, columns=columns)

        # Add automatic variables
        self.automatic = assign_or_use_default(automatic, self.AUTOMATIC)
        if len(self.automatic):
            automatic_variables = set(self.automatic)
            for kind in indicator_types:
                indicators = indicator_matrix(self.data.index, kind=kind)
                match = automatic_variables.intersection(set(indicators.columns))
                if len(match):
                    for v in match:
                        self.data[v] = indicators[v].copy()
                    automatic_variables = automatic_variables.difference(match)
            if len(automatic_variables):
                if exceptions == 'strict':
                    raise FSICError('Unable to create the following automatic variables: {}'
                                    .format(', '.join(list(automatic_variables))))
                elif exceptions == 'ignore':
                    for v in automatic_variables:
                        self.data[v] = 0.0

        # Initialise columns to store solution information
        self.data['status'] = Series('-', index=index)
        self.data['iterations'] = Series(-1, index=index, dtype=int)
        self.data['converged'] = Series(False, index=index, dtype=bool)

        # Store list of variables to test for convergence
        if convergence_variables:
            self.convergence_variables = convergence_variables
        else:
            if self.CONVERGENCE_VARIABLES:
                self.convergence_variables = self.CONVERGENCE_VARIABLES
            else:
                self.convergence_variables = self.variables

        # Generate properties for individual `DataFrame` columns
        for variable in self.data.columns:
            setattr(self.__class__, variable, self._make_property(variable))

    def _make_index(self,
                    start=None, end=None,
                    solve_from=None, solve_to=None,
                    data=None):
        """Make a `pandas` index object from the arguments.

        Parameters
        ----------
        start : int or valid argument to `pandas` `Period` class,
                default `None`
            The first period in the index, if passed. Has precedence over all
            other arguments relating to the start period
        end : int or valid argument to `pandas` `Period` class,
              default `None`
            The last period in the index, if passed. Has precedence over all
            other arguments relating to the end period

        solve_from : int or valid argument to `pandas` `Period` class,
                     default `None`
            The first period for solution, if passed. This may differ from the
            intended start period of the index, owing to lagged variables or if
            the user wants to restrict the period of solution. If set, and
            `start` is not set, then the start period of the index will be:
              `solve_from` - `self.START_OFFSET`
        solve_to : int or valid argument to `pandas` `Period` class,
                   default `None`
            The last period for solution, if passed. This may differ from the
            intended last period of the index, owing to leading variables or if
            the user wants to restrict the period of solution. If set, and
            `end` is not set, then the end period of the final index will be:
              `solve_to` + `self.END_OFFSET`

        data : `pandas` `Series` or `DataFrame` object, default `None`
            Object to use to form the final index, if passed. Has precedence
            over `solve_from` and `solve_to` if the index of `data` encompasses
            the implied start or end periods.

        Returns
        -------
        index : `pandas` `PeriodIndex` or `Index` object
            Prefer `PeriodIndex`, switching to `Index` if elements can be
            coerced to integers and at least some are non-positive

        Examples
        --------
        # Setup
        >>> from FSIC import Model
        >>> class Derived(Model):
        ...     START_OFFSET = 2
        ...     END_OFFSET = 1
        >>> test = Derived()

        # Annual `PeriodIndex`
        >>> test._make_index(2000, 2005)
        PeriodIndex(['2000', '2001', '2002', '2003', '2004', '2005'], dtype='int64', freq='A-DEC')

        # `RangeIndex` (for indexes with non-positive numbers)
        >>> test._make_index(-2, 2)
        RangeIndex(start=-2, stop=3, step=1)

        # Quarterly `PeriodIndex` with automatic accounting for offsets
        >>> test._make_index(solve_from='2000Q1', solve_to='2000Q4')
        PeriodIndex(['1999Q3', '1999Q4', '2000Q1', '2000Q2', '2000Q3', '2000Q4',
                     '2001Q1'],
                    dtype='int64', freq='Q-DEC')

        # Mix of first four arguments
        >>> test._make_index(start=2000, solve_to=2004)
        PeriodIndex(['2000', '2001', '2002', '2003', '2004', '2005'], dtype='int64', freq='A-DEC')

        >>> test._make_index(solve_from=2002, end=2005)
        PeriodIndex(['2000', '2001', '2002', '2003', '2004', '2005'], dtype='int64', freq='A-DEC')

        # With `data` argument
        >>> from pandas import DataFrame
        >>> df = DataFrame(0, index=range(5), columns=list('ABCDEFG'))

        >>> test._make_index(data=df)
        RangeIndex(start=0, stop=5, step=1)

        >>> test._make_index(start=2, data=df)
        RangeIndex(start=2, stop=5, step=1)

        >>> test._make_index(solve_from=1, data=df)
        RangeIndex(start=-1, stop=5, step=1)

        >>> test._make_index(solve_to=2, data=df)
        RangeIndex(start=0, stop=5, step=1)

        """
        if start is not None:
            pass
        elif solve_from is not None:
            try:
                solve_from = Period(solve_from)
            except ValueError:
                solve_from = int(solve_from)
            start = solve_from - self.START_OFFSET

            if data is not None:
                try:
                    start = min(start, data.index[0])
                except TypeError:
                    start = min(start, Period(data.index[0]))

        elif data is not None:
            start = data.index[0]
        else:
            raise ValueError('Must provide a start period, '
                             'either explicitly '
                             '(`start` or the index of `data`) '
                             'or implicitly (`solve_from`)')
        if end is not None:
            pass
        elif solve_to is not None:
            try:
                solve_to = Period(solve_to)
            except ValueError:
                solve_to = int(solve_to)
            end = solve_to + self.END_OFFSET

            if data is not None:
                end = max(end, data.index[-1])

        elif data is not None:
            end = data.index[-1]
        else:
            raise ValueError('Must provide an end period, '
                             'either explicitly '
                             '(`end` or the index of `data`) '
                             'or implicitly (`solve_to`)')
        try:
            index = PeriodIndex(start=start, end=end)
        except ValueError:
            start = int(str(start))
            end = int(str(end))
            index = Index(range(start, end + 1))
        return index

    def _make_property(self, name):
        """Return a property attribute for the column `name`.

        Parameter
        ---------
        name : str
            The name of the column in `self.data` to generate a property for

        Returns
        -------
        : property attribute
            Properties to manage the attribute for `name`

        Notes
        -----
        Property attributes for the variables in `self.data` are useful to:
         - ease variable assignment in Python scripts by avoiding references to
           `self.data`
         - prevent accidental variable (rather than value) replacement or
           deletion

        For some object instance `model` with variable with name 'G', the
        property attribute allows for statements like:

        # Assign a value of 20 to 'G' in all periods (rather than setting
        # `model.G` to an integer with value 20)
        >>> model.G = 20

        # Throw an exception on an attempt to delete 'G'
        >>> del model.G
        RuntimeError: Cannot delete a model variable after initialisation

        """
        def getter(self):
            return self.data[name]

        def setter(self, value):
            self.data[name].ix[:] = value

        def deleter(self):
            raise RuntimeError('Cannot delete a model variable '
                               'after initialisation')

        return property(fget=getter, fset=setter, fdel=deleter, doc=None)


    def solve(self,
              first=None, last=None, single=None,
              min_iter=0, max_iter=100, tol=1e-06,
              verbosity=0,
              **kwargs) -> None:
        """Solve the model for one or more periods.

        Parameters
        ----------
        first, last : int or valid arguments to `pandas` `Period` class,
                      default `None`
            Specify the *range* of periods to solve, beginning with `first` and
            ending with `last` (inclusive). If either is `None` (and `single`
            is also `None`), use the periods implied by `self.start_offset` and
            `self.end_offset`, respectively

        single : int or valid arguments to `pandas` `Period` class,
                 default `None`
            Specify a single period to solve. Is mutually exclusive with
            `first` and `last` (both *must* be `None`, if `single` is not
            `None`)

        min_iter, max_iter : int, defaults 0 and 100
            The minimum and maximum number of iterations per period when
            attempting to solve the model:
             - if the model solves in fewer than `min_iter` iterations, there
               will be additional iterations up to `min_iter`
             - if the model does not converge within `max_iter` iterations,
               solution for that period will stop and the period will be
               recorded as a failed convergence
        tol : float, default 1e-06
            Error tolerance to check convergence during solution each period,
            based on the sum of the squared differences between iterations for
            the variables in `self.convergence_variables`

        verbosity : int, default 0
            The level of detail to report on solution progress. Prints no
            output if zero; higher values report progressively more detail

        kwargs : arguments to pass to solver function

        """
        if self.data is None:
            raise RuntimeError(
                'Model database must be initialised before solution')

        if single is not None and (first is not None or last is not None):
            raise ValueError('The arguments (`first`, `last`) and `single` '
                             'are mutually exclusive; cannot have non-`None` '
                             'values for both sets of arguments')

        # Form tuple of periods to solve, expressed as index slices (rather
        # than period identifiers)
        if single is not None:
            rows_to_solve = (locate_in_index(self.data.index, single), )
        else:
            if first is None:
                if self.start_offset is None:
                    first = self.data.index[0]
                else:
                    first = self.data.index[self.start_offset]
            if last is None:
                if self.end_offset is None:
                    last = self.data.index[-1]
                else:
                    last = self.data.index[-1 - self.end_offset]
            rows_to_solve = tuple(range(
                locate_in_index(self.data.index, first),
                locate_in_index(self.data.index, last) + 1))

        # Set `verbosity` to be no higher than the (hardcoded) maximum
        # permitted value
        verbosity = min(2, verbosity)

        # Initial report of periods to solve, depending on `verbosity` value
        info = {'first': str(self.data.index[rows_to_solve[0]]),
                'last': str(self.data.index[rows_to_solve[-1]]),
                'length': len(rows_to_solve)}

        if verbosity == 0:
            pass
        elif verbosity in (1, 2):
            if info['length'] == 1:
                print('{first}[{length}] '.format(**info), end='')
            else:
                print('{first}:{last}[{length}] '.format(**info), end='')
        else:
            raise ValueError(
                'Invalid value for `verbosity`: {}'.format(verbosity))
        sys.stdout.flush()

        # Solve model
        self._solver(rows_to_solve,
                     min_iter, max_iter, tol,
                     verbosity,
                     **kwargs)


    def _solver_gauss_seidel_python(self,
                                    rows_to_solve,
                                    min_iter, max_iter, tol,
                                    verbosity,
                                    *,
                                    stop_on_nan=True,
                                    copy=None):
        """Gauss-Seidel solver, implemented in Python.

        Parameters
        ----------
        rows_to_solve : tuple of ints
        min_iter, max_iter : ints
        tol : float
        verbosity : int
        stop_on_nan : bool
        copy : str {'endogenous', 'convergence'}, default `None`
            If not `None`, copy selected values from the previous period into
            the current period prior to solution. This may help to reduce the
            number of iterations to convergence and/or guard against `NaN`s in
            the event of an unfavourable/unfortunate equation order.

            Options:
             - 'endogenous' : copy endogenous variables only
             - 'convergence' : copy convergence variables only

        """
        spacing = [False] * len(rows_to_solve)
        if verbosity == 2:
            spacing = self._make_spacing(rows_to_solve)

        for i, row in enumerate(rows_to_solve):
            status = 'F'

            # Optionally copy previous period's values over to the current period
            if copy is not None:
                if copy == 'endogenous':
                    raise NotImplementedError
                if copy == 'convergence':
                    copy_vars = self.convergence_variables
                else:
                    raise ValueError('Invalid `copy` argument: {}'.format(copy))

                if len(copy_vars) > 1:
                    self.data.iloc[row, [self.data.columns.get_loc(v) for v in copy_vars]] = (
                        self.data.iloc[row - 1, [self.data.columns.get_loc(v) for v in copy_vars]])
                else:
                    self.data.iloc[row, self.data.columns.get_loc(copy_vars[0])] = (
                        self.data.iloc[row - 1, self.data.columns.get_loc(copy_vars[0])])

            current = self.data[self.convergence_variables].values[row].copy()
            for iteration in range(1, max_iter + 1):

                previous = current.copy()
                self._solve_python_iteration(row)
                current = self.data[self.convergence_variables].values[row].copy()

                if iteration >= min_iter:
                    diff = current - previous
                    sum_sq_diff = sum(diff ** 2)

                    if stop_on_nan and np.isnan(sum_sq_diff):
                        status = 'N'
                        break

                    if sum_sq_diff < tol:
                        status = '.'
                        break

            self.data['status'].values[row] = status
            self.data['iterations'].values[row] = iteration
            self.data['converged'].values[row] = True if status == '.' else False

            if verbosity == 0:
                pass
            elif verbosity in (1, 2):
                if verbosity == 2 and spacing[i]:
                    print(' ', end='')
                print(status, end='')
            else:
                raise ValueError(
                    'Invalid value for `verbosity`: {}'.format(verbosity))
            sys.stdout.flush()

        if verbosity == 0:
            pass
        elif verbosity in (1, 2):
            print('')
        else:
            raise ValueError(
                'Invalid value for `verbosity`: {}'.format(verbosity))
        sys.stdout.flush()

    def _make_spacing(self, rows=None):
        if rows is None:
            rows = range(len(self.data.index))

        spacing = [False] * len(rows)
        periods = list(self.data.index[[rows]])

        try:
            freq = self.data.index.freqstr
            periods = [p.year for p in periods]
        except AttributeError:
            freq = 'A'

        if freq.startswith('A'):
            if len(rows) > 25:
                blocks = (10, )
            else:
                blocks = (5, 10)

            try:
                spacing = [any([(year % b) == 0 for b in blocks])
                           for year in periods]
            except TypeError:
                spacing = [any([(i % b) == 0 for b in blocks])
                           for i in range(len(periods))]
        else:
            for i in range(1, len(periods)):
                if periods[i] != periods[i-1]:
                    spacing[i] = True

        spacing[0] = False
        return spacing


    def _solve_python_iteration(self, row):
        raise NotImplementedError
