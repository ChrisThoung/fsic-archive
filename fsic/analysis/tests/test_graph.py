# -*- coding: utf-8 -*-
"""
test_graph
==========
Test FSIC graph analysis code.

"""

import itertools

import networkx as nx
import networkx.algorithms.isomorphism as iso

import nose
import fsic.analysis.graph


XP_G = nx.DiGraph()
XP_G.add_edges_from([('C_d', 'C_s'),
                     ('G_d', 'G_s'),
                     ('T_d', 'T_s'),
                     ('N_d', 'N_s'),
                     ('W', 'YD'), ('N_s', 'YD'), ('T_s', 'YD'),
                     ('theta', 'T_d'), ('W', 'T_d'), ('N_s', 'T_d'),
                     ('alpha_1', 'C_d'), ('YD', 'C_d'), ('alpha_2', 'C_d'), ('H_h[-1]', 'C_d'),
                     ('H_s[-1]', 'H_s'), ('G_d', 'H_s'), ('T_d', 'H_s'),
                     ('H_h[-1]', 'H_h'), ('YD', 'H_h'), ('C_d', 'H_h'),
                     ('C_s', 'Y'), ('G_s', 'Y'),
                     ('Y', 'N_d'), ('W', 'N_d'), ])
nx.set_node_attributes(XP_G,
                       name='equations',
                       values={'C_s': ('C_s = C_d', ),
                               'C_d': ('C_d = alpha_1 * YD + alpha_2 * H_h[-1]', ),
                               'G_s': ('G_s = G_d', ),
                               'G_d': (),
                               'T_s': ('T_s = T_d', ),
                               'T_d': ('T_d = theta * W * N_s', ),
                               'N_s': ('N_s = N_d', ),
                               'N_d': ('N_d = Y / W', ),
                               'YD': ('YD = W * N_s - T_s', ),
                               'W': (),
                               'theta': (),
                               'alpha_1': (),
                               'alpha_2': (),
                               'H_h[-1]': (),
                               'H_s': ('H_s = H_s[-1] + G_d - T_d', ),
                               'H_s[-1]': (),
                               'H_h': ('H_h = H_h[-1] + YD - C_d', ),
                               'Y': ('Y = C_s + G_s', ), })
SIM = '''\
C_s = C_d
G_s = G_d
T_s = T_d
N_s = N_d

YD = W * N_s - T_s
T_d = theta * W * N_s

C_d = alpha_1 * YD + alpha_2 * H_h[-1]

H_s = H_s[-1] + G_d - T_d
H_h = H_h[-1] + YD - C_d

Y = C_s + G_s
N_d = Y / W'''

XP_ORDER = [
    'G_s = G_d',

    'C_d = alpha_1 * YD + alpha_2 * H_h[-1]',
    'C_s = C_d',
    'Y = C_s + G_s',
    'N_d = Y / W',
    'N_s = N_d',
    'YD = W * N_s - T_s',

    'T_d = theta * W * N_s',
    'T_s = T_d',

    'H_h = H_h[-1] + YD - C_d',
    'H_s = H_s[-1] + G_d - T_d']


def test_make_graph_list():
    nm = iso.categorical_node_match('equations', '')

    G = fsic.analysis.graph.make_graph(SIM)
    assert nx.is_isomorphic(G, XP_G, node_match=nm)

    G = fsic.analysis.graph.make_graph(SIM.split('\n'))
    assert nx.is_isomorphic(G, XP_G, node_match=nm)

def test_make_graph_disconnected():
    G = fsic.analysis.graph.make_graph(['Y = C + I + G + X - M',
                                        'pi = 0.02'])
    assert sorted(G.nodes()) == ['C', 'G', 'I', 'M', 'X', 'Y', 'pi']

def test_topological_sort():
    order = list(itertools.chain.from_iterable(
        fsic.analysis.graph.topological_sort(XP_G)))

    assert len(order) == len(XP_ORDER)

    # Print comparison between result and expected order, if equality assertion
    # fails
    pad_match = 10
    pad_width = max([len(x) for x in XP_ORDER]) + 4
    print('\n** Output from `fsic.analysis.graph.topological_sort()` test **\n')
    print('MATCH?'.ljust(pad_match), 'EXPECTED:'.ljust(pad_width), 'RESULT:')
    for xp, result in zip(XP_ORDER, order):
        print(('Yes' if xp == result else 'No').ljust(pad_match),
              xp.ljust(pad_width), result)

    assert order == XP_ORDER

def test_topological_sort_fully_nested_cycles():
    # Test topological sort on a system in which the subgraphs of cycles, when
    # connected, encompass the larger cycle subgraphs
    #
    # (Added as a test because an earlier version of the algorithm assumed that
    # looping through the cycles, from smallest to largest, would always leave
    # *some* graph available to unravel in the last iteration. This would lead
    # to a null graph which other [internal] functions cannot operate on. The
    # revised implementation keeps eliminating cycle nodes from the graph until
    # the graph is empty. Rather than attempt to continue through the loop, the
    # algorithm simply halts and moves on to the next stage.)
    G = nx.DiGraph()
    G.add_edges_from([('B', 'A'), ('C', 'A'),
                      ('A', 'B'), ('C', 'A'),
                      ('A', 'C')])
    nx.set_node_attributes(G, name='equations',
                           values={'A': ('A = B + C', ),
                                   'B': ('B = A + C', ),
                                   'C': ('C = A', )})

    # Two possible orders
    expected_1 = [['A = B + C', 'C = A', 'B = A + C']]
    expected_2 = [['A = B + C', 'B = A + C', 'C = A']]
    print('''\
EXPECTED: {}
      OR: {}'''.format(expected_1, expected_2))

    order = fsic.analysis.graph.topological_sort(G)
    print('RESULT:  ', order)

    assert order == expected_1 or order == expected_1


def test_unravel_graph():
    # Test cycle detection and graph unravelling
    # (Originally added to check for no duplicate nodes across cycles.)
    G = nx.DiGraph()
    G.add_edges_from([('A', 'B'), ('B', 'C'), ('C', 'D'), ('D', 'A'),
                      ('X', 'Y'), ('Y', 'Z'), ('Z', 'A'), ('A', 'B'), ('B', 'X'), ])
    assert fsic.analysis.graph._unravel_graph(G) == [['A', 'B', 'C', 'D'], ['X', 'Y', 'Z']]


if __name__ == '__main__':
    nose.runmodule()
