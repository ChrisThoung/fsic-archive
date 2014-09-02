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
    # 2. While there are still nodes in `G`...
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
        # c. More than one node with in-degree of one or greater: Extract
        #    the node with the lowest PageRank
        else:
            break
        # Delete from `G`
        G.remove_nodes_from(nodes_to_delete)
        # Break if no nodes remain in `G`
        if not len(G.nodes()):
            break
    # Return
    return reordered


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
    # Return
    return G
