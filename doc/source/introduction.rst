.. _introduction:

************
Introduction
************

FSIC (Flows and Stocks Integrated Consistently) is a Python_ package for the
specification, solution and analysis of Stock-Flow Consistent macroeconomic
models in the tradition of Wynne Godley.

While FSIC provides a library of Python code to build macroeconomic models from
scratch, for most users, it is more convenient to specify a model in one or more
files formatted in Markdown_.

Markdown files can contain both the code blocks that define the model and
explanatory text. An excerpt from such a file might look as follows::

    Godley and Lavoie's (2007) Model SIM specifies household final consumption
    expenditure as a function of current-period disposable income and the stock
    of wealth carried into the current period (from accumulated savings).

    ```{.python}
    C_d = alpha_1 * YD + alpha_2 * H_h[-1]
    ```

The opening paragraph of text explains the specification of the consumption
function. This is followed by a fenced code block (bracketed by ```) that
contains the equation itself, in Python, to be processed by FSIC.

Thus, the files can simultaneously contain the model itself and its
documentation. Markdown files have the additional advantage that they can be
converted to other formats for publication/distribution, such as HTML, Microsoft
Word, and LaTeX. The recommended tool for Markdown conversion is Pandoc_. In
fact, the version of Markdown supported by FSIC is the version implemented in
Pandoc.

FSIC converts the contents of Markdown files into a Python script. This script
embeds the economic relationships of the model along with the more-general code
to handle solution and data input/output. Crucially, the script includes a
command-line interface, to run the final model from the command line::

    python mymodel.py solve --span 2005Q1 2020Q4 --input data.csv --output results.csv

In this way, FSIC frees the user to focus on the economic relationships of their
model, rather than the mechanics of model building.

.. _Python: https://www.python.org
.. _Markdown: http://daringfireball.net/projects/markdown/
.. _Pandoc: http://johnmacfarlane.net/pandoc/
