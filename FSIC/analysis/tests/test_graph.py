# -*- coding: utf-8 -*-
"""
test_graph
==========
Test FSIC graph analysis code.

"""

import networkx as nx
import networkx.algorithms.isomorphism as iso

import nose
import FSIC.analysis.graph


XP = nx.DiGraph()
XP.add_edges_from([('C_d', 'C_s'),
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
nx.set_node_attributes(XP, 'equations',
                       {'C_s': ('C_s = C_d', ),
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


def test_make_graph_list():
    nm = iso.categorical_node_match('equations', '')

    G = FSIC.analysis.graph.make_graph(SIM)
    assert nx.is_isomorphic(G, XP, node_match=nm)

    G = FSIC.analysis.graph.make_graph(SIM.split('\n'))
    assert nx.is_isomorphic(G, XP, node_match=nm)


if __name__ == '__main__':
    nose.runmodule()
