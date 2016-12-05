.. _io:

I/O
===

``fsic`` includes I/O functions to read and write CSV data, possibly with `YAML
frontmatter`_ (hence the 'y' suffix in the function names). These functions are
wrappers for `pandas`_ functions, mainly to ease data handling when running
models from the command line. The functions are also available for direct use::

    from fsic import read_csvy, write_csvy


:func:`read_csvy()` wraps the ``read_csv()`` function from ``pandas``. For
regular CSV files, the behaviour is identical to the ``pandas`` function, and
will return an identical result. If the input file has YAML frontmatter,
``read_csvy()`` will (optionally) return the frontmatter as a dictionary, along
with the CSV data.

.. function:: read_csvy(filepath_or_buffer, return_frontmatter=False, *args, **kwargs)

   Wrapper for ``pandas.read_csv()``, to allow for YAML frontmatter.

   :param filepath_or_buffer: input to read, as for ``pandas``'s ``read_csv()`` function

   :param return_frontmatter: instead of just returning the DataFrame (as ``read_csv()`` would), return a 2-tuple containing the data and the frontmatter
   :type return_frontmatter: bool

   :param args: other arguments to pass to ``read_csv()``
   :param kwargs: other arguments to pass to ``read_csv()``

   :returns: a DataFrame, if ``return_frontmatter`` is ``False``; a 2-tuple containing the DataFrame and a dictionary of frontmatter if ``return_frontmatter`` is ``True``
   :rtype: ``DataFrame`` or (``DataFrame``, ``dict``)

   :See also: the underlying ``read_csv()`` function from ``pandas``


:func:`write_csvy()` also wraps ``pandas`` functionality but, in this case, the
function accesses the ``to_csv()`` method of a ``pandas`` object.

.. function:: write_csvy(data, path_or_buf=None, frontmatter=None, *args, **kwargs)

   Wrapper for ``pandas`` objects' ``to_csv()`` method, to allow for YAML frontmatter.

   :param data: object to write; must have a ``to_csv()`` method

   :param path_or_buf: destination for output, as for the object's ``to_csv()`` method; if ``None`` (the default), return the result as a string

   :param frontmatter: (optional) frontmatter to write as a YAML block; typically a list- or dict-like

   :param args: other arguments to pass to ``to_csv()``
   :param kwargs: other arguments to pass to ``to_csv()``

   :returns: the output as a string, if ``path_or_buf`` is ``None``; otherwise, nothing

   :See also: the ``to_csv()`` method of ``data``; typically a DataFrame or Series object


.. _YAML frontmatter: http://blog.datacite.org/using-yaml-frontmatter-with-csv/
.. _pandas: http://pandas.pydata.org/
