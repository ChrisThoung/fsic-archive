.. _specify:

***************
Specify a model
***************


.. _gl2007-sim:

Godley and Lavoie (2007): Model SIM
===================================

This section illustrates how to specify a model using a Markdown-formatted text
file. The example used is Model SIM, from Chapter 3 of Godley and Lavoie
(2007). A complete version of the Markdown file, along with further explanation
of the model's relationships, can be found in ``examples/gl2007/3_SIM.md``,
which accompanies this release of FSIC.

This section first presents the model, before explaining how to specify these
relationships as a Markdown file.

.. _gl2007-sim-model:

The model
---------

.. _gl2007-flows:

Behavioural (transactions) matrix
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The table below presents the behavioural transactions-flow matrix for the
model. The columns indicate institutional sectors of the model economy while the
rows indicate flows of funds between these sectors. For example, the first row
shows how funds flow *from* Households *to* firms (Production) in exchange for
consumption goods and services.

Behavioural (transactions) matrix for Model SIM:

=============================  ===========  ===========  ===========
Flow                            Households   Production   Government
=============================  ===========  ===========  ===========
Consumption                           -C_d         +C_s
Government expenditures                            +G_s         -G_d
[Output]                                            [Y]
Factor income (wages)               +W.N_s       -W.N_d
Taxes                                 -T_s                      +T_d
Change in the stock of money       -D(H_h)                   +D(H_s)
=============================  ===========  ===========  ===========

Source: Godley and Lavoie (2007), Table 3.3.

As defined, it is a requirement of the transactions matrix that the elements in
each row should sum to zero, indicating that every outflow from a sector is
matched by a corresponding inflow to another sector. There are no 'black holes'.

Similarly, within sectors (the columns), all inflows and outflows must sum to
zero. In the case of the columns, this is achieved by any surpluses or
shortfalls in funds translating into a change in a sector's stock of money (Row
6). Thus, should Households' consumption exceed their disposable income,
Households' stock of money must decrease, to cover the shortfall in
income. Conversely, should Households' consumption be less than their income,
their stock of money should rise as a consequence of their saving.

Similarly, Government budget surpluses (a flow) translate into reductions in
(the stock of) Government debt while a budget deficit will increase public
debt. In this simple model, money is the only financial asset/liability,
providing Households with a vehicle for saving and the Government with a means
to issue debt.

In this simple economy, firms are assumed to hold no cash: their receipts from
sales equal their labour costs each period. As such, the Production sector holds
neither assets or liabilities at the start or end of each period.


.. _gl2007-sim-ds:

Equations to equalise demand and supply
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The following equations equalise demands and supplies in the economy.

Consumption expenditure:

.. math::
   C_s = C_d

Government expenditure:

.. math::
   G_s = G_d

The implicit assumption that underpins these first two equations is that of the
Keynesian or Kaleckian quantity adjustment mechanism. By this mechanism,
production is the flexible element in the market, providing as much output as is
required, on demand. Furthermore, there are no inventories, such that output is
equal to purchases.

Taxes:

.. math::
   T_s = T_d

Labour:

.. math::
   N_s = N_d

This last equation, like the first two, implies no supply constraints in the
economy. In the case of labour, the underlying assumption is that of a 'reserve
army of unemployed workers, all eager to work at the going wage, whenever their
labour services are demanded' (Godley and Lavoie 2007, Page 63). Godley and
Lavoie (2007) stress that such a situation is *not* one of full employment in
the economy; rather, the supply of labour adjusts to the demand for labour.


.. _gl2007-sim-yd:

Disposable income
~~~~~~~~~~~~~~~~~

In Model SIM, disposable income is wage income to households less taxes:

.. math::
   YD = W.N_s - T_s

with taxes set at a fixed proportion of that wage income:

.. math::
   T_d = \theta . W . N_s \qquad \theta < 1


.. _gl2007-sim-c:

Household consumption
~~~~~~~~~~~~~~~~~~~~~

Household consumption depends on the influences of:

* Current disposable income, which is assumed to be accurately known by
  households when they make their consumption decisions
* Past accumulated wealth

.. math::
   C_d = \alpha_1 . YD + \alpha_2 . H_{h-1} \qquad 0 < \alpha_2 < \alpha_1 < 1


.. _gl2007-sim-stocks:

Changes in stocks
~~~~~~~~~~~~~~~~~


.. _gl2007-sim-markdown:

Markdown
--------

Markdown_ is a formatting syntax that is intended to be easy to read even in its
plain text form, while being suitable for conversion to other formats
(principally HTML). Pandoc_ is a tool that implements a variant of Markdown and
allows for conversion to a range of output formats, including PDF and Microsoft
Word ``docx``.

.. _Markdown: http://daringfireball.net/projects/markdown/
.. _Pandoc: http://pandas.pydata.org/

Markdown allows text to be interspersed by code blocks. For this reason,
Markdown is the input-file format that has been chosen to specify models for
FSIC:

#. The user can document their model using text and LaTeX as necessary,
   alongside the actual code blocks that will define the model i.e. all code and
   documentation is in **one** place
#. The model specification is easily converted to alternative formats for
   publishing/dissemination
#. As a text file, the model specification is easily shared and version
   controlled

In these respects, a model specified in this way facilitates replication and
thus reproducible research. The rationale for ``R Markdown`` (which has informed
some of the implementation of FSIC in this respect) is similar: to intersperse
exposition and explanation with the actual code to carry out statistical
analysis in ``R``.
