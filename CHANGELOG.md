# Change log

[Change log](http://keepachangelog.com/) for FSIC.

FSIC follows the conventions of
[Semantic Versioning](http://semver.org/spec/v2.0.0.html) (version 2.0.0).

## Unreleased - YYYY-MM-DD

### Added

* New schematic classes to represent model structure:
    * `Variable`: to parse individual variable expressions e.g. 'C_d'
    * `Equation`: to parse a single equation expression
	  e.g. 'C_d = alpha_1 * YD + alpha_2 * H_h[-1]'
* Further improvements to Sphinx documentation from v0.1.0
* Update documentationn in package code:
    * Description of equation-ordering algorithm in
      `FSIC.optimise.order.recursive()`
* Additional tests to improve coverage
* Specification for `build` system
* Specification for solution phases in model objects
* Specification for data variables in model objects
* Support for YAML frontmatter in delimiter-separated data files

### Changed

* Overhaul of build and templating system
    * New `classes` sub-package containing new, simplified `Model` class
    * New template, 'derived.py', to use new `Model` class
    * Update 'fsic.py' script with new `template` command
* Handling of solution-period controls in model template:
    * Version 0.1.0 specified a solution span (with the argument ``--span``)
      and, optionally, a prior period to allow for lagged relationships but not
      to be solved (using ``--past``)
    * Updated version continues to specify a solution span (with ``--span``, as
      before) but now uses an optional period *within* that span to solve from
      (with a new ``--solve-from`` argument). Documentation updated accordingly
* `FSIC.dtype` variable renamed to `FSIC.DTYPE`

### Deprecated

### Removed

* Remove ``--past`` period argument from model-script template. To solve a
  (typically dynamic) model beginning in a period other than the first one, use
  ``--solve-from`` instead

### Fixed

* Add CHANGELOG.md to MANIFEST.in
* Correct escaping of single quotes in input-argument file example in
  documentation
* Call to equation-order optimisation function in build script

### Security

## 0.1.0 - 2014-11-26

First version of FSIC, implementing rudimentary script generation, with basic
Markdown parsing and code translation:

* Main `fsic.py` script to build models from Markdown files
* Core of code extractor for Markdown files
* First version of model-script template
* Input-file handling for (possibly-compressed) delimited files
* First version of equation-order optimisation code
* Unit tests for all but the `Build` class
* Example implementation of *Model SIM*, from Chapter 3 of Godley and Lavoie
  (2007)
* Equations from Almon (2014) AMI model
* Minimal documentation, in [Sphinx](http://sphinx-doc.org/)
