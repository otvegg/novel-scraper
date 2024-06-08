from .website import Website


class Wuxiaworld(Website):
    def __init__(self):
        self.chapterUrl = "https://wuxiaworld.site/novel/"
        self.searchUrl = "https://wuxiaworld.site/?s=martial+world&post_type=wp-manga"


    def search(self, search: str) -> list:
        return []