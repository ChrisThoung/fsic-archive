# FSIC: Flows and Stocks Integrated Consistently

[![Build Status](https://travis-ci.org/cthoung/fsic.svg?branch=master)](https://travis-ci.org/cthoung/fsic)

FSIC is a Python package for the specification, solution and analysis of
Stock-Flow Consistent macroeconomic models in the tradition of Wynne Godley.

`REFERENCES.md` contains a bibliography to accompany this package and the
included examples.

## Dependencies

### Required

* [pandas](http://pandas.pydata.org/):
  Version 0.14.1 or higher
    * See the `pandas` documentation for further dependencies
      (FSIC also uses [NumPy](http://www.numpy.org/) directly)
* [NetworkX](http://networkx.github.io/):
  Version 1.8.1 or higher

### Optional

* [IPython](http://ipython.org/) for interactive modelling:
  Version 2.0.0 or higher
* [Sphinx](http://sphinx-doc.org/) to build the documentation:
  Version 1.2.2 or higher

## Other useful software

* [pandoc](http://johnmacfarlane.net/pandoc/) to convert pandoc Markdown files
  (the preferred format with which to define a model using FSIC's built-in
  template) to other formats, such as HTML, PDF and Microsoft Word docx
