import importlib
import os
import pandas as pd
from websites.website import Website

def initiateClasses() -> list[Website]:
    website_instances = []

    files = os.listdir("./websites")

    # Filter out all python files that start with 'website_'
    website_files = [f for f in files if f.startswith("website_") and f.endswith(".py")]
    print("Files", website_files)

    # Iterate over all website files
    for website_file in website_files:
        
        module_name = website_file[:-3] # Remove .py extension and import the module
        module = importlib.import_module(f"websites.{module_name}")

        # Get the class name by removing 'website_' and capitalize the first letter
        class_name = module_name[len("website_") :].capitalize()

        WebsiteClass:type[Website] = getattr(module, class_name) # Get the class from the module

        instance = WebsiteClass()
        website_instances.append(instance)
    return website_instances

def searchWebsites(website_instances:list[Website],search:str) -> pd.DataFrame:
    results = []
    for website in website_instances:
        hits = website.search(search)
        for hit in hits:
            hit.append(website)
            results.append(hit)
    
    df = pd.DataFrame(
        results, columns=["Title", "Score", "Chapters", "Website", "ChapterUrl", "instance"] 
        )
   

    df["Chapters"] = df["Chapters"].astype('int32')
    df["Score"] = df["Score"].astype('float32')
    df.index += 1
    return df

def collectNovel(novel:pd.Series):
    website = novel.instance

    # choose format

    # actually download
    website.scrape_novel(novel)
