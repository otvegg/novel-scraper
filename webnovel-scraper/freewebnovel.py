from urllib.request import urlopen
from bs4 import BeautifulSoup
import requests
import pandas as pd  # remove if i can make nice tables
from alive_progress import alive_bar, config_handler


url = "https://freewebnovel.com"
searchUrl = url + "/search/"
payload = {"searchkey": "martial world"}

response = requests.post(searchUrl, data=payload)
soup = BeautifulSoup(response.text, "html.parser")
elements = soup.select(
    "body > div.main > div.wp > div.row-box > div.col-content > div > div > div > div > div.txt"
)

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

    website = url.split("/")[2]

    table.append([title, score, n_chapters, website, link])

df = pd.DataFrame(table, columns=["Title", "Score", "Chapters", "Website", "Link"])
df.index += 1

print(df)

# Get min and max of possible values
min_value = df.index.min()
max_value = df.index.max()

# Ask for value from user
selected_novel = -1
while selected_novel > max_value or selected_novel < min_value:
    selected_novel = int(
        input("Enter the number corresponding to the novel you want to read: ")
    )
    if selected_novel > max_value or selected_novel < min_value:
        print("Incorrect value, please choose a value fitting corresponding to a novel")


# Retrieve selected novel
novel_info = df.loc[selected_novel]

print("Selected:", novel_info.Title, "with rating", novel_info.Score)


if novel_info.Website == "freewebnovel.com":
    website = "https://freewebnovel.comenovel.com"
    link = novel_info.Link.replace(".html", "/chapter-1")
else:
    website = novel_info.Website
    link = novel_info.Link
novel_url = website + link


def get_chapter_info(url: str):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    next_chapter = website + soup.select_one(
        "#main1 > div > div > div.ul-list7 > ul > li:nth-child(4) > a"
    ).get("href")

    # Check if the current chapter is the last chapter
    if url.split("-")[-1] == novel_info.Chapters:
        next_chapter = -1

    content = soup.select("#article > p")
    paragraphs = []
    for element in content:
        paragraphs.append(element.get_text(strip=True))

    return paragraphs, next_chapter


config_handler.set_global(spinner="waves")

with open(
    f'output/{novel_info.Title.replace(" ", "-")}.txt', "w", encoding="utf-8"
) as file:
    with alive_bar(int(novel_info.Chapters), title="Chapters") as bar:
        while True:
            paragraphs, novel_url = get_chapter_info(novel_url)
            for paragraph in paragraphs:
                file.write(paragraph + "\n\n")
            bar()

            # Somehow figure out we're on the last chapter and there is no more chapters
            if novel_url == -1:
                print(novel_url, novel_info.Website + novel_info.Link)
                break
