import timeit
from alive_progress import alive_bar
from bs4 import BeautifulSoup
import pandas as pd
import requests
from .website import Website
import helpers
from requests_futures.sessions import FuturesSession
import logging
import time


class Freewebnovel(Website):
    def __init__(self):
        super().__init__()
        self.chapterUrl = "https://freewebnovel.comenovel.com"
        self.url = "https://freewebnovel.com"
        self.searchUrl = self.url + "/search/"
        self.BATCH_SIZE = 25
        self.WAIT_TIME = 10
        self.RATELIMIT = 3

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
            chapterLinks = []
            for i in chapters:
                chapterLinks.append(
                    self.chapterUrl + i.get("href").replace(".html", "")
                )

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

    def extract_chapter_content(self, soup, index):
        paragraphs = []

        # Check if the soup object is valid
        if not soup or not isinstance(soup, BeautifulSoup):
            logging.error(f"Invalid soup object for chapter {index}")
            return None

        # Try to get the chapter title
        title_element = soup.select_one("#main1 > div > div > div.top > span")
        if title_element is None:
            logging.error(f"Could not find chapter title for chapter {index}")
            # Log the first 500 characters of the HTML to see what we're dealing with
            logging.debug(f"HTML snippet: {soup.prettify()[:500]}")
            return None

        chapter_title = title_element.get_text()

        content = soup.select("#article > p")
        if not content:
            logging.error(f"Could not find chapter content for chapter {index}")
            return None

        for element in content:
            p = element.get_text(strip=True)
            p = helpers.remove_advertisement(p)
            paragraphs.append(p)

        # get actual header (webnovel serves 2 headers, and it varies where the "proper" header is)
        paragraphs[0] = helpers.cleanChapterHeader(chapter_title, paragraphs[0])

        return paragraphs

    def scrape_novel(self):
        nChapters = len(self.novel["Chapters"])
        chapterUrls = self.novel["Chapters"]

        session = FuturesSession(max_workers=self.BATCH_SIZE)
        futures = []

        interval = 1 / self.RATELIMIT

        # Create futures for all requests
        for index, chapterUrl in enumerate(chapterUrls):
            logging.info(f"Creating future for chapter {index} from {chapterUrl}")
            future = session.get(chapterUrl, headers=self.headers)
            futures.append((index, future))
            time.sleep(interval)

        # Process completed futures
        with alive_bar(total=int(nChapters)) as bar:
            for index, future in futures:
                try:
                    response = future.result()
                    logging.info(f"Received response for chapter {index}")

                    soup = BeautifulSoup(response.text, "html.parser")
                    chapter_content = self.extract_chapter_content(soup, index)
                    if chapter_content is not None:
                        self.chapters.append((index, chapter_content))
                    else:
                        logging.warning(
                            f"Skipping chapter {index} due to extraction failure.\nStatus code: {response.status_code}"
                        )
                except requests.exceptions.RequestException as e:
                    logging.error(f"Error in HTTP request for chapter {index}: {e}")
                except Exception as e:
                    logging.error(f"Unexpected error processing chapter {index}: {e}")

                bar()

        self.chapters = sorted(self.chapters)
        self.chapters = [list(sublist)[1:][0] for sublist in self.chapters]
