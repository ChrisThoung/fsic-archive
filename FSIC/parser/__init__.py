# -*- coding: utf-8 -*-
"""
parser
======
FSIC subpackage for model specification.

Typically, the user will supply a *script* (Pandoc Markdown-compatible
text) as a string. This script will normally contain a mix of text and
code *chunks*. Each chunk takes the form:

    ~~~{#consumption .python type="not hydraulic"}
    C_d = alpha_1 * YD + alpha_2 * H_h[-1]
    ~~~

Each chunk comprises two *blocks*:

1. An *attributes block*, the text inside the braces on the opening line:
       #consumption .python type="not hydraulic"
2. A *code block*, the text on the lines between the rows of tildes
   (or backticks)
        C_d = alpha_1 * YD + alpha_2 * H_h[-1]

The contents of the code blocks form the basis of the model itself,
while the attributes provide additional information to the parser.

Attributes may consist of:

* At most one 'identifier', a word preceded by a '#' e.g. 'consumption'
* Any number (including zero) of 'classes', words preceded by a '.'
  e.g. 'python'
* Any number (including zero) of 'attributes', key:value pairs defined
  by an '='
  e.g. type="not hydraulic', which defines the key/attribute-name 'type'
       and the corresponding value 'not hydraulic'

In summary, the structure of a typical script is as follows:

* A script, containing one or more:
    * Chunks, each comprising two:
        * Blocks, either:
            * An attributes block, containing:
                * An identifier
                * Classes
                * Attributes
            * A code block

The parser subpackage contains the following modules:

Generic:

* `markdown`, to extract chunks from a Markdown-formatted script string
* `chunk`, to extract code blocks and metadata from chunks

Language-specific:

* `code`, to translate Python code blocks into compatible code and identify
  model variables
* `ini`, to handle INI-style configuration file strings

"""
