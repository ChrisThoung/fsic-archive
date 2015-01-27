.. _bonnet-solution:

************************
FSIC internals: Solution
************************

This section provides further technical information on the internals of a
FSIC-generated model. Specifically, this section concerns the model object and
the various stages of the solution. For regular use, these steps are handled by
the model script when it is called from the command line.


.. _bonnet-solution-introduction:

Introduction
============

The solution of a model comprises the following key steps:

1. Initialisation
2. Setup
3. Solution


.. _bonnet-solution-initialisation:

Initialisation
==============

The initialisation of a model is simply the instantiation of a new model
object. This requires a span to be defined, in order to also initialise the
individual model variables. For example, for an annual-frequency instance of a
previously-generated model with name ``ExampleModel`` (which may need to be
imported, along with the pandas ``PeriodIndex`` object)::

    model = ExampleModel()
    span = PeriodIndex(start='1954', end='2015')
    model.initialise(span=span)

A slight more complex case is where the solution period differs from the
complete span of the model (e.g. because of the need for lagged variables)::

    model = ExampleModel()
    span = PeriodIndex(start='2000Q1', end='2014Q4')
    model.initialise(span=span, solve_from='2001Q1')

In the above example, the model has been initialised to for the period 2000Q1
to 2014Q4 but its default start period for actual solution is 2001Q1.


.. _bonnet-solution-setup:

Setup
=====


.. _bonnet-solution-solution:

Solution
========
