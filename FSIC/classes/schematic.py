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

        See also
        ========
        FSIC.classes.schematic.Function.to_graph()
        FSIC.classes.schematic.Model.to_graph()

        """
        if self.string is None:
            raise ValueError

        n = [Variable(a).expr for a in self.n]
        x = [Variable(a).expr for a in self.x]

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
        The DiGraph object has a similar structure to that of the DiGraph
        produced by the `Equation` class. That is, the vertices of the graph
        correspond to variables in the system (whether endogenous or exogenous)
        and endogenous variables have further attributes assigned to them.

        In the case of the `Function` class, endogenous variables have two
        attributes:
         - 'equations' : list of strings
           Consolidated list of equations that solve for this variable
           (combined from individual `Equation` objects)
         - 'functions' : list of strings
           List of functions that contain the current variable (just the name
           of the current function; may be combined with other functions by the
           `Model` class)

        See also
        ========
        FSIC.classes.schematic.Equation.to_graph()
        FSIC.classes.schematic.Model.to_graph()

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
    """FSIC class to handle a complete system of model equations.

    """

    def __init__(self, name=None):
        self.name = None
        self.functions = None

    def add_function(self, equations, name=None):
        """Add a new function (list of equations) to the model.

        Parameters
        ==========
        ** These arguments match the `equation` and `name` members of the
           `Function` class **

        equations : list of strings
            List of equations that comprises the new function
        name : string (or `None`)
            Name to assign to the function (otherwise, use `Function` class
            default)

        Returns
        =======
        N/A

        Sets
        ====
        self.functions : Dictionary of `Function` objects
            Initialises `self.functions` to a Dictionary (if currently `None`)
            and adds the data as a new `Function` object.

        See also
        ========
        FSIC.classes.schematic.Function.parse()

        """
        if self.functions is None:
            self.functions = {}
        fn = Function(name)
        fn.parse(equations)
        self.functions[fn.name] = fn

    def to_graph(self):
        """Return the model as a graph.

        Returns
        =======
        G : NetworkX DiGraph object

        Notes
        =====
        The DiGraph object has an identical structure to that of the DiGraph
        produced by the `Function` class. That is, the vertices of the graph
        correspond to variables in the system (whether endogenous or exogenous)
        and endogenous variables have further attributes assigned to them.

        The endogenous variables have two attributes:
         - 'equations' : list of strings
           Consolidated list of equations that solve for this variable
           (across all functions and equations)
         - 'functions' : list of strings
           List of functions that contain the current variable

        See also
        ========
        FSIC.classes.schematic.Equation.to_graph()
        FSIC.classes.schematic.Function.to_graph()

        """
        if self.functions is None:
            raise ValueError

        G = nx.DiGraph()
        for fn in self.functions.values():
            G_fn = fn.to_graph()
            for n, d in G_fn.nodes(data=True):
                if n in G and len(d):
                    a = G.node[n]
                    d['equations'] = list(set(a.get('equations', []) +
                                              d.get('equations', [])))
                    d['functions'] = list(set(a.get('functions', []) +
                                              d.get('functions', [])))
                G.add_node(n, d)
            G.add_edges_from(G_fn.edges())

        return G


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
