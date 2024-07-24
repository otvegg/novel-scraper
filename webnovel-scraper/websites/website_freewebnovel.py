import timeit
from alive_progress import alive_bar
from bs4 import BeautifulSoup
import pandas as pd
import requests
from .website import Website
import helpers


class Freewebnovel(Website):
    def __init__(self):
        super().__init__()
        self.chapterUrl = "https://freewebnovel.comenovel.com"
        self.url = "https://freewebnovel.com"
        self.searchUrl = self.url + "/search/"

    def search(self, searchkey: str):

        payload = {"searchkey": searchkey}
        response = requests.post(
            self.searchUrl, data=payload, headers=self.headers
        )  # , timeout=1)

        soup = BeautifulSoup(response.text, "html.parser")
        elements = soup.select(
            "body > div.main > div.wp > div.row-box > div.col-content > div > div > div > div > div.txt"
        )

        # TODO: advance the search so we check each novels author , status, original language, alternative names
        # Probably requires an additional query for each novel

        # TODO: Estimate download time (chapters * average scrape time)
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

            estimatedDownload = int(n_chapters) * 0.5

            # scrape info page
            response = requests.get(self.url + link, headers=self.headers)
            bookSoup = BeautifulSoup(response.text, "html.parser")
            commonElements = bookSoup.select_one(
                "body > div.main > div > div > div.col-content > div.m-info > div.m-book1"
            )

            # TODO: can get more detailed score (number of votes) from this page
            abstractEls = commonElements.select("div.m-desc > div.txt > div.inner > p")

            abstract = ""
            for abstractEl in abstractEls:
                abstract += abstractEl.get_text(strip=True) + "\n"

            imgLink = commonElements.select_one("div.m-imgtxt > div.pic > img")["src"]
            imgLink = "https://freewebnovel.com" + imgLink
            everythingButDesc = commonElements.select(
                "div.m-imgtxt > div.txt > div.item"
            )

            abstract, authors, genres, source, originalLanguage, altName, status = (
                None,
                None,
                None,
                None,
                None,
                None,
                None,
            )

            for item in everythingButDesc:
                indicator = item.select_one("span")["title"]

                if indicator == "Author":
                    authors = ""
                    authorEls = item.select("div.right > a")
                    for i, authorEl in enumerate(authorEls):
                        if i > 0:
                            authors += "&"
                        authors += authorEl.get_text()

                elif indicator == "Genre":
                    genres = ""
                    genresEls = item.select("div.right > a")
                    for i, genresEl in enumerate(genresEls):
                        if i > 0:
                            genres += "&"
                        genres += genresEl.get_text()
                elif indicator == "Source":
                    source = item.select_one("div.right > span > a").get_text()
                elif indicator == "Original Language":
                    originalLanguage = item.select_one("div.right > span").get_text()
                elif indicator == "Status":
                    status = item.select_one("div.right > span > a").get_text()
                elif indicator == "Alternative names":
                    t = item.select_one("div.right > span > span")
                    if t:
                        altName = t.get_text()

            firstChapter = self.chapterUrl + link.replace(".html", "/chapter-1")

            table.append(
                [
                    title,
                    score,
                    n_chapters,
                    self.url,
                    firstChapter,
                    abstract,
                    authors,
                    genres,
                    source,
                    originalLanguage,
                    status,
                    altName,
                    imgLink,
                    estimatedDownload,
                ]
            )

        return table

    def scrape_novel(self):
        nChapters = self.novel["Chapters"]
        chapterUrl = self.novel["ChapterUrl"]
        curUrl = chapterUrl
        i = 0

        # TODO: implement parallell requests (remove the next chapter, and just use i instead)
        # probably a dict {chap number: contents} and then sort by chap number

        with alive_bar(total=int(nChapters)) as bar:
            for i in range(1, nChapters + 1):
                response = requests.get(curUrl, headers=self.headers)
                soup = BeautifulSoup(response.text, "html.parser")
                next_chapter = self.chapterUrl + soup.select_one(
                    "#main1 > div > div > div.ul-list7 > ul > li:nth-child(4) > a"
                ).get("href")

                # TODO: Add retrieval of chapter info
                paragraphs = []
                chapter_title = soup.select_one(
                    "#main1 > div > div > div.top > span"
                ).get_text()

                content = soup.select("#article > p")
                for element in content:
                    p = element.get_text(strip=True)
                    p = helpers.remove_advertisement(p)
                    paragraphs.append(p)

                # get actual header (webnovel serves 2 headers, and it varies where the "proper" header is)
                paragraphs[0] = helpers.cleanChapterHeader(chapter_title, paragraphs[0])

                # Remove paragraph (advertisement) # HACK: This might not be final?
                # Currently only for webnovel advertisements
                """ if helpers.is_advertisement(*paragraphs[-1:]):
                    paragraphs.pop() """

                self.chapters.append(paragraphs)

                curUrl = next_chapter
                bar()
