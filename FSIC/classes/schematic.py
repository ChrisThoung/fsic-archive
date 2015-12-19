# -*- coding: utf-8 -*-
"""
schematic
=========
Definitions for FSIC schematic classes:
 - Variable

"""


import re


class Variable(object):
    """FSIC class to parse a single variable expression."""
    # Set, get and delete class methods
    def __setitem__(self, key, value):
        self.__setattr__(key, value)
    def __getitem__(self, key):
        return self.__getattribute__(key)
    def __delitem__(self, key):
        self.__delattr__(key)

    # Default regular expression
    pattern = re.compile(r'''
        (?P<name>[A-Za-z_][0-9A-Za-z_]*)
        (?:\[(?P<index>[+-]*[0-9]*)\])?''', re.VERBOSE)

    def __init__(self, string=None, pattern=None):
        self.raw_string = string
        self._set_pattern(pattern)

        self.expr_template = '{name}[{index}]'

        if self.raw_string is not None:
            self.parse(self.raw_string)

    def _set_pattern(self, pattern):
        """Set the regular expression pattern to parse strings.

        Parameter
        ---------
        pattern : if `None` - set to default pattern
                     string - compile to regular expression (with `re.VERBOSE`)
                     pattern object - just store

        """
        if pattern is None:
            self.pattern = Variable.pattern
        elif type(pattern) is str:
            self.pattern = re.compile(pattern, re.VERBOSE)
        else:
            self.pattern = pattern

    def parse(self, string=None, pattern=None):
        """Parse a variable string.

        Parameters
        ----------
        string : `None` or string
            String to parse (if `None`, use previously stored string)
        pattern : `None`, string or pattern object
            Regular expression to apply to `string`
            (if `None`, use previously stored pattern or default)

        Notes
        -----
        A valid regular expression identifies two groups, by index number,
        rather than name:
         - .groups()[0] : the variable name (usually a valid Python identified)
         - .groups()[1] : optional - the period index

        The pattern should *not* capture brackets in the expression.

        For example:

            The pattern: '([A-Za-z_][0-9A-Za-z_]*)\[([+-]*[0-9]*)\]'
            when applied to: 'H_h[-1]'
            should return the following group: ('H_h', '-1')

            when applied to: 'YD'
            should return the following group: ('YD', 'None')

        """
        # Store arguments, if required
        if string is not None:
            self.raw_string = string
        self._set_pattern(pattern)
        # Run regex search
        match = self.pattern.search(self.raw_string)
        name, raw_index = match.groups()
        self.name = name
        self.raw_index = raw_index
        # Identify index as an integer
        if type(raw_index) is str:
            sign, num = re.search(r'([+-]*)([0-9]*)', raw_index).groups()
            if sign is not None:
                sign = sign.replace('+', '')
                sign = re.sub(r'(?:[-]{2})+', '', sign)
            else:
                sign = ''
            index = int(sign + num)
        else:
            index = 0
        self.index = index
        # Convert integer index to string
        if index > 0:
            index_string = '+' + str(index)
        elif index == 0:
            index_string = ''
        else:
            index_string = str(index)
        self.index_string = index_string
        # Store substitution values
        self.sub_str = {'name': self.name, 'index': self.index}
        self.sub_expr = {'name': self.name, 'index': 'period' + self.index_string}
        self.str = self._expr(expr=False).replace('[0]', '')
        self.expr = self._expr(expr=True)

    def __str__(self):
        return self.str

    def _expr(self, expr=False):
        if expr:
            fmt = self.sub_expr
        else:
            fmt = self.sub_str
        return self.expr_template.format(
            name=fmt['name'],
            index=fmt['index'])

    def __repr__(self):
        return 'Variable(string="{raw_string}", pattern="{pattern}")'.format(
            raw_string=self.raw_string,
            pattern=self.pattern)

class Equation(Variable):
    """FSIC class to parse a single equation expression."""
    # Set, get and delete class methods
    def __setitem__(self, key, value):
        self.__setattr__(key, value)
    def __getitem__(self, key):
        return self.__getattribute__(key)
    def __delitem__(self, key):
        self.__delattr__(key)

    def __init__(self, string=None, pattern=None, sep='='):
        self.raw_string = string
        self._set_pattern(pattern)
        self.sep = sep

        if self.raw_string is not None:
            self.parse(self.raw_string)

    def parse(self, string=None, pattern=None, sep=None):
        """Parse an equation string.

        Parameters
        ----------
        string : `None` or string
            String to parse (if `None`, use previously stored string)
        pattern : `None`, string or pattern object
            Regular expression to apply to `string` to identify variables
            (if `None`, use previously stored pattern or default)
        sep : string
            String to separate endogenous variables (on the left-hand side)
            from exogenous variables (on the right-hand side)

        """
        # Store arguments, if required
        if string is not None:
            self.raw_string = string
        self._set_pattern(pattern)
        if sep is not None:
            self.sep = sep
        # Split into endogenous and exogenous components
        endo, exog = self.raw_string.split(self.sep)
        # Run regex searches on the two components
        self.endo = self._parse(endo)
        self.exog = self._parse(exog)
        self.variables = self.endo + self.exog
        # Form template string
        def repl(match):
            v = Variable(
                match.string[match.span()[0]:match.span()[1]],
                pattern=self.pattern)
            name = str(v)
            return '{' + str(v).replace('[', '').replace(']', '') + '}'
        self.expr_template = self.pattern.sub(repl, self.raw_string)
        # Store substitution values
        self.sub_str = {v.replace('[', '').replace(']', ''): str(self[v])
                        for v in self.variables}
        self.sub_expr = {v.replace('[', '').replace(']', ''): self[v].expr
                         for v in self.variables}
        self.str = self._expr(expr=False)
        self.expr = self._expr(expr=True)

    def _parse(self, string):
        keys = []
        for match in self.pattern.finditer(string):
            v = Variable(
                match.string[match.span()[0]:match.span()[1]],
                pattern=self.pattern)
            name = str(v)
            self[name] = v
            keys.append(name)
        return keys

    def __iter__(self):
        for v in self.variables:
            yield self[v]

    def _expr(self, expr=False):
        if expr:
            return self.expr_template.format(**self.sub_expr)
        else:
            return self.expr_template.format(**self.sub_str)

    def __repr__(self):
        return 'Equation(string="{raw_string}", pattern="{pattern}", sep="{sep}")'.format(
            raw_string=self.raw_string,
            pattern=self.pattern,
            sep=self.sep)
