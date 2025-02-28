"""
Unit tests for metadata.py.

Ensures:
    - Metadata loads correctly from `pyproject.toml`.
    - Default values are used when `pyproject.toml` is missing/malformed.
    - Metadata fields follow expected formats.

Uses unittest for basic validation and pytest-mock for file mocking.
"""

import unittest
import metadata
from unittest.mock import mock_open, patch
import pytest

class TestMetadata(unittest.TestCase):
    """Test cases for the metadata module."""

    def test_app_name(self):
        """Ensure app name is loaded or falls back to default."""
        self.assertIsInstance(metadata.__app_name__, str)
        self.assertGreater(len(metadata.__app_name__), 0)

    def test_version_format(self):
        """Ensure version follows semantic versioning format X.Y.Z."""
        self.assertRegex(metadata.__version__, r"^\d+\.\d+\.\d+$")

    def test_author_exists(self):
        """Ensure at least one author is present or falls back to 'Unknown'."""
        self.assertIsInstance(metadata.__author__, str)
        self.assertGreater(len(metadata.__author__), 0)

    def test_license_format(self):
        """Ensure license is a valid string."""
        self.assertIsInstance(metadata.__license__, str)

@pytest.fixture
def mock_toml():
    """Valid `pyproject.toml` mock data."""
    return b"""
    [project]
    name = "Test App"
    version = "1.2.3"
    authors = [{name = "Test Author"}]
    license = {text = "MIT"}
    """

@pytest.fixture
def malformed_toml():
    """Malformed TOML mock data."""
    return b"INVALID DATA"

def test_metadata_loading(mock_toml):
    """Test successful metadata loading from a valid TOML file."""
    with patch("metadata.open", mock_open(read_data=mock_toml), create=True):
        with patch("metadata.tomllib.load", return_value={"project": {
            "name": "Test App",
            "version": "1.2.3",
            "authors": [{"name": "Test Author"}],
            "license": {"text": "MIT"},
        }}):
            reload_metadata()
            assert metadata.__app_name__ == "Test App"
            assert metadata.__version__ == "1.2.3"
            assert metadata.__author__ == "Test Author"
            assert metadata.__license__ == "MIT"

def test_missing_toml():
    """Test behavior when `pyproject.toml` is missing."""
    with patch("metadata.open", side_effect=FileNotFoundError):
        reload_metadata()
        assert metadata.__app_name__ == "Unknown App"

def test_malformed_toml(malformed_toml):
    """Test behavior when `pyproject.toml` is malformed."""
    with patch("metadata.open", mock_open(read_data=malformed_toml), create=True):
        with patch("metadata.tomllib.load", side_effect=Exception):
            reload_metadata()
            assert metadata.__app_name__ == "Unknown App"

def reload_metadata():
    """Helper function to reload metadata to apply mocks properly."""
    global metadata
    from importlib import reload
    reload(metadata)
