# -*- coding: utf-8 -*-
"""
schematic
=========
Definitions for FSIC schematic classes:
 - Equation
 - Function : A group of Equation objects
              e.g. a 'block' of equations specifying a consumption function
 - Model : A group of Function objects, comprising the complete specification

"""


import re

import networkx as nx


class Equation:
    """FSIC class to handle a single equation of a model.

    """

    # Default regular expressions
    sep = re.compile(r'=')
    regex = re.compile(
        r'''[_A-z][_0-z]*
            (?:(?<=\[).*\])?
        ''',
        re.DOTALL | re.VERBOSE)

    def __init__(self):
        self.string = None
        self.n = None
        self.x = None

    def parse(self, string=None, sep=None, regex=None):
        """
        """
        if string is None:
            string = self.string
        self.n, self.x = Equation._parse(string, sep, regex)

    def _parse(string, sep=None, regex=None):
        """Separate `string` into a list of endogenous and exogenous terms.

        Parameters
        ==========
        string : string
            Equation to parse
        sep : regular expression object or
              `None` (defaults to `Equation.regex`)
            Regular expression to split `string` into an endogenous and
            exogenous component
        regex :  regular expression object or
                 `None` (defaults to `Equation.regex`)
            Regular expression to terms in an equation

        Returns
        =======
        n : list of strings
        x : list of strings
            Endogenous and exogenous variables, respectively

        Examples
        ========
        # Default usage
        >>> Equation._parse('C_d = alpha_1 * YD + alpha_2 * H_h[-1]')
        (['C_d'], ['alpha_1', 'YD', 'alpha_2', 'H_h[-1]'])

        # Alternative `sep` argument if, for example, only parsing an 'equation'
        # defined as an endogenous variable and a list of exogenous variables
        >>> Equation._parse('C_d : alpha_1, YD, alpha_2, H_h[-1]',
                            sep=re.compile(r':'))
        (['C_d'], ['alpha_1', 'YD', 'alpha_2', 'H_h[-1]'])

        # Alternative `regex` to only match variables whose identifier begins
        # with a capital letter
        >>> Equation._parse('C_d = alpha_1 * YD + alpha_2 * H_h[-1]',
		            regex=re.compile(r'\b[A-Z][_0-z]+\b'))
        (['C_d'], ['YD', 'H_h'])

        """
        if sep is None:
            sep = Equation.sep
        if regex is None:
            regex = Equation.regex
        n, x = sep.split(string)
        n = regex.findall(n)
        x = regex.findall(x)
        return n, x


class Function:
    def __init__(self):
        pass


class Model:
    def __init__(self):
        pass
