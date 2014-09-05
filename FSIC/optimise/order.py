# -*- coding: utf-8 -*-
"""
order
=====
FSIC module to optimise the order of a system of equations to reduce the number
of iterations to convergence by the Gauss-Seidel method.

"""


import warnings

import numpy as np

try:
    import networkx as nx
except:
    raise ImportError('Unable to import NetworkX')


def recursive(equations, warn=True):
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
    warn : boolean
        If `True`, print a warning if there is more than one equation with the
        same endogenous variable

    Notes
    =====
    The procedure for reordering the equations is as follows:

    1. Translate `equations` into a directed graph object (a NetworkX DiGraph)
    2. Extract equation list from node attributes
    3. While there are still nodes in `G`...

    """
    # Return `equations` unchanged if length is zero or one
    if len(equations) < 2:
        return equations
    # 1. Translate `equations` into a directed graph object (a NetworkX DiGraph)
    G = make_graph(equations, warn=warn)
    # 2. Extract equation list from node attributes
    node_equations = nx.get_node_attributes(G, 'equations')
    # 3. While there are still nodes in `G`...
    reordered = []
    while True:
        # Take the in-degree of the nodes in `G` and use to identify the next
        # node(s) to delete
        in_degree = G.in_degree()
        # a. One node remaining: Extract
        if len(in_degree) == 1:
            nodes_to_delete = list(in_degree.keys())
        # b. Nodes with degree zero: Extract
        elif 0 in in_degree.values():
            nodes_to_delete = [k for k, v in in_degree.items() if v == 0]
        # c. More than one node with in-degree of one or greater: Extract the
        #    node with the lowest PageRank (sort alphabetically as a
        #    tie-breaker)
        else:
            pr = nx.pagerank(G)
            # Get lowest PageRank in the system and identify all nodes with that
            # PageRank
            lowest_pr = min(pr.values())
            least_connected_nodes = [k for k, v in pr.items()
                                     if np.isclose(v, lowest_pr)]
            # Sort alphabetically as the tie-breaker
            nodes_to_delete = [sorted(least_connected_nodes)[0]]
        # Add equations to `reordered` and delete endogenous variables from `G`
        for n in nodes_to_delete:
            if n in node_equations:
                for e in node_equations.pop(n):
                    reordered.append(e)
        G.remove_nodes_from(nodes_to_delete)
        # Break if no nodes remain in `G`
        if not len(G.nodes()):
            break
    # Return
    return reordered


def make_graph(equations, warn=True):
    """Return `equations` as a NetworkX DiGraph.

    Parameters
    ==========
    equations : list of strings
        List of equations to reorder, one equation per element
    warn : boolean
        If `True`, print a warning if there is more than one equation with the
        same endogenous variable

    Returns
    =======
    G : NetworkX DiGraph object
        Directed graph representation of `equations`. Nodes signifying
        endogenous variables have, as an attribute, the associated equation
        string(s). If `warn` is `True`, this function prints a warning if
        multiple equations are found for a single endogenous variable.

    """
    from fsic.parser.code import identify_variables
    G = nx.DiGraph()
    # Initialise dictionary to store equations
    node_equations = {}
    # Loop by equation
    for e in equations:
        v = identify_variables(e, suffix=r'\[.+?\]')
        # Extract endogenous variable (should only be one)
        n = v['endogenous']
        if len(n) != 1:
            raise ValueError('Expected just one endogenous variable')
        n = n[0]
        # Extract exogenous variable(s) and add edges
        x = v['exogenous']
        for term in x:
            G.add_edge(term, n)
        # Store equation with the endogenous variable as the key
        if n in node_equations:
            if warn:
                warnings.warn(
                    'An endogenous variable appears as the left hand-side '
                    'variable in more than one equation',
                    Warning)
            node_equations[n] = node_equations[n] + [e]
        else:
            node_equations[n] = [e]
    # Add equations to node attributes
    nx.set_node_attributes(G, 'equations', node_equations)
    # Return
    return G
