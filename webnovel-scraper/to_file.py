import ebooklib
from ebooklib import epub


def create_file(filetype: str, filename: str):
    """
    Create a file of the specified type.

    Parameters:
    - filetype (str): The type of file to create. Valid options are "txt", "epub", and "pdf".
    - filename (str): The name of the file to create.

    Returns:
    - int: Returns -1 if an invalid filetype is provided.

    Example:
    - create_file("txt", "my_text_file")  # Creates a text file named "my_text_file.txt"
    - create_file("epub", "my_epub_file")  # Creates an EPUB file named "my_epub_file.epub"
    - create_file("pdf", "my_pdf_file")  # Creates a PDF file named "my_pdf_file.pdf"
    - create_file("doc", "my_doc_file")  # Returns -1, as "doc" is an invalid filetype.
    """
    filepath = "output/" + filename
    if filetype == "txt":
        create_txt(filepath)
    elif filetype == "epub":
        create_epub(filepath)
    elif filetype == "pdf":
        create_pdf(filepath)
    else:
        return -1
    return filepath


def append_file(filetype: str, filePath: str, chapter: str, paragraphs: list):
    if filetype == "txt":
        append_txt(filePath, chapter, paragraphs)
    elif filetype == "epub":
        append_epub(filePath, chapter, paragraphs)
    elif filetype == "pdf":
        append_pdf(filePath, chapter, paragraphs)
    else:
        return -1
    return 0


def create_txt(path: str):
    open(path, "w").close()


def append_txt(path: str, chapter: str, paragraphs: list):
    # Write to text
    f = open(path, "a", encoding="UTF-8")
    for paragraph in paragraphs:
        f.write(paragraph + "\n\n")
    f.close()


def create_pdf(path: str):
    open(path, "w").close()


def append_pdf(path: str, chapter: str, paragraphs: list):
    pass


def create_epub(
    path: str,
    identifier: str,
    title: str,
    language: str = "en",
    author=None,
):
    book = epub.EpubBook()

    book.set_identifier(identifier)
    book.set_title(title)
    book.set_language(language)
    if author:
        book.add_author(
            "Test",
            file_as="Test as",
            role="ill",
            uid="coauthor",
        )

    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())

    # define CSS style
    style = "BODY {color: white;}"
    nav_css = epub.EpubItem(
        uid="style_nav", file_name="style/nav.css", media_type="text/css", content=style
    )

    # add CSS file
    book.add_item(nav_css)

    # create spine
    book.spine = ["nav"]

    # create epub file
    epub.write_epub(path, book, {})


def append_epub(path: str, chapter: str, paragraphs: list):
    # read epub
    book = epub.read_epub(path)

    c1 = epub.EpubHtml(title="Chapter 1", file_name="chap_01.xhtml", lang="en")
    c1.content = "<h1>Chapter 1</h1><p>%s</p>" % "content"

    # add chapter
    book.add_item(c1)

    # define Table Of Contents
    book.toc = (c1,)
