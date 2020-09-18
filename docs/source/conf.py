# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# Standard Library
import os
import sys
# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
# -- Project information -----------------------------------------------------
from datetime import datetime

# Third Party

sys.path.insert(0, os.path.abspath('../../smdebug/'))

import mock

MOCK_MODULES = ["numpy", "scipy", "mxnet", "tensorflow", "torch"]
for mod_name in MOCK_MODULES:
    sys.modules[mod_name] = mock.Mock()

project = "smdebug"
copyright = u"%s, Amazon" % datetime.now().year
author = "AWS DeepLearning Team"

# The full version, including alpha/beta/rc tags
release = "0.0.1"

# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
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
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']


# -- Options for HTML output -------------------------------------------------

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]

# Markdown support
# The suffix of source filenames.
source_suffix = {".rst": "restructuredtext", ".txt": "markdown", ".md": "markdown"}
master_doc = "index"  # The master toctree document.

pygments_style = "default"

autoclass_content = "both"
autodoc_default_flags = ["show-inheritance", "members", "undoc-members"]
autodoc_member_order = "bysource"

html_theme = "sphinx_rtd_theme"
#html_theme = "classic"

# autosummary
autosummary_generate = True

# autosectionlabel
autosectionlabel_prefix_document = True

def setup(app):
    app.add_css_file('custom.css')
