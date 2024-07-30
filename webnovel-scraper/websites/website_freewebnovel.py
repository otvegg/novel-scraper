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

        #
        searchResults = soup.select(
            "body > div.main > div.wp > div.row-box > div.col-content > div > div > div > div > div.txt"
        )

        # TODO: Estimate download time (chapters * average scrape time)

        table = []
        for book in searchResults:
            title = book.select_one("div > h3.tit > a").get_text(strip=True)
            link = book.select_one("div > h3.tit > a").get("href")
            score = book.select_one("div > div.core > span").get_text(strip=True)

            # scrape info page
            response = requests.get(self.url + link, headers=self.headers)
            bookSoup = BeautifulSoup(response.text, "html.parser")

            chapters = bookSoup.select("#idData > li > a")
            print(link)
            chapterLinks = []
            for i in chapters:
                chapterLinks.append(self.chapterUrl + i.get("href"))

            estimatedDownload = len(chapterLinks) * 0.5

            bookInfo = bookSoup.select_one(
                "body > div.main > div > div > div.col-content > div.m-info > div.m-book1"
            )

            # TODO: can get more detailed score (number of votes) from this page
            abstractEls = bookInfo.select("div.m-desc > div.txt > div.inner > p")

            abstract = ""
            for abstractEl in abstractEls:
                abstract += abstractEl.get_text(strip=True) + "\n"

            imgLink = bookInfo.select_one("div.m-imgtxt > div.pic > img")["src"]
            imgLink = "https://freewebnovel.com" + imgLink
            everythingButDesc = bookInfo.select("div.m-imgtxt > div.txt > div.item")

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

            table.append(
                [
                    title,
                    score,
                    chapterLinks,
                    self.url,
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
        nChapters = len(self.novel["Chapters"])
        chapterUrls = self.novel["Chapters"]

        print(f"Scraping {chapterUrls[0]}")

        def extract_chapter_content(soup):
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

            return paragraphs

        # TODO: implement parallell requests (remove the next chapter, and just use i instead)
        # probably a dict {chap number: contents} and then sort by chap number

        with alive_bar(total=int(nChapters)) as bar:
            for index, chapterUrl in enumerate(chapterUrls):
                soup = None
                try:
                    response = requests.get(chapterUrl, headers=self.headers)
                    soup = BeautifulSoup(response.text, "html.parser")
                    CHAPTER_LINK_SELECTOR = (
                        "#main1 > div > div > div.ul-list7 > ul > li:nth-child(4) > a"
                    )
                    next_chapter = self.chapterUrl + soup.select_one(
                        CHAPTER_LINK_SELECTOR
                    ).get("href")
                except requests.exceptions.RequestException as e:
                    # TODO Handle this error
                    print(f"Error in HTTP request: {e}")
                if soup:
                    self.chapters.append(extract_chapter_content(soup))

                bar()
