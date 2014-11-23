.. _example-spec:

***********************************************
Specifying Godley and Lavoie's (2007) Model SIM
***********************************************

This section is the second part of the example, to show how to specify Godley
and Lavoie's (2007) *Model SIM* and conduct numerical simulations.

The example below reflects the typical use case, of a user with their model
specification stored to a `Pandoc Markdown`_ file. This file simultaneously
specifies the model for use with FSIC and provides documentation on the economic
theory that underpins that model.

.. _`Pandoc Markdown`: http://johnmacfarlane.net/pandoc/README.html#pandocs-markdown

The example below first shows how the equations of the model should be specified
as code blocks. This is followed by an explanation of the layout of the input
Markdown file.

.. Note::

   Strictly, the Markdown-specific features of FSIC only concern the format
   necessary to identify and extract code blocks from a text file that mixes
   such code blocks with other text and markup. FSIC then translates these code
   blocks into Python objects and passes the objects to code to convert the
   information into model components.

   Consequently, there is no particular reason why a model must be specified in
   Markdown, this format is simply one of the more user-friendly (and
   easily-documented) methods for developing a model.

   As long as model components are supplied as either the necessary intermediate
   Python objects or as Markdown-like code blocks, the precise source of the
   user-written code is irrelevant.


.. _example-spec-equations:

Model equations
===============

Below are the 11 equations that make up *Model SIM*, as well as the twelfth
'redundant' or 'hidden' equation.


.. _example-spec-equations-ds:

Equalising demand and supply
----------------------------

The first four equations of the model equalise demands and supplies:

.. math::
   :label: sd-consumption

   C_s = C_d

.. math::
   :label: sd-government

   G_s = G_d

.. math::
   :label: sd-taxes

   T_s = T_d

.. math::
   :label: sd-labour

   N_s = N_d

The code that specifies the above four equations for use in FSIC closely
resembles the above, requiring a 'fenced' code block in a Markdown file as
follows::

	```{.python}
	C_s = C_d
	G_s = G_d
	T_s = T_d
	N_s = N_d
	```

In the above block, the code is 'fenced' at the beginning and end by three
backticks (`````) on a new line. Three tildes (``~``) may also form a valid
fence but the same characters must begin and end the code block. It is not valid
to mix backticks and tildes either within or between a pair of fences.

The equations themselves lie between the fences and closely resemble the way
they might be written in a document.

The opening fence is immediately followed by an attributes block, marked by
braces (``{``, ``}``). The attributes block must contain at least one attribute
that identifies the programming language of the code block. For inclusion as a
set of one or more model equations, a code block *must* be identified as a
Python code block (``.python``). FSIC recognises a number of other attributes
that provide additional control over the creation of the final model. More
information on these attributes is covered in a separate section.


.. _example-spec-equations-income:

Disposable income
-----------------

Disposable income (*YD*) is defined as the wage bill earned by households, less
taxes:

.. math::
   :label: income

   YD = W . N_s - T_s

where taxes are levied as a fixed proportion of money income, at rate |theta|:

.. math::
   :label: taxation

   T_d = \theta . W. N_s \qquad \theta < 1

.. |theta| replace:: :math:`\theta`

The code block for these two equations follows a similar format to that of the
previous one, with dots replaced with ``*`` for multiplication::

	```{.python}
	YD = W * N_s - T_s
	T_d = theta * W * N_s
	```


.. _example-spec-equations-consumption:

Consumption function
--------------------

Household consumption is a function of current disposable income (*YD*, as
described above) and past accumulated wealth (|H[-1]|):

.. math::
   :label: consumption

   C_d = \alpha _1 . YD + \alpha _2 . H_{h-1} \qquad 0 < \alpha _1 < \alpha _2 < 1

.. |H[-1]| replace:: :math:`H_{-1}`

In the Markdown file, this should appear as follows::

	```{.python}
	C_d = alpha_1 * YD + alpha_2 * H_h[-1]
	```

This is the first equation to include variables that relate a period other than
the current one (the lagged household wealth term |H[-1]|). The variable ``H_h``
refers to household wealth and the previous period's value is denoted by the
``[-1]`` index.

.. Note::
   Where a period index (such as ``H_h[-1]``) is *not* given, FSIC makes the
   assumption that the variable referenced is the one for the current
   period. This saves the user from having to write expressions such as
   ``C_d[0]`` when ``C_d`` will do.

   Period indices may be any integer value, where negative numbers indicate lags
   (past periods), zeroes indicate the current period, and positive numbers
   indicate leads (future periods).


.. _example-spec-balances:

Financial balances
------------------

The following two equations describe the evolution of household and government
financial stocks.

.. math::
   :label: government-debt

   \Delta H_s = H_s - H_{s-1} = G_d - T_d

.. |H_s| replace:: :math:`H_s`

.. math::
   :label: household-wealth

   \Delta H_h = H_h - H_{h-1} = YD - C_d

Because FSIC does not yet support difference operators, these equations must be
specified as follows::

	```{.python}
	H_s = H_s[-1] + G_d - T_d
	H_h = H_h[-1] + YD - C_d
	```

.. important::
   FSIC does not yet support the use of difference operators in model
   equations. All relationships must use the untransformed variable name.


.. _example-spec-output-employment:

Output and employment
---------------------

The final two equations of the model are as follows:

.. math::
   :label: output

   Y = C_s + G_s

.. math::
   :label: labour

   N_d = \frac{Y}{W}

and specified as::

	```{.python}
	Y = C_s + G_s
	N_d = Y / W
	```


.. _example-spec-redundant:

The redundant equation
----------------------

The final equation is the 'redundant', or 'hidden' equation.

.. math::
   \Delta H_h = \Delta H_s

This equation does not feature in the model solution, but may be useful for
diagnostic purposes (by verifying that the implicit equality does indeed hold).

This can be specified as follows (again, without the difference operators)::

	```{.python .hidden}
	H_h = H_s
	```

.. Important::
   There can only be one code block with the ``.hidden`` attribute. This code
   block can only contain one expression, on a single line.

.. Note::
   Either ``.hidden`` or ``.redundant`` can be used as attributes to denote this
   equation.


.. _example-spec-markdown-file:

The complete Markdown file
==========================

A bare-bones Markdown file for the model, with no explanatory text or
documentation, looks as follows::

    ```{.ini}
    NAME = SIM
    DESCRIPTION = The simplest model with government money
    REFERENCE = Godley, W., Lavoie, M. (2007), *Monetary economics: an integrated approach to credit, money, income, production and wealth*, Palgrave Macmillan
    MAJOR = 0
    MINOR = 1
    PATCH = 0
    DEV = No
    ```

    ```{.python}
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
    N_d = Y / W
    ```

    ```{.python .hidden}
    H_h = H_s
    ```

The file consolidates the model equations into the second code block, with the
'hidden' equation in its own block (in order to have the special ``.hidden``
attribute).

The first code block is new and provides additional information about the
model. This information is not critical for the example shown here but, for more
complicated 'production-quality' models, such information is important. The
attributes block for this first section identifies the language as ``.ini``, to
denote the INI/configuration file format. Each line in this section represents a
pair of values, separated by the leftmost equals (``=``) sign.

The table below explains each set of values in turn:

.. csv-table:: Descriptive information about a model
   :header: Key, Type, Description
   :widths: 10, 5, 30

   NAME, String, "The name of the model"
   DESCRIPTION, String, "A short description of the model"
   REFERENCE, String, "A reference to more detailed documentation, where applicable"
   MAJOR, Integer, "The major version number (by Semantic Versioning 2.0.0)"
   MINOR, Integer, "The minor version number (by Semantic Versioning 2.0.0)"
   PATCH, Integer, "The patch number (by Semantic Versioning 2.0.0)"
   DEV, Yes/No, "Whether or not the model is still in development"

For a complete version of the Markdown file, as it might be used in practice
(i.e. with accompanying documentation) see ``examples/gl2007/3_SIM.md``.


.. _example-spec-build:

Generating a model script
=========================

Having written a Markdown file, the equations must be converted into a Python
script to run the model.

Assuming the code block in the section above has been saved to a file with name
``sim.md``, and with FSIC installed, the model script can be generated by the
following command-line call::

    python fsic.py build -o sim.py sim.md

The first two part of the call (``python fsic.py``) runs the main FSIC
program. The first argument to the program is ``build``, to construct a new
model from one or more input files.

The second argument (``-o sim.py``) sets the output file for the model to
``sim.py``. The third and final argument is the path of the input file
containing the model equations in Markdown format.

This will create a new file (or overwrite the existing one) with name
``sim.py``.

This script is a standalone Python script, operating like any other command-line
tool. For example, the following call at the command line::

    python sim.py -h

will display the help information::

    usage: sim.py [-h] [-V] {solve} ...

    Class definition for SIM: The simplest model with government money.

    optional arguments:
      -h, --help     show this help message and exit
      -V, --version  show program's version number and exit

    commands:
      {solve}
        solve        solve the model

While the following::

    python sim.py -V

will print version information about the current script::

    Model version: 0.1.0
    Built under FSIC version: 0.1.0
    FSIC version installed: 0.1.0

The next section explains how to run this model.
