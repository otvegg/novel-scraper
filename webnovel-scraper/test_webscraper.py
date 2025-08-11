from subprocess import Popen, PIPE, STDOUT
import sys
import time


def run_scraper(terms: tuple):
    print(f"Running scraper with search term: '{terms}'")

    input_data = "divine talisman\nq"

    process = Popen(["python", "webscraper.py"], stdin=PIPE, stdout=PIPE, text=True)
   


test_cases = [
    ("divine talisman", "q"),
    # ("another novel", "2\nq"),
]

for terms in test_cases:
    run_scraper(terms)
