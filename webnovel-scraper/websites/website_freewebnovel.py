import timeit
from alive_progress import alive_bar
from bs4 import BeautifulSoup
import pandas as pd
import requests
from .website import Website


class Freewebnovel(Website):
    def __init__(self):
        super().__init__()
        self.chapterUrl = "https://freewebnovel.comenovel.com"
        self.url = "https://freewebnovel.com"
        self.searchUrl = self.url + "/search/"
        
        

    def search(self, search: str) -> list:

        payload = {"searchkey": search} 
        response = requests.post(self.searchUrl, data=payload, headers=self.headers)#, timeout=1)

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

            firstChapter = self.chapterUrl + link.replace(".html", "/chapter-1")

            table.append([title, score, n_chapters, self.url, firstChapter])


        return table

        

    def scrape_novel(self):
        title, score, nChapters, website, chapterUrl, instance = self.chosenNovel

        curUrl = chapterUrl
        i = 0

        # implement parallell requests (remove the next chapter, and just use i instead)
        # probably a dict {chap number: contents} and then sort by chap number
        with alive_bar(total=int(nChapters)) as bar:
            for i in range(1, nChapters+1):
                
                bar()

                response = requests.get(curUrl, headers=self.headers)
                soup = BeautifulSoup(response.text, "html.parser")
                next_chapter = self.chapterUrl + soup.select_one(
                    "#main1 > div > div > div.ul-list7 > ul > li:nth-child(4) > a"
                ).get("href")
            
                content = soup.select("#article > p")
                paragraphs = []
                for element in content:
                    paragraphs.append(element.get_text(strip=True))

                paragraphs = paragraphs[:-1]  # Remove last paragraph (advertisement)
                self.chapters.append(paragraphs)

                curUrl = next_chapter