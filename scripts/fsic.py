#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FSIC
====
**FSIC** (Flows and Stocks Integrated Consistently) is a Python package for the
specification, solution and analysis of Stock-Flow Consistent macroeconomic
models in the tradition of Wynne Godley.

"""

from FSIC.cli.script import PARSER, handle_args


if __name__ == '__main__':
    handle_args(PARSER.parse_args())
