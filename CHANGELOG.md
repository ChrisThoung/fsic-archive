# Change log

[Change log](http://keepachangelog.com/) for FSIC.

FSIC follows the conventions of
[Semantic Versioning](http://semver.org/spec/v2.0.0.html) (version 2.0.0).

## Unreleased - YYYY-MM-DD

### Added

* Further improvements to Sphinx documentation from v0.1.0
* Update documentationn in package code:
    * Description of equation-ordering algorithm in
      `FSIC.optimise.order.recursive()`

### Changed

### Deprecated

### Removed

### Fixed

* Add CHANGELOG.md to MANIFEST.in
* Correct escaping of single quotes in input-argument file example in
  documentation

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
