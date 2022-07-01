"""Sphinx configuration."""
project = "Matterless"
author = "Mark Gomersbach"
copyright = "2022, Mark Gomersbach"
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx_click",
    "myst_parser",
]
autodoc_typehints = "description"
html_theme = "furo"
