import pandas as pd
import freewebnovel


def search_websites(searchString: str):
    allResults = []
    allResults.extend(freewebnovel.search_novels(searchString))
    # allResults.append(wuxiaworld.search_novels(searchString))
    # allResults.append(readnovelfull.search_novels(searchString))
    # allResults.append(novelfull.search_novels(searchString))

    df = pd.DataFrame(
        allResults, columns=["Title", "Score", "Chapters", "Website", "ChapterUrl"]
    )
    df.index += 1
    return df


def get_chapter_info(novel_info, url):
    # instead of all these if else, can we make a class?
    if novel_info.Website == "https://freewebnovel.com":
        current_chapter, paragraphs, next_chapter = freewebnovel.get_chapter_info(
            url,
            int(novel_info.Chapters),
        )
    else:
        return -1

    return current_chapter, paragraphs, next_chapter
