import unittest
from unittest.mock import patch
import core


class TestNovelSearch(unittest.TestCase):
    @patch("builtins.input", return_value="Alice")
    def test_greet_user(self, mock_input):
        with patch("builtins.print") as mock_print:
            websites = core.initiateClasses()
            core.searchWebsites(websites, searchkey)
            mock_print.assert_called_with("Hello, Alice!")


if __name__ == "__main__":
    unittest.main()
