import unittest
from unittest.mock import patch, MagicMock
import os, sys
import pytest


sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import helpers
from core import initiateClasses
from websites.website import Website


# Mocking the Website base class
class MockWebsite(Website):
    pass


def test_initiate_classes_empty_directory(tmp_path):
    with patch("os.listdir", return_value=[]):
        assert initiateClasses() == []


def test_initiate_classes_no_website_files(tmp_path):
    with patch("os.listdir", return_value=["other_file.py", "not_a_website.txt"]):
        assert initiateClasses() == []


def test_initiate_classes_with_website_files(tmp_path):
    # Create a mock 'websites' directory
    websites_dir = tmp_path / "websites"
    websites_dir.mkdir()

    # Create mock website files
    (websites_dir / "website_example1.py").write_text(
        """
from websites.website import Website
class Example1(Website):
    def __init__(self):
        self.name = "Example1"
    """
    )

    (websites_dir / "website_example2.py").write_text(
        """
from websites.website import Website
class Example2(Website):
    def __init__(self):
        self.name = "Example2"
    """
    )

    # Patch the Website import in the test files
    with patch.dict(sys.modules, {"websites.website": sys.modules[__name__]}), patch(
        "websites.website.Website", MockWebsite
    ):
        result = initiateClasses(str(websites_dir))

        assert len(result) == 2
        assert isinstance(result[0], MockWebsite)
        assert isinstance(result[1], MockWebsite)
        assert result[0].name == "Example1"
        assert result[1].name == "Example2"


def test_initiate_classes_directory_not_found():
    with pytest.raises(FileNotFoundError):
        initiateClasses("/path/to/nonexistent/directory")


def test_initiate_classes_integration(tmp_path):
    # Create actual Python files for integration testing
    websites_dir = tmp_path / "websites"
    websites_dir.mkdir()

    (websites_dir / "website_test1.py").write_text(
        """
from websites.website import Website
class Test1(Website):
    def __init__(self):
        self.name = "Test1"
    """
    )

    (websites_dir / "website_test2.py").write_text(
        """
from websites.website import Website
class Test2(Website):
    def __init__(self):
        self.name = "Test2"
    """
    )

    # Patch the Website import in the test files
    with patch.dict(sys.modules, {"websites.website": sys.modules[__name__]}), patch(
        "websites.website.Website", MockWebsite
    ):
        result = initiateClasses(str(websites_dir))

        assert len(result) == 2
        assert result[0].name == "Test1"
        assert result[1].name == "Test2"
