# Minimal Sphinx configuration file
import sys
from pathlib import Path

# Add src/ to PYTHONPATH
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

project = "csvsmith"
author = "Eiichi YAMAMOTO"
copyright = "2026, Eiichi YAMAMOTO"

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.napoleon",   # for Google/NumPy docstrings
    "sphinx.ext.viewcode",   # adds source links
]

autodoc_default_options = {
    "members": True,
    "undoc-members": False,
    "show-inheritance": True,
}

templates_path = ["_templates"]
exclude_patterns = ["_build"]

html_theme = "alabaster"
html_static_path = ["_static"]

autosummary_generate = True
