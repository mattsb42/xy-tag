######
xy-tag
######

.. image:: https://img.shields.io/pypi/v/xy-tag.svg
   :target: https://pypi.python.org/pypi/xy-tag
   :alt: Latest Version

.. image:: https://img.shields.io/pypi/pyversions/xy-tag.svg
   :target: https://pypi.python.org/pypi/xy-tag
   :alt: Supported Python Versions

.. image:: https://img.shields.io/badge/code_style-black-000000.svg
   :target: https://github.com/ambv/black
   :alt: Code style: black

.. image:: https://readthedocs.org/projects/xy-tag/badge/
   :target: https://xy-tag.readthedocs.io/en/stable/
   :alt: Documentation Status

.. important::

    This project is a work in progress and is not yet ready for use.

xy-tag takes an existing version tag in X.Y.Z format
and creates new tags for the X and Y versions
pointing to the same commit.

The primary intended use for this is to provide variable version aliasing.
This is useful, for example, when publishing a GitHub Actions Action to the GitHub Marketplace.
Rather than requiring your users to continuously update their version dependencies
as you release updates to your Action,
or requiring *you* to manually create these aliasing tags.

Configuration
*************

.. list-table::
   :header-rows: 1

   * - Name
     - Default
     - GitHub Actions Input
     - CLI Flag
   * - `GitHub Token`_
     - REQUIRED
     - ``github-token``
     - ``--github-token``
   * - `XYZ Version`_
     - ``$GITHUB_REF``
     - ``xyz-version``
     - ``--xyz-version``
   * - `Commitish`_
     - ``$GITHUB_SHA``
     - ``commitish``
     - ``--commitish``
   * - `GitHub Repository`_
     - ``$GITHUB_REPOSITORY``
     - ``github-repository``
     - ``--github-repository``
   * - `Dry Run`_
     - ``false``
     - ``dry-run: true``
     - ``--dry-run``
   * - `Version Separator`_
     - ``.``
     - ``version-separator``
     - ``--version-separator``
   * - `Beta Separator`_
     - ``-``
     - ``beta-separator``
     - ``--beta-separator``

GitHub Token
============

Access token to use to call GitHub.

XYZ Version
===========

The full X.Y.Z version to start with.

.. note::

    If this value starts with ``refs/heads/``, that prefix is removed.

Commitish
=========

Git commit-ish identifier for tags to target.

GitHub Repository
=================

The GitHub Repository to target.

Dry Run
=======

Don't actually make the tags, just show what they would be.

Version Separator
=================

Value that separates version identifiers.

Beta Separator
==============

Value that separates beta identifiers.

.. note::

    If this value is present in XYZ version, no tags are created!

Use as a GitHub Action
**********************

.. code-block:: yaml

    on:
      release:
        types: [published]

    jobs:
      make-tags:
        runs-on: ubuntu-latest
        steps:
          - uses: mattsb42-meta/xy-tag@v1
            with:
              github-token: ${{ secrets.GITHUB_TOKEN }}


Use as a CLI
************

If you don't want to use GitHub Actions
or you just want to retain the ability to run xy-tag manually Just In Case,
you can!

.. code-block:: bash

    xy-tag --github-token $GITHUB_TOKEN --xyz-version 1.4.2

You can also specify
