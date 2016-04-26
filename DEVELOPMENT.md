# Development

The development workflow for FSIC follows the principles of Vincent Driessen's
[Git branching model](http://nvie.com/posts/a-successful-git-branching-model/).

* The `master` branch always contains the latest (fully-operational and
  documented) release i.e. it matches the contents of the latest tag
* The `development` branch consolidates new development work, by merging the
  contents of other branches (see below for naming conventions)
    * New development work should take the `development` branch as its starting
      point
	* Completed development work should be merged back into the `development`
      branch
	* The contents of the `development` branch (possibly via an interim release
      branch) will eventually supplant the contents of the previous `master`
      branch, in the form of a new tagged release
	* New additions to the `development` branch should be noted in
      `CHANGELOG.md`
	* Merged branches should be deleted after use

## Branch naming conventions

All branches other than `master`, `development` and `archive` (which stores
defunct and/or experimental code) must have a prefix to denote the nature of
the development work in that branch:

* New features (requiring additions to 'Added' in `CHANGELOG.md`): `feature/`
  e.g. `feature/io-sqlite`
* Changes in functionality: `change/`
* Fixes (requiring additions to at least one of 'Added', 'Deprecated',
  'Removed', 'Fixed' or 'Security'): `fix/`
* Examples (requiring additions to 'Added'): `example/`
* Documentation (where distinct from documentation to accompany one of the
  above, requiring additions to 'Added'): `doc/`
