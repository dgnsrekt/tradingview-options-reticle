"""Module for commonly used paths."""

from pathlib import Path

SOURCE_ROOT_PATH = Path(__file__).parent
"""* A path to the source code directory."""

PROJECT_ROOT_PATH = SOURCE_ROOT_PATH.parent
"""* A path to the project root directory."""

TEMPLATES_PATH = SOURCE_ROOT_PATH / "templates"
"""* A path to the templates directory."""

TESTS_PATH = PROJECT_ROOT_PATH / "tests"
"""* A path to the test directory."""
