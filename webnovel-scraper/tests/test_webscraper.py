import logging
import unittest
from unittest.mock import patch
import os, sys
from io import StringIO

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import core, helpers
from websites.website import Website


logging.basicConfig(level=logging.INFO)


def test_divine_talisman(monkeypatch):
    # Mock the input() function to return "1"
    monkeypatch.setattr("builtins.input", lambda _: "1")

    # Capture the output of the print() function
    captured_output = StringIO()
    monkeypatch.setattr(sys, "stdout", captured_output)

    # Call the functions
    websites = core.initiateClasses()
    novels = core.searchWebsites(websites, "divine talisman")
    novel = helpers.select_novel(novels)

    # Check the captured output
    captured_output.seek(0)
    output = captured_output.read().strip()
    assert output == "Selected: Divine Talisman Grandmaster with rating 4.0"

    website: Website = novel.instance
    website.setFormat()
    monkeypatch.setattr("builtins.input", lambda _: "epub")

    website: Website = novel.instance
    website.setFormat()

    # Capture the output again if needed
    captured_output.seek(0)
    output = captured_output.read().strip()
    # Add assertions for the expected output after setting the format
    assert "Expected output after setting format" in output

    website.setNovel(novel)
    # website.scrape_novel()
    # website.saveFile()
