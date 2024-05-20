from alive_progress import alive_bar
import websites
import helpers
import to_file


def initiate():
    # Search through possible
    results = websites.search_websites("martial world")

    novel_info = helpers.select_novel(results)

    file_format = helpers.select_file_format()
    if file_format == -1:
        print("Error with fileformat")
        return -1

    # Create file
    filePath = to_file.create_file(
        file_format, f'{novel_info.Title.replace(" ", "-")}.txt'
    )
    if filePath == -1:
        print("Error creating file")
        return -1

    novel_url = novel_info.ChapterUrl
    with alive_bar(int(novel_info.Chapters), title="Chapters") as bar:
        while True:
            current_chapter, paragraphs, novel_url = websites.get_chapter_info(
                novel_info, novel_url
            )
            # append to file
            to_file.append_file(file_format, filePath, current_chapter, paragraphs)
            bar()

            # Reach last chapter, so we exit
            if novel_url == -1:
                break


initiate()
