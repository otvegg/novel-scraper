from unittest.mock import patch, MagicMock
import os, sys
import pandas as pd
import pytest

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from websites.website import Website
from core import searchWebsites


class MockWebsite(Website):
    def __init__(self, name):
        self.name = name

    def search(self, term):
        print("seracihng")
        return [
            [
                "Test title",  # Title
                0.95,  # score
                100,  # Chapters
                f"https://{self.name}.com",  # Website
                f"This is a test novel from {self.name}",  # abstract
                f"Author {self.name}",  # author
                "Fantasy",  # genre
                self.name,  # source
                "English",  # original_language
                "Ongoing",  # status
                ["Test", "title"],  # alternate_names
                f"https://{self.name}.com/image.jpg",  # imglink
                "10 minutes",  # estimatedDownload
            ]
        ]


def test_search_websites():
    mock_websites = [MockWebsite("Site1"), MockWebsite("Site2"), MockWebsite("Site3")]
    print(mock_websites)
    result = searchWebsites(mock_websites, "Test")
    assert isinstance(result, pd.DataFrame)
    assert len(result) == 3
    assert set(result["source"]) == {"Site1", "Site2", "Site3"}


def test_search_websites_no_results():
    class EmptyMockWebsite(Website):
        def search(self, term):
            return []

    mock_websites = [EmptyMockWebsite()]
    result = searchWebsites(mock_websites, "test")
    assert result is None
