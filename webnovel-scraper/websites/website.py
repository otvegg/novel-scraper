import pandas as pd
from ebooklib import epub
import helpers
# Notes:
# ipv4 might cause read timeouts

class Website:
    def __init__(self):
        self.url = None
        self.chapters:list[list[str]] = []
        self.headers = {"User-Agent": "Mozilla/5.0 (X11; CrOS x86_64 12871.102.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.141 Safari/537.36"}
        self.format = None
        self.supportedFormats = ['txt', 'epub'] #  'epub', 'pdf'
        self.chosenNovel:pd.Series = None
        self.novel = {
            "title":None,
            "author":None,
            "description":None,
            "score":None,
            "nChapters":None,
            "original_language":None,
            "alternate_names":None,
            "status":None,
            "instanse":None,
            "chapterUrl":None,
            "website":None
        }

    def search(self, searchkey: str) -> list[list]:
        """Search website for searchkey

        Args:
            searchkey (str): parameter sent to the website

        Returns:
            list[list]: list of hits, each hit containing information about the hit
        """
        print("Not implemented {search}")

    def scrape_novel(self) -> tuple[int,str,int]:
        """Scrapes webnovel

        Returns:
            tuple[int,str,int]: List of chapters, chapters are list of paragraphs (lines divided by '\\n')
        """
        print("Not implemented {scrape_novel}")

    def setFormat(self) -> None:
        """Chooses format to save file with
        """
        format = ''
        while format not in self.supportedFormats and format.upper() != 'Q':
            format = input(f"Enter file format {self.supportedFormats}: ")
            
            if format not in self.supportedFormats:
                print("Incorrect format.")
            else:
                self.format = format
    
    def setNovel(self, novel:pd.Series):
        self.chosenNovel = novel


    def saveFile(self) -> None:
        """Saves file to specified format
        """
        if self.format == 'txt':
            self.saveTXT()    
        elif self.format == 'pdf':
            self.savePDF()
        elif self.format == 'epub':
            self.saveEPUB()
    
    def saveTXT(self) -> None:
        """Saves downloaded novel to PDF format
        """
        with open(f'../output/{self.chosenNovel['Title'].replace(' ', '-')}.txt', 'w', encoding="utf-8") as f:
            for chapter in self.chapters:
                for paragraph in chapter:
                    f.write(paragraph)
                    f.write('\n\n')
        

    def savePDF(self) -> None:
        """Saves downloaded novel to PDF format
        """
        pass

    def saveEPUB(self) -> None:
        """Saves downloaded novel to ePub format
        """
        book = epub.EpubBook()

        book.set_identifier('sample123456')
        book.set_title(self.chosenNovel['Title'])
        book.set_language('en')

        if self.novel["author"]:
            book.add_author(self.novel["author"])

        metadata_fields = ["description", "score", "nChapters", "original_language", "status", "alternate_names", "website"]
        for field in metadata_fields:
            if self.novel[field]:
                book.add_metadata('DC', field, self.novel[field])


        # TODO: Add image to the chapter header 
        # TODO: Chapter styling
        toc = []
        all_chapters = []
        for i, chapter in enumerate(self.chapters):
            echapter = epub.EpubHtml(title=f"Chapter {i}", file_name=f"chapter-{i}.xhtml", lang="en")
            cleanedHeader = helpers.cleanChapterHeader(chapter[0])
            chapter_link = epub.Link(f"chapter-{i+1}.xhtml", f"{cleanedHeader}", f"chapter-{i+1}")
            toc.append(chapter_link)

            chapter_header = f"<h1 style='font-size: 24px;'>{chapter[0]}</h1>"
            chapter_content = ''.join([f"<p>{paragraph}</p>" for paragraph in chapter[1:]])
            echapter.set_content(f"{chapter_header}{chapter_content}")
        
            all_chapters.append(echapter)
            book.add_item(echapter)

        all_chapters.insert(0,"nav")

        book.spine =  all_chapters
        book.toc = tuple(toc)


        book.add_item(epub.EpubNcx())
        book.add_item(epub.EpubNav())
        epub.write_epub(f"../output/{self.chosenNovel['Title'].replace(' ', '-')}.epub", book)
