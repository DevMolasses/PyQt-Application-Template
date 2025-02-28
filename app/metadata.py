"""
metadata.py

This module provides a centralized way to retrieve application metadata 
from `pyproject.toml`, ensuring a single source of truth for the app name, 
version, author, and license information. 

By dynamically loading metadata, this module prevents duplication across 
different parts of the application and allows easy modifications without 
editing multiple files.

Usage:
    from metadata import __app_name__, __version__, __author__

    print(f"{__app_name__} v{__version__} by {__author__}")

If `pyproject.toml` is missing or incorrectly formatted, the module 
falls back to default values to prevent runtime errors.

Dependencies:
    - Python 3.11+ (or `tomli` for older versions)
    - A valid `pyproject.toml` file in the project root

"""

import tomllib  # Python 3.11+ (use 'import tomli' for Python 3.10 and below)

from core.logger import logger

def load_metadata():
    """
    Loads metadata from `pyproject.toml` and returns it as a dictionary.

    If the file is missing or malformed, the function returns an empty 
    dictionary instead of raising an exception. The exception is logged.

    Returns:
        dict: Parsed metadata from the TOML file.
    """
    try:
        with open("pyproject.toml", "rb") as f:
            return tomllib.load(f).get("project", {})
    except FileNotFoundError:
        logger.warning("pyproject.toml not found. Using default metadata.")
        return {}
    except tomllib.TOMLDecodeError:
        logger.error("Error decoding pyproject.toml. Check file formatting.")
        return {}

# Load metadata safely
_metadata = load_metadata()

# Extract metadata using `.get()` to prevent KeyErrors
__app_name__ = _metadata.get("name", "Unknown App")
__version__ = _metadata.get("version", "0.0.0")
__description__ = _metadata.get("description", "No description available")
__license__ = _metadata.get("license", {}).get("text", "No license")

# Extract first author if available, otherwise set to "Unknown"
_authors = _metadata.get("authors", [])
__author__ = _authors[0].get("name", "Unknown") if _authors else "Unknown"

# Print metadata when run directly (for debugging)
if __name__ == "__main__":
    print(f"{__app_name__} v{__version__} by {__author__} - {__license__}")
