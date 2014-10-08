.. _installation:

************
Installation
************

The latest version of FSIC can be downloaded from GitHub_. This section sets out
how to:

* Install the package
* Run the test suite
* Build the documentation

.. _GitHub: https://github.com/cthoung/fsic


.. _installation-install:

Install package
===============

FSIC is provided as a standard Python package distribution. To install the
package, while in the root folder, run ``setup.py`` as follows::

    python setup.py install


.. _installation-test:

Test package code
=================

Code tests for FSIC are implemented in nose_ and can be run as follows::

    nosetests

To also check the tests' coverage of the code base::

    nosetests --with-coverage --cover-package=FSIC

.. _nose: https://nose.readthedocs.org/en/latest/


.. _installation-doc:

Build documentation
===================

The documentation for FSIC is written in Sphinx_. It can be built from source
using the ``makefile`` in the ``doc`` folder. For example, to build the html
version of the documentation::

    make html

.. _Sphinx: http://sphinx-doc.org/
