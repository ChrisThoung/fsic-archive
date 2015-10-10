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
        'Y[0]',
        equations=['Y[0] = C[0] + G[0]'], functions=[name])
    expected.add_edge('C[0]', 'Y[0]')
    expected.add_edge('G[0]', 'Y[0]')

    expected.add_node(
        'YD[0]',
        equations=['YD[0] = Y[0] - T[0]'], functions=[name])
    expected.add_edge('Y[0]', 'YD[0]')
    expected.add_edge('T[0]', 'YD[0]')

    expected.add_node(
        'T[0]',
        equations=['T[0] = theta[0] * Y[0]'], functions=[name])
    expected.add_edge('theta[0]', 'T[0]')
    expected.add_edge('Y[0]', 'T[0]')

    expected.add_node(
        'C[0]',
        equations=['C[0] = alpha_1[0] * YD[0] + alpha_2[0] * H[-1]'], functions=[name])
    expected.add_edge('alpha_1[0]', 'C[0]')
    expected.add_edge('YD[0]', 'C[0]')
    expected.add_edge('alpha_2[0]', 'C[0]')
    expected.add_edge('H[-1]', 'C[0]')

    assert nx.is_isomorphic(G, expected, node_match=dict.__eq__)


if __name__ == '__main__':
    import nose
    nose.runmodule()
