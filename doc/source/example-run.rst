.. _example-run:

***********************************************
Simulating Godley and Lavoie's (2007) Model SIM
***********************************************

This section is the second part of the example, to show how to specify Godley
and Lavoie's (2007) *Model SIM* and conduct numerical simulations.

The example below reflects the typical use case, of a user with their model
specification stored to a `Pandoc Markdown`_ file. This file simultaneously
specifies the model for use with FSIC and provides documentation on the economic
theory that underpins that model.

.. _`Pandoc Markdown`: http://johnmacfarlane.net/pandoc/README.html#pandocs-markdown

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


.. _example-run-equations:

Model equations
===============

Below are the 11 equations that make up *Model SIM*, as well as the twelfth
'redundant' or 'hidden' equation.


.. _example-run-equations-ds:

Equalising demand and supply
----------------------------

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


.. _example-run-equations-income:

Disposable income
-----------------

.. math::
   :label: income

   YD = W . N_s - T_s

.. math::
   :label: taxation

   T_d = \theta . W. N_s \qquad \theta < 1

.. |theta| replace:: :math:`\theta`


.. _example-run-equations-consumption:

Consumption function
--------------------

.. math::
   :label: consumption

   C_d = \alpha _1 . YD + \alpha _2 . H_{h-1} \qquad 0 < \alpha _1 < \alpha _2 < 1

.. |H[-1]| replace:: :math:`H_{-1}`


.. _example-run-balances:

Financial balances
------------------

.. math::
   :label: government-debt

   \Delta H_s = H_s - H_{s-1} = G_d - T_d

.. |H_s| replace:: :math:`H_s`

.. math::
   :label: household-wealth

   \Delta H_h = H_h - H_{h-1} = YD - C_d


.. _example-run-output-employment:

Output and employment
---------------------

.. math::
   :label: output

   Y = C_s + G_s

.. math::
   :label: labour

   N_d = \frac{Y}{W}


.. _example-run-redundant:

The redundant equation
----------------------

.. math::
   \Delta H_h = \Delta H_s
