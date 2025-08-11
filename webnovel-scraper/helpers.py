import pandas as pd
from tabulate import tabulate
import re
import unicodedata
import os

a = "a"
b = "bɓ"
c = "cƈċ"
d = "d"
e = "eēёêèéẹ"
f = "fƒ"
r = "rɾг"
w = "wω𝑤"
n = "nηɳ"
o = "oσ0ο૦ơѳøȯọỏ"
v = "vѵν"
l = "lɭḷℓ"
m = "mɱ๓"
x = "x"


def normalize_text(text: str) -> str:
    """
    Normalize the input text by removing non-ASCII characters and converting it to lowercase.

    Args:
        text (str): The text to be normalized.

    Returns:
        str: The normalized text.
    """
    # Remove non-ASCII characters and convert to lowercase
    return "".join(
        char
        for char in unicodedata.normalize("NFKD", text)
        if unicodedata.category(char) != "Mn"
    ).lower()


def select_novel(df: pd.DataFrame) -> pd.Series | int:
    """Prompts the user to select a novel from a DataFrame by entering a corresponding number

    Args:
        df (pd.DataFrame): A DataFrame containing novel information with an index.

    Returns:
        pd.Series: A Series containing the selected novel's information
    """

    # Get min and max of possible values
    min_value = df.index.min()
    max_value = df.index.max()

    display_n_novels = os.get_terminal_size().lines - 5

    # Ask for value from user
    selected_novel = -1
    iteration = 0
    answer = ""
    b = 0

    while selected_novel > max_value or selected_novel < min_value:

        if b == max_value:
            iteration = 0

        b = iteration + display_n_novels
        if b > max_value:
            b = max_value

        os.system("cls")
        prettyPrintTable(df[iteration:b])

        answer = input(
            "Enter the number corresponding to the novel you want to read (q to exit | enter for more options): "
        )

        if answer == "":
            iteration += display_n_novels
            continue

        if answer.isdigit():
            selected_novel = int(answer)
            if selected_novel > max_value or selected_novel < min_value:
                print(
                    "Incorrect value, please choose a value fitting corresponding to a novel."
                )
                input("Press any button to continue...")
        elif answer != "q":
            print(
                "Incorrect value, please choose a value fitting corresponding to a novel."
            )
        elif answer == "q":
            return -1

    # Retrieve selected novel
    novel_info = df.loc[selected_novel]

    print("Selected:", novel_info.Title, "with rating", novel_info.score)
    return novel_info


def cleanChapterHeader(header1: str, header2: str) -> str:
    # Use the longer part (assuming it's more likely to contain the full title)
    main_part = max([header1, header2], key=len).strip()

    patterns = [
        r"^Chapter\s+[-]?\d+:?\s*-?\s*",  # Matches "Chapter 13:", "Chapter -2:", etc.
        r"^Chapter\s+[-]?\d+\s+",  # Matches "Chapter 13 ", "Chapter -2 ", etc.
        r"^\d+:?\s*",  # Matches "1:", "13 ", etc.
        r"^Chapter\s+",  # Matches "Chapter " at the beginning
    ]

    for pattern in patterns:
        main_part = re.sub(pattern, "", main_part, flags=re.IGNORECASE)

    # Pattern to match freewebnovel(.com) with possible obfuscation
    pattern = rf"[{f}]\W*[{r}]\W*[{e}]\W*[{e}]\W*[{w}]\W*[{e}]\W*[{b}]\W*[{n}]\W*[{o}]\W*[{v}]\W*[{e}]\W*[{l}](\W*[.]\W*[{c}]\W*[{o}]\W*[{m}])?"

    cleaned = re.sub(pattern, "", main_part, flags=re.IGNORECASE)
    return cleaned.strip()


def prettyPrintTable(table: pd.DataFrame) -> None:
    """
    Prints a formatted table with selected columns from the input DataFrame.

    Parameters:
        table (pd.DataFrame): The input DataFrame containing the data to be displayed.

    Returns:
        None
    """
    newtable = table[
        [
            "Title",
            "score",
            "status",
            "Chapters",
            "author",
            "estimatedDownload",
            "source",
            "Website",
        ]
    ].copy(deep=True)

    # only keep main author
    newtable["author"] = newtable["author"].str.split("&").str[0]
    newtable["Chapters"] = newtable["Chapters"].apply(len)
    # more readable format
    newtable["estimatedDownload"] = (
        newtable["estimatedDownload"].round().apply(pd.to_timedelta, unit="s")
    )

    # rename columns
    newtable = newtable.rename(
        columns={
            "author": "Author",
            "estimatedDownload": "DL time",
            "score": "Score",
            "status": "Status",
            "source": "Source",
        }
    )

    def truncate(x, cutoff_value):
        return (
            x[:cutoff_value] + "..."
            if isinstance(x, str) and len(x) > cutoff_value
            else x
        )

    def format_timedelta(td):
        total_seconds = int(td.total_seconds())
        hours, remainder = divmod(total_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        if hours > 0:
            return f"{hours:02}:{minutes:02}:{seconds:02}"
        else:
            return f"{minutes:02}:{seconds:02}"

    newtable["DL time"] = newtable["DL time"].apply(format_timedelta)

    newtable["Title"] = newtable["Title"].apply(lambda x: truncate(x, 30))
    newtable["Author"] = newtable["Author"].apply(lambda x: truncate(x, 15))

    # newtable = newtable.applymap(truncate)
    newtable["Website"] = newtable["Website"].apply(lambda x: x.replace("https://", ""))

    print(tabulate(newtable, headers="keys", tablefmt="psql"))


def remove_advertisement(text: str) -> str:
    # Pattern to match freewebnovel(.com) with possible obfuscation
    # Look into python homoglyph libraries?
    pattern_freewebnovel = rf"[{f}][\W_.]*[{r}][\W_.]*[{e}][\W_.]*[{e}][\W_.]*[{w}][\W_.]*[{e}][\W_.]*[{b}][\W_.]*[{n}][\W_.]*[{o}][\W_.]*[{v}][\W_.]*[{e}][\W_.]*[{l}]([\W_.]*[{c}][\W_.]*[{o}][\W_.]*[{m}])?"
    pattern_daonovel = rf"[{d}][\W_.]*[{a}][\W_.]*[{o}][\W_.]*[{n}][\W_.]*[{o}][\W_.]*[{v}][\W_.]*[{e}][\W_.]*[{l}]([\W_.]*[{c}][\W_.]*[{o}][\W_.]*[{m}])?"
    pattern_boxnovel = rf"[{b}][\W_.]*[{o}][\W_.]*[{x}][\W_.]*[{n}][\W_.]*[{o}][\W_.]*[{v}][\W_.]*[{e}][\W_.]*[{l}]([\W_.]*[{c}][\W_.]*[{o}][\W_.]*[{m}])?"

    patterns = [pattern_freewebnovel, pattern_daonovel, pattern_boxnovel]
    combined_pattern = "|".join(patterns)

    # Remove parentheses surrounding advertisements
    text = re.sub(rf"\(\s*({combined_pattern})[\s.]*\)", "", text, flags=re.IGNORECASE)

    # Remove "read only at" and similar phrases, including everything after
    read_patterns = [
        r"read\s+(?:more|only)\s+(?:on|at)",
        r"search.*on\s+google",
        r"you['']re\s+reading\s+on",
        r"tks!",
        r"You’re reading",
    ]
    read_combined = "|".join(read_patterns)

    # Combine all patterns
    full_pattern = rf"({combined_pattern}|{read_combined}).*$"

    # Remove advertisements and related phrases from the entire text
    cleaned_text = re.sub(full_pattern, "", text, flags=re.IGNORECASE | re.DOTALL)

    # Remove any trailing whitespace or punctuation
    # cleaned_text = re.sub(r'[.!?]\s*$', '', cleaned_text.strip())

    return cleaned_text


def is_advertisement(text: str) -> bool:
    """
    Check if the given text contains any advertisement patterns.

    Args:
        text (str): The text to check for advertisement patterns.

    Returns:
        bool: True if any advertisement pattern is found, False otherwise.
    """
    normalized_text = normalize_text(text)

    # More specific patterns to match
    patterns = [
        r"\bfreewebnovel\b",
        r"visit.*for.*novel.*experience",
        r"read.*chapters.*at",
        r"content.*taken.*from",
        r"source.*of.*this.*content",
        r"updated.*from",
        r"chapter.*updated.*by",
        r"chapters.*published.*on",
        r"novels.*published.*on",
        r"follow.*current.*novels",
        r"for.*the.*best.*novel.*reading",
        r"most.*uptodate.*novels",
        r"latest.*chapters.*at",
        r"new.*novel.*chapters",
        r"free.*web.*novel",
        r"ew.*bn.*vel",
    ]

    # Check if any pattern matches
    return any(re.search(pattern, normalized_text) for pattern in patterns)
