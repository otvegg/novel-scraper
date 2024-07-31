import pandas as pd
import helpers
import core
import timeit
from websites.website import Website
import argparse
import logging

parser = argparse.ArgumentParser()
parser.add_argument(
    "-log",
    "--loglevel",
    default="warning",
    help="Provide logging level. Example --loglevel debug, default=warning",
)

args = parser.parse_args()

logging.basicConfig(
    level=args.loglevel.upper(), format="%(asctime)s - %(levelname)s - %(message)s"
)
logging.info("Logging now setup.")


def main():
    start = timeit.default_timer()

    # TODO: Optionally make a selection of what websites to search
    websites = core.initiateClasses()
    while True:
        searchkey = input("Search for a novel (q to exit): ")
        novels = core.searchWebsites(websites, searchkey)

        if novels is not None and not novels.empty:
            break

        if novels == None and searchkey.lower() != "q":
            print("No novel found, please adjust query.")
        if searchkey.lower() == "q":
            print("Exiting...")
            return

    helpers.prettyPrintTable(novels)

    novel = helpers.select_novel(novels)

    website: Website = novel.instance
    website.setFormat()
    website.setNovel(novel)
    website.scrape_novel()
    website.saveFile()

    stop = timeit.default_timer()

    print("Time: ", stop - start)


if __name__ == "__main__":
    main()
