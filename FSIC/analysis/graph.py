# -*- coding: utf-8 -*-
"""
graph
=====
FSIC module for graph analysis of models.

"""

import networkx as nx
from FSIC.classes.equation import Equation


def make_graph(equations, name='normalised', ignore_self_loops=False):
    """Form a system of equations into a directed graph.

    Parameters
    ----------
    equations : str, or list/dict of str/Equation
        The system of equations to form into a graph. Can be:
         - str : one equation per line (empty lines are automatically ignored)
         - list or dict-like : one equation per item, whether as a string or an
                               `Equation` object (or a mix). If a dict, only
                               use the values; that is, the keys are irrelevant
    name : str, default 'normalised'
        The column of the `Equation`s' `terms` attribute to use to name the
        keys
    ignore_self_loops : bool, default `False`
        If `True`, ignore any self loops from equations where a variable is
        both an endogenous and an exogenous variable. This avoids adding an
        edge to the graph, but the variable will still have a non-empty
        'equations' attribute

    Returns
    -------
    G : `networkx` `DiGraph`
        The system of equations as a graph, with:
         - vertices: the variables of the system (excluding parameters and
                     errors; also ignores functions)
         - edges: denoting variables that determine other variables. For
                  example, an edge from 'x' to 'y' denotes 'y' as an endogenous
                  variable that depends on 'x'

        The vertices have an attribute 'equations', which is either:
         - a tuple of strings listing the equations in which the vertex is an
           endogenous variable. The equation *always* uses the normalised
           version of the variables
         - an empty tuple, if a vertex is an exogenous variable, with no
           accompanying equation

    """
    equation_list = _make_equation_list(equations)
    G = _make_graph_from_list(equation_list, name, ignore_self_loops)

    equation_mapping = _map_equations_to_nodes(equation_list, name)
    # Only keep nodes that are already in `G`, rather than duplicating the
    # filtering in `_make_graph_from_list()`, either here or in
    # `_map_equations_to_nodes()`
    equation_mapping = {k: equation_mapping[k] for k in G.nodes()}
    nx.set_node_attributes(G, 'equations', equation_mapping)

    return G

def _make_equation_list(equations):
    def make_clean_list(list_):
        clean_list = []
        for item in list_:
            if type(item) is str:
                item = item.strip()
                if len(item):
                    item = convert_to_equation(item)
                else:
                    continue
            clean_list.append(item)
        return clean_list

    def convert_to_equation(item):
        if isinstance(item, Equation):
            return item
        elif type(item) is str:
            return Equation(item)
        else:
            raise TypeError(
                'Unrecognised item of type: {}'.format(type(item)))

    if type(equations) is str:
        equations = [e.strip()
                     for e in equations.split('\n')
                     if len(e.strip())]

    if type(equations) is list:
        return make_clean_list(equations)
    elif isinstance(equations, dict):
        return make_clean_list(equations.values())
    else:
        raise TypeError(
            'Unrecognised input variable of type: {}'.format(type(equations)))

def _make_graph_from_list(list_, key='normalised', ignore_self_loops=False):
    G = nx.DiGraph()
    for equation in list_:
        endogenous = []
        exogenous = []
        for _, variable in equation.terms.iterrows():
            name, type_ = variable[[key, 'type']]
            if type_ in ('endogenous', ):
                endogenous.append(name)
            elif type_ in ('exogenous', ):
                exogenous.append(name)
            elif type_ in ('function', 'parameter', 'error', ):
                continue
            else:
                raise ValueError(
                    'Unrecognised variable type: {}'.format(type_))

            for n in endogenous:
                for x in exogenous:
                    if ignore_self_loops and x == n:
                        continue
                    G.add_edge(x, n)
    return G

def _map_equations_to_nodes(list_, key='normalised'):
    equation_mapping = {}
    for equation in list_:
        expression = equation.template.format(
            **equation.terms['normalised'].to_dict())
        for _, variable in equation.terms.iterrows():
            name = variable[key]
            entry = equation_mapping.get(name, ())
            if variable['type'] == 'endogenous':
                entry += (expression, )
            equation_mapping[name] = entry
    return equation_mapping
