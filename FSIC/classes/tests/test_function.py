# -*- coding: utf-8 -*-


import networkx.algorithms.isomorphism as iso
import networkx as nx

from FSIC.classes.schematic import Function


def test_to_graph():
    name = 'Test'
    fn = Function(name)
    fn.parse(['Y = C + G',
              'YD = Y - T',
              'T = theta * Y',
              'C = alpha_1 * YD + alpha_2 * H[-1]', ])
    G = fn.to_graph()

    expected = nx.DiGraph()

    expected.add_node(
        'Y[period]',
        equations=['Y[period] = C[period] + G[period]'], functions=[name])
    expected.add_edge('C[period]', 'Y[period]')
    expected.add_edge('G[period]', 'Y[period]')

    expected.add_node(
        'YD[period]',
        equations=['YD[period] = Y[period] - T[period]'], functions=[name])
    expected.add_edge('Y[period]', 'YD[period]')
    expected.add_edge('T[period]', 'YD[period]')

    expected.add_node(
        'T[period]',
        equations=['T[period] = theta[period] * Y[period]'], functions=[name])
    expected.add_edge('theta[period]', 'T[period]')
    expected.add_edge('Y[period]', 'T[period]')

    expected.add_node(
        'C[period]',
        equations=['C[period] = alpha_1[period] * YD[period] + alpha_2[period] * H[period-1]'], functions=[name])
    expected.add_edge('alpha_1[period]', 'C[period]')
    expected.add_edge('YD[period]', 'C[period]')
    expected.add_edge('alpha_2[period]', 'C[period]')
    expected.add_edge('H[period-1]', 'C[period]')

    assert nx.is_isomorphic(G, expected, node_match=dict.__eq__)


if __name__ == '__main__':
    import nose
    nose.runmodule()
