import pandas as pd
import pycountry

allowed_formats = ["txt"]  # To add: epub, pdf


def is_iso_639_compliant(tag: str) -> bool:
    """
    Check if a language tag is compliant with ISO 639-1 or ISO 639-3.

    Parameters:
        tag (str): The language tag to be checked.

    Returns:
        bool: True if the tag is compliant, False otherwise.

    Example:
        >>> is_iso_639_compliant('nn')
        True

    Note:
        This function uses the pycountry library to check if the tag is in ISO 639-1 or ISO 639-3.
        If the tag is not found or an error occurs, False is returned.
    """
    try:
        # Check if the tag is in ISO 639-1 or ISO 639-3
        if pycountry.languages.get(alpha_2=tag) or pycountry.languages.get(alpha_3=tag):
            return True
        else:
            return False
    except (KeyError, AttributeError):
        return False


def select_file_format():
    """
    Prompt the user to enter a desired file format and validate the input. Q to exit.

    Returns:
        str: The selected file format.
    """
    file_format = -1
    while file_format not in allowed_formats:
        file_format = input("Enter the wanted file format: ")

        if file_format.upper() == "Q":
            return -1

        if file_format not in allowed_formats:
            print(f"Please choose between [{', '.join(allowed_formats)}].")
    return file_format


def select_novel(df: pd.DataFrame)-> pd.Series:
    """Prompts the user to select a novel from a DataFrame by entering a corresponding number

    Args:
        df (pd.DataFrame): A DataFrame containing novel information with an index.

    Returns:
        pd.Series: A Series containing the selected novel's information
    """

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
            print(
                "Incorrect value, please choose a value fitting corresponding to a novel."
            )

    # Retrieve selected novel
    novel_info = df.loc[selected_novel]

    print("Selected:", novel_info.Title, "with rating", novel_info.Score)
    return novel_info