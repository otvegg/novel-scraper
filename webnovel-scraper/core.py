import importlib
import os, sys
from typing import List
import pandas as pd
from websites.website import Website


def initiateClasses(directory="./websites") -> List[Website]:
    """Loads website instances from Python files in the given directory

    Args:
        directory (str): The directory to search for website files

    Returns:
        List[Website]: A list of instantiated website objects
    """
    website_instances = []

    # Get the absolute path of the directory
    abs_directory = os.path.abspath(directory)

    files = os.listdir(abs_directory)

    # Filter out all python files that start with 'website_'
    website_files = [f for f in files if f.startswith("website_") and f.endswith(".py")]

    # Iterate over all website files
    for website_file in website_files:
        file_path = os.path.join(abs_directory, website_file)
        module_name = website_file[:-3]  # Remove .py extension

        # Use importlib.util to load the module directly from the file path
        spec = importlib.util.spec_from_file_location(module_name, file_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        # Get the class name by removing 'website_' and capitalize the first letter
        class_name = module_name[len("website_") :].capitalize()

        WebsiteClass = getattr(module, class_name)

        instance = WebsiteClass()
        website_instances.append(instance)

    return website_instances


def searchWebsites(
    website_instances: list[Website], search: str
) -> pd.DataFrame | None:
    """Searches website instances for the specified search term.

    Args:
        website_instances (list[Website]): A list of instantiated website objects
        search (str): The search term to look for

    Returns:
        pd.DataFrame
    """
    results = []

    for website in website_instances:
        hits = website.search(search)

        for hit in hits:
            hit.append(website)
            results.append(hit)

    if len(results) == 0:
        return None

    df = pd.DataFrame(
        results,
        columns=[
            "Title",
            "score",
            "Chapters",
            "Website",
            "abstract",
            "author",
            "genre",
            "source",
            "original_language",
            "status",
            "alternate_names",
            "imglink",
            "estimatedDownload",
            "instance",
        ],
    )

    df["score"] = df["score"].astype("float32")

    df.index += 1
    return df
