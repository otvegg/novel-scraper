import pandas as pd
import helpers
import core
import timeit
from websites.website import Website


def main():
    start = timeit.default_timer()

    # TODO: Optionally make a selection of what websites to search
    websites = core.initiateClasses()
    #novels = None
    #while type(novels) == 'NoneType':
    searchkey = input("Search for a novel (q to exit): ")
        #if searchkey == 'q':
        #    return
    novels = core.searchWebsites(websites, searchkey)

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