from bs4 import BeautifulSoup
import requests
from websites.website import Website


class Wuxiaworld_site(Website):
    def __init__(self):
        super().__init__()
        self.chapterUrl = "https://wuxiaworld.site/novel/"
        self.searchUrl = "https://wuxiaworld.site/?"
        self.BATCH_SIZE = 25
        self.WAIT_TIME = 10
        self.RATELIMIT = 3

    def search(self, searchkey: str):
        return []

        payload = {"s": searchkey, "post_type": "wp_manga"}

        response = requests.get(self.searchUrl, data=payload, headers=self.headers)

        soup = BeautifulSoup(response.text, "html.parser")

        searchResults = soup.select(
            "body > div.wrap > div > div.site-content > div.c-page-content > div > div > div > div > div.main-col-inner > div > div.tab-content-wrap > div > div"
        )

        print(len(searchResults))
        return searchResults

    def do(self):
        return "Hey!"
