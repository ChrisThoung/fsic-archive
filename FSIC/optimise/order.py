# -*- coding: utf-8 -*-
"""
order
=====
FSIC module to optimise the order of a system of equations to reduce the number
of iterations to convergence by the Gauss-Seidel method.

"""


import warnings

import numpy as np
import networkx as nx


def recursive(equations, warn=True):
    """Reorder `equations` to be 'more recursive'.

    Parameters
    ==========
    equations : list of strings
        List of equations to reorder, one equation per element
    warn : boolean
        If `True`, print a warning if there is more than one equation with the
        same endogenous variable

    Returns
    =======
    reordered : list of strings
        Reordered version of equations (unchanged if length of equation list is
        one or zero)

    Notes
    =====
    The procedure for reordering the equations in the system is as follows:

    1. Translate the list of equation strings into a directed graph object (a
       NetworkX DiGraph) with name `G`, where the nodes correspond to the
       variables in the model. Endogenous variables have, as an attribute, the
       original equation string in `equations`

    2. 'Pop' variables from `G` and add the corresponding equations (where the
       variables are endogenous) to `reordered` according to the following
       algorithm:

       While there are still nodes in `G`, calculate their in-degrees,
       popping as follows:

           a. Just one node remaining: Pop from `G` and finish
           b. Pop all nodes with degree zero (are exogenous from the point of
              view of the system); return to start i.e. by recalculating the
              in-degrees of `G` after removing one or more nodes
           c. More than one node with in-degree greater than zero: Pop the node
              with the lowest PageRank, on the basis that this node is the
              least endogenous/important, as defined by its PageRank. It has
              the lowest probability of being passed through and is thus the
              node with the lowest system-wide dependency. It is the 'most
              exogenous' variable

    """
    # Return `equations` unchanged if length is zero or one
    if len(equations) < 2:
        return equations
    # 1. Translate `equations` into a directed graph object
    #    (a NetworkX DiGraph)
    G = make_graph(equations, warn=warn)
    node_equations = nx.get_node_attributes(G, 'equations')
    # 2. While there are still nodes in `G`...
    reordered = []
    while True:
        # ...take the in-degree of the nodes in `G` and use to identify the
        # next node(s) to delete
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
            # Get lowest PageRank in the system and identify all nodes with
            # that PageRank
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
    from FSIC.parser.code import identify_variables
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
