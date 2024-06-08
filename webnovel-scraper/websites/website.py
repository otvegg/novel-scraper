import pandas as pd
from ebooklib import epub

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

        if self.novel["description"]:
            book.add_metadata('DC', 'description', self.novel["description"])

        if self.novel["score"]:
            book.add_metadata('DC', 'description', self.novel["score"])
        if self.novel["nChapters"]:
            book.add_metadata('DC', 'description', self.novel["nChapters"])
        if self.novel["original_language"]:
            book.add_metadata('DC', 'description', self.novel["original_language"])
        if self.novel["status"]:
            book.add_metadata('DC', 'description', self.novel["status"])
        if self.novel["alternate_names"]:
            book.add_metadata('DC', 'description', self.novel["alternate_names"])
        if self.novel["website"]:
            book.add_metadata('DC', 'description', self.novel["website"])

        toc = []
        all_chapters = []
        for i in range(0,len(self.chapters)):
            echapter = epub.EpubHtml(title=f"Chapter {i}", file_name=f"chapter-{i}.xhtml", lang="en")
            chapter_link = epub.Link(f"chapter-{i}.xhtml", f"Chapter {i}", f"chapter-{i}")
            toc.append(chapter_link)
            chapterContent = ''
            k = 0

            # TODO: Add image to the chapter header 
            # TODO: Chapter header
            for paragraph in self.chapters[i]:
                if k == 0:
                    print(paragraph)
                k += 1
                chapterContent += f"<p>{paragraph}</p>"
                
            echapter.set_content(f"<p>{chapterContent}</p>")
            
            all_chapters.append(echapter)
            book.add_item(echapter)
            

        all_chapters.insert(0,"nav")

        book.spine =  all_chapters
        book.toc = tuple(toc)


        book.add_item(epub.EpubNcx())
        book.add_item(epub.EpubNav())
        epub.write_epub(f"../output/{self.chosenNovel['Title'].replace(' ', '-')}.epub", book)
