# -*- coding: utf-8 -*-
"""
model
=====
Base `Model` class for `FSIC` models.

"""

from pandas import Index, Period, PeriodIndex
from pandas import Series, DataFrame

import pandas as pd
pd.set_option('mode.chained_assignment', None)


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
    ERRORS = None

    CONVERGENCE_VARIABLES = None

    START_OFFSET = 0
    END_OFFSET = 0


    def __init__(self, *args, **kwargs):
        self.variables = None
        self.parameters = None
        self.errors = None

        self.convergence_variables = None

        self.start_offset = None
        self.end_offset = None

        self.data = None

        if len(args) or len(kwargs):
            self.initialise(*args, **kwargs)


    def initialise(self,
                   start=None, end=None,
                   solve_from=None, solve_to=None,
                   data=None,
                   variables=None, parameters=None, errors=None,
                   convergence_variables=None,
                   default_value=0.0) -> None:
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
                    `errors`, the columns of `data` and `['status',
                    'iterations', 'converged']` ; `VARIABLES`, `PARAMETERS` and
                    `ERRORS` otherwise

        The order of assignment of the list of convergence variables
        (`self.convergence_variables`) is:
         - `convergence_variables`, if passed
         - `CONVERGENCE_VARIABLES`, if not `None`
         - `self.variables` otherwise

        """
        # Make `DataFrame` index and find offsets
        index = self._make_index(start, end,
                                 solve_from, solve_to,
                                 data)
        if solve_from:
            self.start_offset = self._locate_in_index(index, solve_from)
        else:
            self.start_offset = self.START_OFFSET

        if solve_to:
            self.end_offset = self._locate_in_index(index, solve_from)
        else:
            self.end_offset = self.END_OFFSET

        # Form combined list of variables, using class attributes as defaults
        def assign_or_use_default(arg, default):
            if arg:
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
        if start:
            pass
        elif solve_from:
            try:
                solve_from = Period(solve_from)
            except ValueError:
                pass
            start = solve_from - self.START_OFFSET

            if data is not None:
                start = min(start, data.index[0])

        elif data is not None:
            start = data.index[0]
        else:
            raise ValueError('Must provide a start period, '
                             'either explicitly '
                             '(`start` or the index of `data`) '
                             'or implicitly (`solve_from`)')
        if end:
            pass
        elif solve_to:
            try:
                solve_to = Period(solve_to)
            except ValueError:
                pass
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
            index = Index(range(start, end + 1))
        return index

    def _locate_in_index(self, index, period) -> int:
        """Return the location of `period` in `index`.

        Parameters
        ----------
        index : `pandas` `Index`-like
            Array to search in (an object with a `get_loc()` method)
        period : int or valid argument to `pandas` `Period` class
            Item to search for

        Returns
        -------
        : int
            The location of `period` in `index`

        """
        if index.holds_integer():
            period = int(period)
        else:
            period = Period(period)
        return index.get_loc(period)

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
