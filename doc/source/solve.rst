.. _solve:

*************
Solve a model
*************

A command-line call to ``fsic.py build`` on a Markdown file generates a Python
script to solve the model. Like the core ``fsic`` script, the model file is
intended to be run from the command line.


.. _command-format:

Command format
==============

As with ``fsic.py``, help on the model command-line arguments can be accessed
with the ``-h`` argument. In the case of Godley and Lavoie's (2007) SIM model::

    usage: sim.py [-h] [-V] {solve} ...

    Class definition for SIM: The simplest model with government money.

    optional arguments:
      -h, --help     show this help message and exit
      -V, --version  show program's version number and exit

    commands:
      {solve}
	solve        solve the model


.. _command-solve:

Command: Solve
==============

A model's ``solve`` arguments are as follows, again using Godley and
Lavoie's (2007) SIM model::

    usage: sim.py solve [-h] [-v] [-f INPUT [INPUT ...]] [-o OUTPUT [OUTPUT ...]]
			 [-D PARAMETER [PARAMETER ...]]
			 [--set EXPRESSION [EXPRESSION ...]]
			 [--span PERIOD PERIOD] [--past PERIOD]

    optional arguments:
      -h, --help            show this help message and exit
      -v, --verbose         print detailed solution output (not yet implemented)
      -f INPUT [INPUT ...], --input INPUT [INPUT ...]
			    input file(s) for model data
      -o OUTPUT [OUTPUT ...], --output OUTPUT [OUTPUT ...]
			    output file(s) for model results
      -D PARAMETER [PARAMETER ...], --define PARAMETER [PARAMETER ...]
			    set (time-invariant) model parameters
      --set EXPRESSION [EXPRESSION ...]
			    set (time-varying) model variables prior to run
      --span PERIOD PERIOD  set the start and end periods of the model run
      --past PERIOD         set the first historical period of the model run


.. _output-results:

Output results
--------------

In order to write the model results to one or more output files, supply ``-o``
or ``--output`` and one or more filepaths to the command-line call::

    python sim.py --output results.csv

The call above saves the model results to ``results.csv``. The file extension of
the output file determines the format of the output data. Multiple files can be
passed::

    python sim.py --output results1.csv results2.csv

The following output-file formats are currently supported:

=====================  ==============  ==================
Type                   File extension  Can be compressed?
=====================  ==============  ==================
Comma-separated value            .csv                  No
=====================  ==============  ==================

.. important::
   If no output file is specified, no results will be saved at the end of the
   model run


.. _solution-arguments:

Solution arguments
------------------

Required
~~~~~~~~

In order to run the model, the user must, at a minimum, supply the span of the
solution period, comprising:

* A start period
* An end period

These can be set as follows::

    python sim.py --span 0 100

which sets the solution period from 0 to 100 inclusive.

Optional
~~~~~~~~

In addition to the `--span`` argument, the user may optionally supply a start
period for the 'past', the period(s) prior to the start period. The model will
not solve over these periods, but they may be necessary to ensure enough lags
for the early periods of a dynamic model e.g. in order to ensure the presence of
values for period -1 when solving for period 0.

For example::

    python sim.py --span 0 100 --past -5

sets the solution period from 0 to 100 inclusive, but also initialises the
periods -5 to -1 inclusive. By default, these past periods are not solved; it is
up to the user to supply data for these periods.

.. important::
   The ``--past`` period must come before the start period in the ``--span``
   argument.

Finally, the model script provides some limited functionality to set model
parameters and data from the command line. This allows the user to quickly alter
model inputs for small 'toy' models but is unsuitable for more complicated,
data-driven models, where it is preferable to maintain a separate database (see
next section).

There are currently two commands available:

* ``-D``/``--define``: to fix a variable over the entire solution period e.g. a
  model parameter
* ``--set``: to assign values to a variable using a Python expression

The ``--D`` (or ``--define``) argument allows the user to fix the value of one
or more variables with an expression of the form ``var_name = some_value``. For
example::

    alpha_1 = 0.6

where ``var_name`` is ``alpha_1`` and ``some_value`` is ``0.6``.

Multiple assignments are possible, such that the following is a valid
command-line call::

    python sim.py -D alpha_1=0.6 alpha_2=0.4

The above statement sets:

* The variable ``alpha_1`` to ``0.6``
* The variable ``alpha_2`` to ``0.4``

The ``--set`` argument differs because it allows the user to change a variable's
value over the course of the solution period. The syntax in this case must
resemble a statement that modifies selected elements of a pandas Series object,
such as::

    python sim.py --set G_d[1:]=20

which sets the variable ``G_d`` to ``20`` from period 1 onwards.


.. _input-data:

Input data
----------

In all but the simplest cases, it is infeasible to specify all input data to a
model using the ``solve`` command's ``PARAMETER`` and ``EXPRESSION``
arguments. Instead, it is normally preferable to supply one or more files of
input data, indexed by time. This is purpose of the ``INPUT`` argument.

The data that must eventually enter the model must be structured as a pandas
DataFrame object but FSIC provides facilities to construct such a database from
a variety of input-file formats. FSIC will attempt to automatically detect the
file type based on the file extensions in the filepath.

In the simplest case, the user can provide a file of delimiter-separated tabular
data e.g. a CSV or TSV file::

    C,I,G,X,M
    105.00,30.50,30.00,25.00,40.50
    107.68,31.29,30.90,25.44,41.55
    110.42,32.09,31.83,25.88,42.63
    113.24,32.92,32.78,26.34,43.74
    116.13,33.76,33.77,26.80,44.88
    119.09,34.63,34.78,27.27,46.05
    122.12,35.51,35.82,27.74,47.24
    125.24,36.41,36.90,28.23,48.47
    128.43,37.33,38.00,28.72,49.73
    131.71,38.28,39.14,29.22,51.02

As a table, this would appear as follows:

======  =====  =====  =====  =====
     C      I      G      X      M
======  =====  =====  =====  =====
105.00  30.50  30.00  25.00  40.50
107.68  31.29  30.90  25.44  41.55
110.42  32.09  31.83  25.88  42.63
113.24  32.92  32.78  26.34  43.74
116.13  33.76  33.77  26.80  44.88
119.09  34.63  34.78  27.27  46.05
122.12  35.51  35.82  27.74  47.24
125.24  36.41  36.90  28.23  48.47
128.43  37.33  38.00  28.72  49.73
131.71  38.28  39.14  29.22  51.02
======  =====  =====  =====  =====

It is not necessary for the data to cover the entirety of the model span
(allowing the user to alter the span of the solution period without necessarily
having to extend the dataset). However, depending on the model specification,
values may be necessary to achieve a (plausible) solution.

Having saved an input file to, for example, ``data.csv``, the model can be
solved from the command line using these data as follows::

    python sim.py -f data.csv

The user can specify multiple input files::

    python sim.py -f data1.csv data2.csv

and the files need not be of the same format::

    python sim.py -f data1.csv data2.tsv

``--input`` can be used instead of ``-f`` as an argument::

    python sim.py --input data1.csv data2.tsv

The following input-file formats are currently supported:

=====================  ==============  ==================
Type                   File extension  Can be compressed?
=====================  ==============  ==================
Comma-separated value            .csv                 Yes
Tab-separated value              .tsv                 Yes
=====================  ==============  ==================
