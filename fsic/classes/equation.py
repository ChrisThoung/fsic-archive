# -*- coding: utf-8 -*-
"""
equation
========
`Equation` class to handle specification of a single equation.

"""

from collections import Counter, OrderedDict
from collections.abc import Container, Mapping

import re

from pandas import DataFrame

from fsic.classes.variable import Variable
from fsic.classes.frame import Frame
from fsic.utilities import merge_dicts, make_comparison_function


class Equation(object):
    """FSIC class to specify a single equation."""

    PATTERN = re.compile(
        r'''
        (?P<_raw>
            # Functions: Python identifier followed by brackets
            (?: (?P<function>[_A-Za-z][._A-Za-z0-9]*) (?=\s*[(].*[)]) )|

            # Variable expressions: name + (optional) index
            (?: # Name: Python identifier
                (?: # Parameters: enclosed in braces
                    (?: \{ (?P<parameter>[_A-Za-z][_A-Za-z0-9]*) \} )|

                    # Errors: enclosed in angled brackets
                    (?: < (?P<error>[_A-Za-z][_A-Za-z0-9]*) > )|

                    # Automatic variables: enclosed in '$'
                    (?: [$] (?P<automatic>[_A-Za-z][_A-Za-z0-9]*) [$] )|

                    # Endogenous: before an '=' sign
                    (?: (?P<endogenous>[_A-Za-z][_A-Za-z0-9]*) (?=.*?[=]) )|

                    # Exogenous: anything else
                    (?: (?P<exogenous>[_A-Za-z][_A-Za-z0-9]*) ))

                # Index (optional): enclosed in square brackets
                (?:\s* \[ (?P<_index>.*?) \])? ))''',
        re.VERBOSE)

    PRECEDENCE = ('endogenous', 'exogenous')
    EXCLUSIVE = ('automatic', 'error', 'function', 'parameter')

    CONTAINER_1D = Variable
    CONTAINER_2D = Frame

    EXPRESSION = None

    def __init__(self, expression=None):
        self.raw = expression
        self.template = None
        self.terms = None
        self.symbols = None

        if self.raw is not None:
            self.parse(self.raw)

        self.data = None

        self.index = None
        self.start_offset = None
        self.end_offset = None

    def parse(self, expression):
        """Extract template and table of terms from `expression`."""
        self.raw = expression
        terms = self._parse_terms(self.raw)

        self.template = self._make_template(self.raw, terms)
        self.terms = DataFrame.from_dict(terms, orient='index')
        symbols = self._make_symbols(self.terms)
        self.symbols = DataFrame.from_dict(self._make_symbols(self.terms),
                                           orient='index').loc[symbols.keys(), :]

    def _parse_terms(self, expression):
        """Extract `OrderedDict` of parsed terms from `expression`."""
        terms = OrderedDict()
        counter = Counter()
        for match in self.PATTERN.finditer(expression):
            term = {k: v
                    for k, v in match.groupdict().items()
                    if v is not None or k.startswith('_')}
            # Check for just one type
            type_ = [k for k in term.keys() if not k.startswith('_')]
            assert len(type_) == 1
            type_ = type_[0]
            # Rename reserved keys
            term = {k[0].replace('_', '') + k[1:]: v
                    for k, v in term.items()}
            # Store name and type
            term['name'] = term.pop(type_)
            term['type'] = type_
            # Create normalised variable expression
            term['normalised'] = term['name']
            try:
                term['index'] = int(term['index'])
                if term['index'] != 0:
                    term['normalised'] += '[{:+d}]'.format(term['index'])
            except TypeError:
                term['index'] = 0
            # Generate key and store
            key = '{}_{}'.format(type_, counter[type_])
            counter[type_] += 1
            terms[key] = term.copy()
        return terms

    def _make_template(self, expression, terms):
        """Form clean template from `expression` using the keys in `terms`."""
        template = re.sub(r'\s+', '', self.PATTERN.sub('{}', expression))
        template = re.sub('([*]{2}|[=*/+-])', r' \1 ', template).replace(',', ', ')
        template = template.format(*['{' + k + '}' for k in terms.keys()])
        return template.strip()

    def _make_symbols(self, terms):
        """Form `dict` of symbol information from `terms`."""
        compare_types = make_comparison_function(self.PRECEDENCE, self.EXCLUSIVE)
        symbols = OrderedDict()
        for _, term in terms.iterrows():
            name = term['name']
            entry = {'type': term['type'],
                     'min': term['index'],
                     'max': term['index']}
            if name in symbols:
                entry = merge_dicts([symbols[name], entry],
                                    {'type': compare_types,
                                     'min': min,
                                     'max': max})
            symbols[name] = entry
        return symbols

    def __eq__(self, other, strict=False):
        """Test for equality with `other` in terms of derived (parsed)
           variables. `strict=True` will also test the original inputs (rarely
           useful).

        Parameters
        ----------
        other : object to compare with `self`
            Must have the following attributes (matching those of the current
            object):
             - template : str
             - terms : DataFrame
             - symbols : DataFrame
            If `strict=True`, also requires `raw` (str).
        strict : bool, default `False`
            If `True`, also test that the original inputs are identical.

        """
        if strict:
            if self.raw != other.raw:
                return False

        if self.template != other.template:
            return False
        elif not (self.terms.drop('raw', axis=1) ==
                  other.terms.drop('raw', axis=1)).all().all():
            return False
        elif not (self.symbols == other.symbols).all().all():
            return False

        return True

    def initialise(self, index, values=0.0):
        self.index = tuple(index)

        if isinstance(values, Mapping):
            get = lambda k: values.get(k, 0.0)
        else:
            get = lambda k: values

        data = {k: self.CONTAINER_1D(get(k), self.index)
                for k in self.terms['name']}
        self.data = self.CONTAINER_2D(data)

        for k in self.data.keys():
            setattr(self.__class__, k, self._make_property(self.data, k))

        self.start_offset = -1 * min(self.symbols['min'])
        self.end_offset = max(self.symbols['max'])

        solve_function = self._make_solve_function_script(self.raw, self.template, self.terms)
        exec(solve_function, globals(), locals())
        setattr(self.__class__, 'solve', locals()['solve'])

    @staticmethod
    def _make_property(container, key):

        def getter(self):
            return container.__getitem__(key)

        def setter(self, value):
            container.__setitem__(key, value)

        def deleter(self):
            raise NotImplementedError

        return property(getter, setter, deleter)

    def span(self):
        if self.start_offset is None or self.end_offset is None:
            raise RuntimeError

        for i in range(self.start_offset, len(self.index) - self.end_offset):
            yield self.index[i]

    def solve(self, period=None, data=None):
        raise NotImplementedError

    @staticmethod
    def _make_solve_function_script(raw_expression, template, terms):

        expr_terms = {}
        for i, row in terms.iterrows():
            expr_terms[i] = 'self.{}[index[{}]]'.format(row['name'], row['index'])
        code = template.format(**expr_terms)

        docstring = '''\
Solve: {}

    Coded as: {}

    Parsed from: {}\
'''.format(template.format(**terms['normalised'].to_dict()),
           code,
           template.format(**terms['raw'].to_dict()))

        function = '''\
def solve(self, period=None, data=None):
    """{docstring}

    """
    if period is None:
        period = self.span()
    elif not isinstance(period, Container):
        period = [period]

    for p in period:
        position = self.index.index(p)
        index = self.index[position:] + self.index[:position]
        {code}\
'''.format(docstring=docstring, code=code)

        return function
