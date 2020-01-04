# FSIC: Flows and Stocks Integrated Consistently

**I no longer maintain this package (and, admittedly, haven't done so for some
time). From what I've learned from this first go, I've since started over with
a streamlined implementation at
[https://github.com/ChrisThoung/fsic](https://github.com/ChrisThoung/fsic)**

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
