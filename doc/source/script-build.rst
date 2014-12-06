.. _script-build:

**********************
FSIC script: ``build``
**********************

This section provides further documentation on the FSIC ``build`` system. In
most cases the user will interact with the system through the ``fsic.py``
script.


.. _script-build-optimise-order:

Solution-order optimisation
===========================

The user's input Markdown file(s) for a model will tend to favour clarity of
expression in the order of presentation of the equations over efficiency of
solution. For this reason, the order that the equations appear in the file(s)
will not necessarily yield the fastest solution in terms of the number of
iterations to convergence.

FSIC includes an algorithm to re-order a set of equations to, as far as
possible, minimise the likely number of iterations to convergence for any
single period of the model. This algorithm draws on the principles of graph
theory/network analysis.

One way to analyse a model is to think of it as a directed graph. By this
method, the nodes (vertices) of the graph correspond to the variables in the
model. The edges represent the relationships between the models in terms of
which variables are determinants of others.

As an example, take the consumption function of Godley and Lavoie's (2007)
*Model SIM*:

.. math::
   C_d = \alpha _1 . YD + \alpha _2 . H_{h-1} \qquad 0 < \alpha _1 < \alpha _2 < 1

This comprises:

* An endogenous (left-hand side) variable: |C_d|
* Four exogenous (right-hand side) variables (at least from the point of view
  of this equation):
    * Two parameters: |alpha_1|, |alpha_2|
    * Two 'drivers': |YD|, |H_h[-1]|

.. |C_d| replace:: :math:`C_d`

.. |alpha_1| replace:: :math:`\alpha_1`
.. |alpha_2| replace:: :math:`\alpha_2`

.. |YD| replace:: :math:`YD`
.. |H_h[-1]| replace:: :math:`H_{h-1}`

Represented as a graph, the |C_d| node has an in-degree of four, with edges
directed from the right-hand side variables to |C_d|. The right-hand side
variables have in-degrees of zero and out-degrees of one.

Adding another equation to the system, for disposable income:

.. math::
   YD = W . N_s - T_s

The |YD| variable now has an in-degree of three (because it now depends on |W|,
|N_s| and |T_s|) and continues to have an out-degree of one.

.. |W| replace:: :math:`W`
.. |N_s| replace:: :math:`N_s`
.. |T_s| replace:: :math:`T_s`

Continuing this process and including the other equations of *Model SIM* yields
a graph like the following:

.. image:: _static/gl2007-sim-graph.png

As described, endogenous variables are those with a positive in-degree; they
may have a positive out-degree i.e. they influence other parts of the
system. Exogenous variables have zero in-degree (their values are not
determined by the system) and positive out-degree i.e. they influence other
parts of the system.

From the above, it is possible to implement an algorithm to re-order a model's
equations, on the basis that endogenous variables that depend on relatively
fewer other endogenous variables should solve first. This is the basis of the
reordering algorithm in FSIC's equation-reordering function:

.. autofunction:: FSIC.optimise.order.recursive
