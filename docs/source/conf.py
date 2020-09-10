# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
# import os
# import sys
# sys.path.insert(0, os.path.abspath('.'))


# Standard Library
# -- Project information -----------------------------------------------------
from datetime import datetime

project = "smdebug-api-doc"
copyright = u"%s, Amazon" % datetime.now().year
author = "AWS DeepLearning Team"

# The full version, including alpha/beta/rc tags
release = "0.1"


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx_rtd_theme",
    "recommonmark",
    "sphinx.ext.autodoc",
    "sphinx.ext.doctest",
    "sphinx.ext.intersphinx",
    "sphinx.ext.todo",
    "sphinx.ext.coverage",
    "sphinx.ext.autosummary",
    "sphinx.ext.napoleon",
    "sphinx.ext.autosectionlabel",
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# Markdown support


# The suffix of source filenames.

source_suffix = {".rst": "restructuredtext", ".txt": "markdown", ".md": "markdown"}
master_doc = "index"  # The master toctree document.

# The full version, including alpha/beta/rc tags.
release = version

# List of directories, relative to source directory, that shouldn't be searched
# for source files.
exclude_trees = ["_build"]

pygments_style = "default"

autoclass_content = "both"
autodoc_default_flags = ["show-inheritance", "members", "undoc-members"]
autodoc_member_order = "bysource"

if "READTHEDOCS" in os.environ:
    html_theme = "default"
else:
    html_theme = "haiku"
html_static_path = []
htmlhelp_basename = "%sdoc" % project

# Example configuration for intersphinx: refer to the Python standard library.
intersphinx_mapping = {"http://docs.python.org/": None}

# autosummary
autosummary_generate = True

# autosectionlabel
autosectionlabel_prefix_document = True
