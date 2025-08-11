import pandas as pd
from ebooklib import epub
import helpers
import requests

# Notes:
# ipv4 might cause read timeouts


class Website:
    def __init__(self):
        self.url = None
        self.chapters: list[list[str]] = []
        self.headers = {
            "User-Agent": "Mozilla/5.0 (X11; CrOS x86_64 12871.102.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.141 Safari/537.36"
        }
        self.format = None
        self.supportedFormats = ["txt", "epub"]  #  'pdf'
        self.novel: pd.Series = None

    def search(self, searchkey: str) -> list[list]:
        """Search website for searchkey

        Args:
            searchkey (str): parameter sent to the website

        Returns:
            list[list]: list of hits, each hit containing information about the hit
        """
        print("Not implemented {search}")

    def scrape_novel(self) -> tuple[int, str, int]:
        """Scrapes webnovel

        Returns:
            tuple[int,str,int]: List of chapters, chapters are list of paragraphs (lines divided by '\\n')
        """
        print("Not implemented {scrape_novel}")

    def setFormat(self) -> None:
        """Chooses format to save file with"""
        format = ""
        while format not in self.supportedFormats and format.upper() != "Q":
            format = input(f"Enter file format {self.supportedFormats}: ")

            if format not in self.supportedFormats:
                print("Incorrect format.")
            else:
                self.format = format

    def setNovel(self, novel: pd.Series):
        """
        Set the novel data for the Website instance.

        Parameters:
        novel (pd.Series): A pandas Series containing novel data.

        Returns:
        None
        """

        self.novel = novel

    def saveFile(self) -> None:
        """Saves file to specified format"""
        if self.format == "txt":
            self.saveTXT()
        elif self.format == "pdf":
            self.savePDF()
        elif self.format == "epub":
            self.saveEPUB()

    def saveTXT(self) -> None:
        """
        Saves the novel content in a TXT file with chapters separated by double newlines.

        Returns:
            None
        """
        with open(
            f"../output/{self.novel['Title'].replace(' ', '-')}.txt",
            "w",
            encoding="utf-8",
        ) as f:
            for chapter in self.chapters:
                for paragraph in chapter:
                    f.write(paragraph)
                    f.write("\n\n")

    def savePDF(self) -> None:

        pass

    def saveEPUB(self) -> None:
        """
        Saves the novel content in EPUB format with metadata such as title, author, description,
        rating, publisher, chapters, original language, status, alternate names, and cover image.

        Returns:
            None
        """
        book = epub.EpubBook()

        book.set_identifier("sample123456")
        book.set_title(self.novel["Title"])
        book.set_language("en")
        book.add_metadata("DC", "description", self.novel["abstract"])
        book.add_metadata("DC", "type", "novel")

        if self.novel["author"]:
            book.add_author(self.novel["author"])

            # TODO: add metadata ?
            # main author -> Creator
            # secondary authors -> contributors

        if self.novel["abstract"]:
            book.add_metadata("DC", "format", "EPUB")

            # TODO: try to infer DC subject from abstract?

        if self.novel["score"]:
            normalizedScore = self.novel["score"] / 5 * 10
            book.add_metadata(
                None,
                "meta",
                "",
                {"name": "calibre:rating", "content": f"{float(normalizedScore)}"},
            )
            book.add_metadata(
                None,
                "meta",
                "",
                {"name": "rating", "content": f"{float(normalizedScore)}"},
            )

        if self.novel["source"]:
            book.add_metadata("DC", "publisher", self.novel["source"])

        if self.novel["Chapters"]:
            book.add_metadata(
                None,
                "meta",
                "",
                {"name": "chapters", "content": f'{self.novel["Chapters"]}'},
            )

        if self.novel["original_language"]:
            book.add_metadata(
                None,
                "meta",
                "",
                {"name": "origLang", "content": f'{self.novel["original_language"]}'},
            )

        if self.novel["status"]:
            book.add_metadata(
                None,
                "meta",
                "",
                {"name": "status", "content": f'{self.novel["status"]}'},
            )

        if self.novel["alternate_names"]:
            book.add_metadata(
                None,
                "meta",
                "",
                {"name": "altNames", "content": f'{self.novel["alternate_names"]}'},
            )

        # TODO: If missing, use generative AI to create a cover? Feeding the abstract/summary?
        if self.novel["imglink"]:
            img_data = requests.get(self.novel["imglink"]).content
            book.set_cover(self.novel["Title"], img_data)

        # TODO: Add image to the chapter header
        # TODO: Chapter styling
        toc = []
        all_chapters = []
        for i, chapter in enumerate(self.chapters):
            echapter = epub.EpubHtml(
                title=f"Chapter {i+1}", file_name=f"chapter-{i+1}.xhtml", lang="en"
            )
            chapter_link = epub.Link(
                f"chapter-{i+1}.xhtml", f"{chapter[0]}", f"chapter-{i+1}"
            )
            toc.append(chapter_link)

            chapter_header = f"<h1 style='font-size: 24px;'>{i+1} - {chapter[0]}</h1>"
            chapter_content = "".join(
                [f"<p>{paragraph}</p>" for paragraph in chapter[1:]]
            )
            echapter.set_content(f"{chapter_header}{chapter_content}")

            all_chapters.append(echapter)
            book.add_item(echapter)

        all_chapters.insert(0, "nav")

        book.spine = all_chapters
        book.toc = tuple(toc)

        book.add_item(epub.EpubNcx())
        book.add_item(epub.EpubNav())
        epub.write_epub(f"../output/{self.novel['Title'].replace(' ', '-')}.epub", book)


""" 
DC metadata
Creator: Identifies the primary creator or author.
Contributor: Lists additional contributors or authors.
Publisher: Indicates the entity responsible for publishing or distributing the resource.
Title: Provides the title or name of the resource.
Date: Specifies the date associated with the resource.
Language: Describes the language of the resource.
Format: Describes the file format or physical medium.
Subject: Represents the topic or subject matter.
Description: Offers a brief summary or abstract.
Identifier: Provides a unique identifier for the resource.
Relation: Describes relationships with other resources.
Source: Indicates the original source of the resource.
Type: Specifies the resource type (e.g., text, image, video).
Coverage: Describes the spatial or temporal coverage.
Rights: Specifies rights information or access restrictions. 
"""
