# -*- coding: utf-8 -*-
"""
model
=====
Build FSIC models from `Schematic` objects.

"""

import yaml

from FSIC.classes.model import Model
from FSIC.templates.python import MODEL, DEFAULT_CONTENTS


def build_model(schematic, output='class', reorder_equations=None, **kwargs):
    """Create a FSIC model class from `schematic`.

    ** Warning: if `output`='class', this function uses `exec()` and `eval()`
                to return the class definition. **

    Parameters
    ----------
    schematic : `FSIC` `Schematic` object
        Input model specification
    output : string, one of ['class', 'script'] or a filename; default 'class'
        Set the output (see 'Returns' below for details)
    reorder_equations : string, default `None`
        If not `None`, apply the specified algorithm to reorder the system of
        equations
    **kwargs : other keyword arguments to insert into class definition

    Returns
    -------
    Depends on `output`:
     - 'class' : class
           The model class as a Python object, to be instantiated
     - 'script' : string
           An `exec`utable string (the same one used to return a class
           definition if `output`='class')
     - filename : None
           Instead of returning anything, write the script to the path in
           `filename`

    """
    # Use default dictionary as a starting point, and copy in frontmatter
    contents = DEFAULT_CONTENTS.copy()
    frontmatter = yaml.load(schematic.block_table.ix['_Frontmatter', '_raw'])
    if frontmatter is not None:
        for k, v in frontmatter.items():
            contents[k] = v

    # Insert variable information
    variable_types = {'endogenous': 'endogenous',
                      'exogenous': 'exogenous',
                      'parameters': 'parameter',
                      'errors': 'error'}
    for key, type_ in variable_types.items():
        contents[key] = [v for v, t in schematic.symbol_table['type'].items()
                         if t == type_]
    contents['variables'] = contents['endogenous'] + contents['exogenous']
    contents['convergence_variables'] = contents['endogenous']

    # Add offset values
    contents['start_offset'] = -min(schematic.symbol_table['min'])
    contents['end_offset'] = max(schematic.symbol_table['max'])

    # Overwrite with any additional keyword arguments
    for k, v in kwargs.items():
        contents[k] = v

    # Create code for Python solution
    if reorder_equations is not None:
        raise NotImplementedError

    lines = []
    for equation in schematic.equations.values():
        format_dict = {}
        for i, t in equation.terms.iterrows():
            key = t.name
            term = t['name']
            if t['type'] in ('endogenous', 'exogenous', 'parameter', 'error'):
                index = t['index']
                if index == 0:
                    index = ''
                term = 'self.{variable}.values[row{index}]'.format(
                    variable=t['name'], index=index)
            format_dict[key] = term
        expression = equation.template.format(**format_dict)
        lines.append(expression)
    contents['python_code'] = '\n        '.join(lines)

    # Create underline to match length of model name
    contents['underline'] = '=' * len(contents['name'])

    # Create script
    for k in contents.keys():
        try:
            contents[k] = contents[k].rstrip()
        except AttributeError:
            pass
    contents['version'] = repr(contents['version'])
    script = MODEL.format(**contents)

    if output == 'class':
        exec(script)
        return eval(contents['name'])
    elif output == 'script':
        return script
    else:
        with open(output, 'w') as f:
            print(script, file=f)
