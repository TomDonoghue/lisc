# -*- coding: utf-8 -*-
#
# Configuration file for the Sphinx documentation builder.
#
# For a full list of documentation options, see:
# https://www.sphinx-doc.org/en/master/usage/configuration.html


# ----------------------------------------------------------------------------

import os
from os.path import dirname as up

from datetime import date

import sphinx_gallery
import sphinx_bootstrap_theme
from sphinx_gallery.sorting import FileNameSortKey

# -- Project information -----------------------------------------------------

# Set project information
project = 'lisc'
copyright = '2018-{}, Thomas Donoghue'.format(date.today().year)
author = 'Thomas Donoghue'

# Get and set the current version number
from lisc import __version__
version = __version__
release = version


# -- General configuration ---------------------------------------------------

# If your documentation needs a minimal Sphinx version, state it here.
#
# needs_sphinx = '1.0'

# Add any Sphinx extension module names here, as strings.
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.doctest',
    'sphinx.ext.intersphinx',
    'sphinx.ext.mathjax',
    'sphinx.ext.viewcode',
    'sphinx.ext.githubpages',
    'sphinx_gallery.gen_gallery',
    'numpydoc',
    'm2r'
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path .
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# numpydoc interacts with autosummary, that creates excessive warnings
# This line is a 'hack' for that interaction that stops the warnings
numpydoc_show_class_members = False

# Set to generate sphinx docs for class members (methods)
autodoc_default_options = {
    'members': None,
    'no-inherited-members': None,
}

# generate autosummary even if no references
autosummary_generate = True

# The suffix(es) of source filenames. Can be str or list of string
source_suffix = '.rst' # ['.rst', '.md']

# The master toctree document.
master_doc = 'index'

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.
html_theme = 'bootstrap'

# Theme options to customize the look and feel, which are theme-specific.
html_theme_options = {

    # A list of tuples containing pages or urls to link to from the navigation bar
    'navbar_links': [
        ("API", "api"),
        ("Tutorials", "auto_tutorials/index"),
        ("Examples", "auto_examples/index"),
        ("GitHub", "https://github.com/lisc-tools/lisc", True)
    ],

    # Bootswatch (http://bootswatch.com/) theme to apply
    'bootswatch_theme': "flatly",

    # Render the current pages TOC in the navbar
    'navbar_pagenav': False,
}

# Settings for whether to copy over and show link rst source pages
html_copy_source = False
html_show_sourcelink = False


# -- Extension configuration -------------------------------------------------

# Configurations for sphinx gallery
sphinx_gallery_conf = {
    'examples_dirs': ['../examples', '../tutorials'],
    'gallery_dirs': ['auto_examples', 'auto_tutorials'],
    'within_subsection_order': FileNameSortKey,
    # Settings for linking between examples & API examples
    'backreferences_dir': 'backrefs',
    'doc_module': ('lisc',),
    'reference_url': {'lisc': None}
}
