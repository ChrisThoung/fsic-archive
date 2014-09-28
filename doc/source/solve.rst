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


.. _input-data:

Input data
----------
