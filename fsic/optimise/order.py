# -*- coding: utf-8 -*-
"""
order
=====
FSIC module to optimise the order of a system of equations to reduce the number
of iterations to convergence by the Gauss-Seidel method.

"""


try:
    import networkx as nx
except:
    raise ImportError('Unable to import NetworkX')


def recursive(equations):
    """Reorder `equations` to be 'more recursive'.

    Parameters
    ==========
    equations : list of strings
        List of equations to reorder, one equation per element

    Returns
    =======
    reordered : list of strings
        Reordered version of equations (unchanged if length of equation list is
        one or zero)

    Notes
    =====
    The procedure for reordering the equations is as follows:

    1. Translate `equations` into a directed graph object (a NetworkX DiGraph)

    """
    # Return `equations` unchanged if length is zero or one
    if len(equations) < 2:
        return equations
    # 1. Translate `equations` into a directed graph object (a NetworkX DiGraph)
    G = make_graph(equations)


def make_graph(equations):
    """Return `equations` as a NetworkX DiGraph.

    Parameters
    ==========
    equations : list of strings
        List of equations to reorder, one equation per element

    Returns
    =======
    G : NetworkX DiGraph object
        Directed graph representation of `equations`

    """
    from fsic.parser.code import identify_variables
    G = nx.DiGraph()
    # Loop by equation
    for e in equations:
        v = identify_variables(e)
        # Extract endogenous variable (should only be one)
        n = v['endogenous']
        if len(n) != 1:
            raise ValueError('Expected just one endogenous variable')
        n = n[0]
        # Extract exogenous variable(s) and add edges
        x = v['exogenous']
        for term in x:
            G.add_edge(term, n)
    # Return
    return G
