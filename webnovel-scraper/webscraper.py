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


def main() -> None:
    logging.info("Logging setup at the beginning of the main function.")

    websites = core.initiateClasses()
    searchkey = ""
    while searchkey.lower() != "q":
        try:
            searchkey = input("Search for a novel (q to exit): ")

            novels = core.searchWebsites(websites, searchkey)
            if novels is not None and not novels.empty:
                break

            if novels is None:
                print("No novel found, please adjust query.")

        except Exception as e:
            print("An error occurred during novel search:", e)

    if searchkey.lower() == "q":
        print("Exiting...")
        return

    helpers.prettyPrintTable(novels)

    novel = helpers.select_novel(novels)

    website: Website = novel.instance
    website.setFormat()
    start = timeit.default_timer()
    website.setNovel(novel)
    website.scrape_novel()
    website.saveFile()

    print("Scraping+saving runtime:", timeit.default_timer() - start)


if __name__ == "__main__":
    main()
