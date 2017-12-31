# -*- coding: utf-8 -*-
"""
graph
=====
FSIC module for graph analysis of models.

"""

import itertools
import networkx as nx
from fsic.classes.equation import Equation


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
    nx.set_node_attributes(G, name='equations', values=equation_mapping)

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
            elif type_ in ('function', 'parameter', 'automatic', 'error', ):
                continue
            else:
                raise ValueError(
                    'Unrecognised variable type: {}'.format(type_))

        for n in endogenous:
            if len(exogenous):
                for x in exogenous:
                    if ignore_self_loops and x == n:
                        continue
                    G.add_edge(x, n)
            else:
                G.add_node(n)

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


def topological_sort(G):
    """Return the topological order of the equation system graph, unravelling
       strongly connected components and their cycles.

    Parameter
    ---------
    G : NetworkX `DiGraph`
        Graph representation of the equation system as created, for example, by
        `make_graph()`. Nodes must have an 'equations' attribute containing a
        tuple. Tuples for nodes with accompanying equations should be non-empty
        and contain strings. See `make_graph()` for more information.

    Returns
    -------
    nested_equation_order : list of lists of strings
        The ordered list of equations (taken from the non-empty node 'equation'
        attributes), nested by subgraph (directed acyclic graph or strongly
        connected component). To flatten this list:

        >>> import itertools
        >>> flattened_equation_order = list(
        ...     itertools.chain.from_iterable(nested_equation_order))

    Notes
    -----
    In most cases, a straight *topological sort* of the graph will not be
    possible, because models with feedback have *strongly connected components*
    (groups of variables with one or more cycles of causation). Consequently,
    the graph is unlikely to be a *directed acyclic graph* and NetworkX's
    topological sort function will not work directly.

    The solution here is to split the graph into a sequence of subgraphs,
    alternating between:
     - directed acyclic graphs, which can be topologically sorted
     - strongly connected components, which contain cycles that must be broken

    Each subgraph can then be unravelled to get the ordered list of nodes (see
    `_unravel_graph()` for details). With this list, at each variable, there is
    a check for accompanying equations (the tuple in the 'equations'
    attribute). If found, this function pushes the equation string(s) to the
    final variable, `order`.

    The *condensation* of the graph is the directed acyclic graph that arises
    from contracting the strongly connected components into single nodes. (See
    Fennell et al [2014] for a good explanation of this, as it applies to
    Stock-Flow Consistent models.) A topological sort of the condensation graph
    identifies the high-level directions of causation between the subgraphs.

    References
    ----------
    Fennell, P., O'Sullivan, D., Godin, A., Kinsella, S. (2014),
    'Visualising Stock Flow Consistent models as directed acyclic graphs',
    05/09/2014, *Social Science Research Network*:
    http://papers.ssrn.com/sol3/papers.cfm?abstract_id=2492242
    [Accessed 01/05/2016]

    See also
    --------
    fsic.analysis.graph.make_graph() : creates an object compatible with this
                                       function
    fsic.analysis.graph._unravel_graph() : unravels a subgraph into an ordered
                                           list of nodes

    """
    equations_by_node = nx.get_node_attributes(G, 'equations')
    nested_equation_order = []
    for subgraph in _split_graph(G):
        # Unravel `subgraph`
        if len(subgraph) > 1:
            ordered_nodes = itertools.chain.from_iterable(
                _unravel_graph(subgraph))
        else:
            ordered_nodes = subgraph.nodes()
        # Add equations to `nested_equation_order`
        ordered_equations = []
        for node in ordered_nodes:
            equations = equations_by_node[node]
            if len(equations):
                ordered_equations += equations
        if len(ordered_equations):
            nested_equation_order.append(ordered_equations)

    return nested_equation_order

def _split_graph(G):
    """Split `G` into a list of directed acyclic graphs and strongly connected
       components.

    Parameter
    ---------
    G : NetworkX `DiGraph`

    Returns
    -------
    subgraphs : list of NetworkX `DiGraph` objects
        Each graph in this list is either a directed acyclic graph or a
        strongly connected component. The order of these subgraphs, if
        contracted into single nodes, would define a directed acyclic graph

    """
    # Condensation of `G` and mapping of nodes back to `G`
    C = nx.condensation(G)
    c_to_g_node_mapping = [tuple(c[1]['members'])
                           for c in C.nodes(data=True)]
    # Topological order of `C`, as groups of constituent nodes (from `G`)
    ordered_node_groups = [c_to_g_node_mapping[i]
                           for i in nx.topological_sort(C)]
    # Combine single nodes into lists that define directed acyclic graphs
    combined_node_groups = []
    node_store = ()
    for group in ordered_node_groups:
        if len(group) == 1:
            node_store += group
            continue
        else:
            if len(node_store):
                combined_node_groups.append(node_store)
                node_store = ()
            combined_node_groups.append(group)

    if len(node_store):
        combined_node_groups.append(node_store)

    return [nx.DiGraph(G.subgraph(group)) for group in combined_node_groups]

def _unravel_graph(G):
    """Unravel `G` into a list of lists of ordered nodes.

    Parameter
    ---------
    G : NetworkX `DiGraph`
        Either a directed acyclic graph, or a strongly connected component.

    Returns
    -------
    nested_order : list of lists of strings
        The ordered groups of nodes of the graph:
         - if a directed acyclic graph: the topological sort, with alphabetical
           sorting as a tie-breaker
         - otherwise: the ordered cycles, reduced so that no cycle is a
           superset of another in the graph. In some cases, this reduces a
           cycle to a directed acyclic graph, permitting a topological sort (as
           above). Otherwise, the order breaks the cycle beginning with the
           first variable from an alphabetical sort

    Notes
    -----
    If `G` is a *directed acyclic graph*, this function just returns the
    *topological sort* of the nodes as the inner list of a one-element outer
    list. For stability (predictability, including for testing), alphabetical
    order is the tie-breaker. By definition, this tie-breaker has no bearing on
    performance in solution as all equations appear before any dependent
    equations.

    If `G` is a *strongly connected component*, the steps to unravel the graph
    are as follows:

    1. Identify the *simple cycles* of the component (there can be more than
       one), from shortest to longest
    2. For each cycle:
       a. Remove any simple cycles identified in previous iterations that are
          subsets of the current one (hence the ordering of cycles from
          shortest to longest)
       b. If the pruned node list is no longer a cycle, then it is a directed
          acyclic graph. A topological sort is possible, as for the case where
          the entirety of `G` is a directed acyclic graph
          If the pruned node list remains a cycle, use the first variable from
          an alphabetical sort as the starting point and unravel the cycle by
          following the path from that node

    The treatment of strongly connected components and their constituent cycles
    is a combination of the need for a predictable order (again, for testing),
    and the result of tests (mainly using Godley and Lavoie's [2007] Model
    *SIM*). This treatment seems to have reasonable properties in solution, as
    measured by the number of iterations to convergence. The treatment will not
    necessarily yield the *most* efficient ordering for *all* model solutions.

    References
    ----------
    Godley, W., Lavoie, M. (2007),
    *Monetary economics: An integrated approach to
     credit, money, income, production and wealth*,
    Palgrave Macmillan

    """
    def order_dag(G):
        """Return the topological sort of `G`, using alphabetical sorting as a
           tie-breaker."""
        order = []
        while True:
            in_degree_zero = sorted([n for n, i in G.in_degree
                                     if i == 0])
            assert len(in_degree_zero) > 0

            order += in_degree_zero
            G.remove_nodes_from(in_degree_zero)

            if len(G) == 0:
                break
        return order

    def break_cycle(cycle):
        """Break `cycle`, beginning with the first variable from an alphabetical sort."""
        first = cycle.index(sorted(cycle)[0])
        return cycle[first:] + cycle[:first]


    # Store the list of nodes to an outer list; grouped into simple cycles
    # (shortest to longest) if not a directed acyclic graph
    if nx.is_directed_acyclic_graph(G):
        node_groups = [G.nodes()]
    elif nx.is_strongly_connected(G):
        node_groups = sorted(nx.simple_cycles(G), key=len)
    else:
        raise ValueError('Input graph must be either '
                         'a directed acyclic graph or '
                         'a strongly connected component')

    nested_order = []
    already_encountered = set()
    for i, group in enumerate(node_groups):
        # Remove nodes from the current group if they appear in a
        # previously-encountered cycle
        group = [node for node in group if node not in already_encountered]

        # Break if `group` is empty (all nodes already accounted for in
        # previous cycles; nothing left to unravel)
        if not len(group):
            break

        # Update list of already-encountered nodes
        already_encountered = already_encountered.union(set(group))

        # Get the subgraph of the remaining nodes and either...
        remainder = G.subgraph(group).copy()
        # Sort topologically, if a directed acyclic graph remains, or...
        if nx.is_directed_acyclic_graph(remainder):
            order = order_dag(remainder)
        # ...break the cycle
        else:
            cycles = list(nx.simple_cycles(remainder))
            assert len(cycles) == 1
            order = break_cycle(cycles[0])

        nested_order.append(order)

    return nested_order
