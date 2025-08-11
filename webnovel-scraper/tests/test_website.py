import pytest
from unittest.mock import patch, MagicMock
from websites.website import Website
from bs4 import BeautifulSoup


class TestWebsite:
    @pytest.fixture
    def mock_website(self):
        return Website()  # or a specific subclass if you're testing a specific website

    @patch("requests.get")
    def test_search(self, mock_get, mock_website):
        # Mock the response
        mock_response = MagicMock()
        mock_response.text = '<html><body><div class="search-result">Result 1</div><div class="search-result">Result 2</div></body></html>'
        mock_get.return_value = mock_response

        # Call the search method
        results = mock_website.search("test query")

        # Assert the results
        assert len(results) == 2
        assert all(isinstance(result, BeautifulSoup) for result in results)
        assert [result.text for result in results] == ["Result 1", "Result 2"]

        # Assert that the GET request was made with the correct parameters
        mock_get.assert_called_once_with(
            mock_website.searchUrl,
            data={"s": "test query", "post_type": "wp_manga"},
            headers=mock_website.headers,
        )
