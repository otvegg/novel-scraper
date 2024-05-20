from urllib.request import urlopen
from bs4 import BeautifulSoup
import requests
import pandas as pd  # remove if i can make nice tables
from alive_progress import alive_bar, config_handler

config_handler.set_global(spinner="waves")

URL = "https://freewebnovel.com"
SEARCHURL = "https://freewebnovel.com/search/"
CHAPTERBASEURL = "https://freewebnovel.comenovel.com"


def search_novels(searchString: str):

    payload = {"searchkey": searchString}

    response = requests.post(SEARCHURL, data=payload)
    soup = BeautifulSoup(response.text, "html.parser")
    elements = soup.select(
        "body > div.main > div.wp > div.row-box > div.col-content > div > div > div > div > div.txt"
    )

    table = []
    for element in elements:
        title = element.select_one("div > h3.tit > a").get_text(strip=True)
        link = element.select_one("div > h3.tit > a").get("href")
        score = element.select_one("div > div.core > span").get_text(strip=True)
        n_chapters = element.select("div > div.desc > div")[2].select(
            "div.right > a > span"
        )
        if len(n_chapters) == 2:
            n_chapters = n_chapters[1].get_text(strip=True).split()[0]
        else:
            n_chapters = n_chapters[0].get_text(strip=True).split()[0]

        firstChapter = CHAPTERBASEURL + link.replace(".html", "/chapter-1")

        table.append([title, score, n_chapters, URL, firstChapter])

    return table


# def get_novel_url(novel_info):
#     if novel_info.Website == "freewebnovel.com":
#         link = novel_info.Link.replace(".html", "/chapter-1")
#     else:
#         website = novel_info.Website
#         link = novel_info.Link
#     return chapterBaseUrl, chapterBaseUrl + link


def get_chapter_info(chapterUrl: str, nChapters: int):

    response = requests.get(chapterUrl)
    soup = BeautifulSoup(response.text, "html.parser")
    next_chapter = CHAPTERBASEURL + soup.select_one(
        "#main1 > div > div > div.ul-list7 > ul > li:nth-child(4) > a"
    ).get("href")
    current_chapter = soup.select_one("#main1 > div > div > div.top > span").get_text(
        strip=True
    )

    # Check if the current chapter is the last chapter
    if int(chapterUrl.split("-")[-1]) == nChapters:
        next_chapter = -1

    content = soup.select("#article > p")
    paragraphs = []
    for element in content:
        paragraphs.append(element.get_text(strip=True))

    paragraphs = paragraphs[:-1]  # Remove last paragraph (advertisement)

    return current_chapter, paragraphs, next_chapter
