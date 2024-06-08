import pandas as pd


class Website:
    def __init__(self):
        self.url = None
        self.chapters:list[list[str]] = []
        self.headers = {"User-Agent": "Mozilla/5.0 (X11; CrOS x86_64 12871.102.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.141 Safari/537.36"}
        self.format = None
        self.supportedFormats = ['txt'] #  'epub', 'pdf'
        self.chosenNovel:pd.Series = None

    def search(self, searchstring: str) -> list[list]:
        print("Not implemented {search}")

    def select_novel(self, index: int):
        print("Not implemented {select_novel}")

    def scrape_novel(self, novel: str) -> tuple[int,str,int]:
        print("Not implemented {scrape_novel}")

    def setFormat(self) -> None:
        format = ''
        while format not in self.supportedFormats and format.upper() != 'Q':
            format = input(f"Enter file format {self.supportedFormats}: ")
            
            if format not in self.supportedFormats:
                print("Incorrect format.")
            else:
                self.format = format
    
    def setNovel(self, novel:pd.Series):
        self.chosenNovel = novel


    def saveFile(self):
        if self.format == 'txt':
            self.saveTXT()    
        elif self.format == 'pdf':
            self.savePDF()
        elif self.format == 'epub':
            self.saveEPUB()
    
    def saveTXT(self):
        with open(f'../output/{self.chosenNovel['Title'].replace(' ', '-')}.txt', 'w') as f:
            for chapter in self.chapters:
                for paragraph in chapter:
                    f.write(paragraph)
                    f.write('\n\n')
        
        pass

    def savePDF(self):
        pass

    def saveEPUB(self):
        pass


