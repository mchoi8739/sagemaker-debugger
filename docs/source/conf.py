# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# Standard Library
# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
# -- Project information -----------------------------------------------------
from datetime import datetime

# Third Party
from recommonmark.transform import AutoStructify

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

# List of directories, relative to source directory, that shouldn't be searched
# for source files.
exclude_trees = ["_build", "tests"]

pygments_style = "default"

autoclass_content = "both"
autodoc_default_flags = ["show-inheritance", "members", "undoc-members"]
autodoc_member_order = "bysource"

html_theme = "sphinx_rtd_theme"

# Example configuration for intersphinx: refer to the Python standard library.
intersphinx_mapping = {"http://docs.python.org/": None}

# autosummary
autosummary_generate = True

# autosectionlabel
autosectionlabel_prefix_document = True


# At the bottom of conf.py
github_doc_root = "https://github.com/mchoi8739/sagemaker-debugger/tree/smdebug-sphinx-apidoc/docs/"


def setup(app):
    app.add_config_value(
        "recommonmark_config",
        {"url_resolver": lambda url: github_doc_root + url, "auto_toc_tree_section": "Contents"},
        True,
    )
    app.add_transform(AutoStructify)
