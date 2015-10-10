# -*- coding: utf-8 -*-
"""
schematic
=========
Definitions for FSIC schematic classes:
 - Variable
 - Equation
 - Function : A group of Equation objects
              e.g. a 'block' of equations specifying a consumption function
 - Model : A group of Function objects, comprising the complete specification

"""


import re

import networkx as nx


class Variable:
    """FSIC class to process a single variable expression.

    """

    match = re.compile(
        r'''\b(?P<name>[_A-Za-z][_0-9A-Za-z]*)
            \b(?:(?P<index>\[.*\]))?
        ''',
        re.VERBOSE)
    replace = re.compile(
        r'''\[(.*)\]
        ''',
        re.VERBOSE)

    def __init__(self, string=None, match=None, replace=None):
        self.string = None
        self.name = None
        self.index = None
        self.mindex = None
        self.expr = None

        if match is None:
            self.match = Variable.match
        else:
            self.match = match

        if replace is None:
            self.replace = Variable.replace
        else:
            self.replace = replace

        if string is not None:
            self.string = string
            self.parse()

    def parse(self, string=None, match=None, replace=None):
        """Split `string` and derive a Python-compatible index expression.

        Parameters
        ==========
        string : string or `None`
            The variable string to process (e.g. 'C_d' or 'H_h[-1]'). If
            `None`, use `self.string` instead
        match : regular expression (as object or string) or `None`
            Regular expression to identify the variable name and index as named
            groups (see `Variable.match` for the default). If `None`, use
            `Variable.match`
        replace : regular expression (as object or string) or `None`
            Regular expression to identify the inner part of an index
            expression (see `Variable.replace` for the default). If `None`, use
            `Variable.replace`

        Returns
        =======
        N/A

        Sets
        ====
        (For an example `string` argument, 'H_h[-1]'.)
        self.name : string
            The variable name in `string`, e.g. 'H_h'
        self.index : string
            The variable index in `string`, e.g. '[-1]'
        self.mindex :
            The variable index as a Python-compatible expression, e.g. '[period-1]'
        self.expr : string
            `self.name` + `self.mindex`, e.g. 'H_h[period-1]'

        See also
        ========
        FSIC.classes.schematic.Variable._parse()

        """
        if string is None:
            string = self.string
        else:
            self.string = string

        if match is not None:
            self.match = match

        if replace is not None:
            self.replace = replace

        self.name, self.index, self.mindex = Variable._parse(
            self.string, match=self.match, replace=self.replace)
        self.expr = self.name + self.mindex

    def _parse(string, match=None, replace=None):
        if match is None:
            match = Variable.match
        if type(match) is str:
            match = re.compile(match)

        if replace is None:
            replace = Variable.replace
        if type(replace) is str:
            replace = re.compile(replace)

        m = match.search(string)
        index = m.group('index')

        if index is None or index == '[]' or re.match(r'\[0+\]', index):
            mindex = '[period]'
        else:
            mindex = replace.sub(r'[period+\1]', index)
            mindex = re.sub('[+]([+-])', r'\1', mindex)

        return m.group('name'), index, mindex


class Equation:
    """FSIC class to handle a single equation of a model.

    """

    sep = re.compile(r'=')
    regex = re.compile(
        r'''[_A-z][_0-z]*
            (?:(?<=\[).*\])?
        ''',
        re.DOTALL | re.VERBOSE)

    def __init__(self, string=None, sep=None, regex=None):
        self.string = None
        self.n = None
        self.x = None
        self.vars = None
        self.expr = None
        self.count = None

        if sep is None:
            self.sep = Equation.sep
        else:
            self.sep = sep

        if regex is None:
            self.regex = Equation.regex
        else:
            self.regex = regex

        if string is not None:
            self.string = string
            self.parse()

    def parse(self, string=None, sep=None, regex=None):
        """Identify endogenous and exogenous terms in an equation string.

        Parameters
        ==========
        ** Where arguments are not provided (or set to `None`), this function
           defaults to class member variables. **

        string : string
            Equation to parse
        sep : regular expression (string or compiled object) or
              `None` (defaults to `Equation.regex`)
            Regular expression to split `string` into an endogenous and
            exogenous component
        regex :  regular expression (string or compiled object) or
                 `None` (defaults to `Equation.regex`)
            Regular expression to terms in an equation

        Returns
        =======
        N/A

        Sets
        ====
        self.string : string
            Set to match `string`
        self.n : list of strings
        self.x : list of strings
            Endogenous and exogenous variables, respectively
        self.vars : tuple of strings
            Tuple containing `self.n` and `self.x`
        self.expr : string
            String expression version of `string`
            e.g. '%s = %s' for 'C_s = C_d'
        self.count : integer
            The number of identified variables in `string`, equal to:
             - the number of instances of '%s' in `self.expr`
             - the sum of the lengths of `self.n` and `self.x`

        Notes
        =====
        A successful parse should result in:

            eqn.string == eqn.expr % eqn.vars

        where `eqn` is the current `Equation` object

        See also
        ========
        FSIC.classes.schematic.Equation._parse()

        """
        if string is None:
            string = self.string
        else:
            self.string = string

        if sep is not None:
            self.sep = sep
        if regex is not None:
            self.regex = regex

        self.n, self.x, self.expr, self.count = Equation._parse(
            self.string, sep=self.sep, regex=self.regex)
        self.vars = tuple(self.n + self.x)

    def _parse(string, sep=None, regex=None):
        """Separate `string` into a list of endogenous and exogenous terms.

        Parameters
        ==========
        string : string
            Equation to parse
        sep : regular expression (string or compiled object) or
              `None` (defaults to `Equation.regex`)
            Regular expression to split `string` into an endogenous and
            exogenous component
        regex :  regular expression (string or compiled object) or
                 `None` (defaults to `Equation.regex`)
            Regular expression to terms in an equation

        Returns
        =======
        n : list of strings
        x : list of strings
            Endogenous and exogenous variables, respectively
        self.expr : string
            String expression version of `string`
            e.g. '%s = %s' for 'C_s = C_d'
        self.count : integer
            The number of identified variables in `string` (equal to the number
            of instances of '%s' in `self.expr`)

        Examples
        ========
        # Default usage
        >>> Equation._parse('C_d = alpha_1 * YD + alpha_2 * H_h[-1]')
        (['C_d'], ['alpha_1', 'YD', 'alpha_2', 'H_h[-1]'], '%s = %s * %s + %s * %s', 5)

        # Alternative `sep` argument if, for example, only parsing an 'equation'
        # defined as an endogenous variable and a list of exogenous variables
        >>> Equation._parse('C_d : alpha_1, YD, alpha_2, H_h[-1]',
                            sep=re.compile(r':'))
        (['C_d'], ['alpha_1', 'YD', 'alpha_2', 'H_h[-1]'], '%s : %s, %s, %s, %s', 5)

        # Alternative `regex` to only match variables whose identifier begins
        # with a capital letter
        >>> Equation._parse('C_d = alpha_1 * YD + alpha_2 * H_h[-1]',
                            regex=re.compile(r'\b[A-Z][_0-z]+\b'))
        (['C_d'], ['YD', 'H_h'], '%s = alpha_1 * %s + alpha_2 * %s[-1]', 3)

        """
        if sep is None:
            sep = Equation.sep
        if type(sep) is str:
            sep = re.compile(sep)

        if regex is None:
            regex = Equation.regex
        if type(regex) is str:
            regex = re.compile(regex)

        n, x = sep.split(string)
        n = regex.findall(n)
        x = regex.findall(x)

        expr, count = regex.subn('%s', string)
        return n, x, expr, count

    def to_graph(self):
        """Return the equation as a graph.

        Returns
        =======
        G : NetworkX DiGraph object

        Notes
        =====
        The DiGraph object has as many vertices as there are variables in the
        equation. The edges run from the exogenous variable(s) (in `self.x`) to
        the endogenous variable(s) (in `self.n`). Each endogenous variable has,
        as an attribute, the original equation string (`self.string`).

        """
        if self.string is None:
            raise ValueError

        n = [Variable(a).expr.replace('period', '').replace('[]', '[0]') for a in self.n]
        x = [Variable(a).expr.replace('period', '').replace('[]', '[0]') for a in self.x]

        G = nx.DiGraph()
        G.name = self.string
        for v in n:
            G.add_node(v, equation=self.expr % tuple(n + x))
            for u in x:
                G.add_edge(u, v)

        return G


class Function:
    """FSIC class to handle a block of equations of a model.

    """

    count = 0

    def __init__(self, name=None):
        Function.count += 1
        if name is None:
            self.name = 'F' + str(Function.count)
        else:
            self.name = name
        self.equations = None

    def parse(self, equations):
        """Parse the contents of `equations` to a list of `Equation` objects.

        Parameters
        ==========
        equations : list of strings
            One equation per string, which must be compatible with the
            `Equation.parse()` function.

        Returns
        =======
        N/A

        Sets
        ====
        self.equations : Dictionary of `Equation` objects
            Each item has a key matching the original equation string and, as
            its value, a parsed `Equation` object

        """
        self.equations = {e: Equation(e) for e in equations}

    def to_graph(self, name=None):
        """Return the system of equations as a graph.

        Returns
        =======
        G : NetworkX DiGraph object

        Notes
        =====

        """
        if self.equations is None:
            raise ValueError

        G = nx.DiGraph()
        G.name = self.name
        for k, v in self.equations.items():
            G_e = v.to_graph()
            for n, d in G_e.nodes(data=True):
                # Update node attributes if variable is endogenous
                if 'equation' in d:
                    d['equations'] = [d.pop('equation')]
                    d['functions'] = [self.name]
                    # Combine attributes if endogenous node already found in `G`
                    if n in G:
                        a = G.node[n]
                        d['equations'] = list(set(a.get('equations', []) +
                                                  d['equations']))
                        d['functions'] = list(set(a.get('functions', []) +
                                                  d['functions']))
                # Insert into `G`
                G.add_node(n, d)
            G.add_edges_from(G_e.edges())

        return G


class Model:
    def __init__(self):
        pass
