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
        Reordered version of equations

    """
    pass
