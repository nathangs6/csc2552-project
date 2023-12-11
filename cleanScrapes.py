import re
import pandas as pd
import csv
import time
from pathlib import Path

articlesFolder          = "scrapers/output/"
unionFilename           = "data/output/unions.txt"
outputFilename          = "data/output/data2023.csv"

leanings = {
        "washingtonpost": ["left",False],
        "breitbart": ["right",True],
        "cnn": ["left",True],
        "nytimes": ["left",False],
        "reuters": ["centre",False],
        "theatlantic": ["left",False],
        "newyorker": ["left",True],
        "foxnews": ["right",True],
        "alternet": ["left",True],
        "bloomberg": ["left",False],
        "theblaze": ["right",True],
        "nypost": ["right",False],
        "bbc": ["centre",False],
        "politico": ["left",False],
        "dailycaller": ["right",True],
        "reason": ["right",False],
        "usatoday": ["left",False],
        "npr": ["centre",False],
        "vox": ["left",True],
        "theguardian": ["left",False],
        "abcnews": ["left",False],
        "nationalreview": ["right",True],
        "cbsnews": ["left",False],
        "nbcnews": ["left",False],
        "thehill": ["centre",False],
        "theintercept": ["left",True],
        "forbes": ["centre",False],
        "dailymail": ["right",True],
        "dailywire": ["right",True],
        "huffpost": ["left",True],
        "apnews": ["centre",False],
        "msn": ["left",True],
        "csmonitor": ["centre",False],
        "democracynow": ["left",True],
        "thefederalist": ["right",True],
        "washingtonexaminer": ["right",False],
        "buzzfeed": ["left",True],
        "washingtontimes": ["right",False],
        "slate": ["left",True],
        "economist": ["left",False],
        "thedailybeast": ["left",True],
        "spectator": ["right",True],
        "axios": ["centre",False],
        "wsj": ["centre",False],
        "time": ["left",False],
        "motherjones": ["left",True],
        "theepochtimes": ["right",False],
        "foxnewsinsider": ["right",True]
}

def getUnions():
    with open(unionFilename) as fp:
        potential = fp.read().split("\n")
        not_allowed = ["pass", "cope", "smart"]
        unions = []
        for union in potential:
            if union not in not_allowed:
                unions.append(union)
    return unions

def getArticleData(articlesFilename):
    """
    Get the initial article data.
    """
    # Load data
    data = pd.read_csv(articlesFilename, encoding="utf-8")
    # Eliminate December data
    data['date_column'] = pd.to_datetime(data['date'])
    data = data[data['date_column'].dt.month != 12]
    # Get relevant columns
    relevantColumns = ["url", "date", "title", "content", "domain"]
    data            = data[relevantColumns]
    # Drop Duplicates
    data = data.drop_duplicates(subset="title", keep='first')
    return data

def articleMask(row, unions) -> bool:
    """
    Row-wise mask for article filtering.
    """
    # Clean content
    tempContent = row.content.lower()
    tempContent = re.sub("[^a-zA-Z0-9]", " ", tempContent)
    tempContent = " " + tempContent + " "

    # Clean title
    tempTitle = row.title.lower()
    tempTitle = re.sub("[^a-zA-Z0-9]", " ", tempTitle)
    tempTitle = " " + tempTitle + " "

    for union in unions:
        unionCheck = " " + union + " "
        if unionCheck in tempContent or unionCheck in tempTitle:
            return True
    return False


def filterArticles(data, unions):
    """
    Filter the articles.
    """
    # Remove those in the wrong years
    m = data.apply(articleMask, axis=1, unions=unions)
    keptData = data[m]
    return keptData

def addLeaning(row):
    return leanings[row["domain"]][0]


def constructMetadata(data):
    """
    Construct the metadata for each article.
    """
    data["leaning"] = data.apply(addLeaning, axis=1)
    return data


def getAllArticles(unions):
    data = pd.DataFrame({
        "url": [],
        "date": [],
        "title": [],
        "content": [],
        "domain": [],
        "leaning": []
    })
    for filePath in sorted(Path(articlesFolder).glob('*.csv')):
        print("Adding data for: " + filePath.name)
        newData = getArticleData(filePath)
        newData = filterArticles(newData, unions)
        if newData.empty: continue
        newData = constructMetadata(newData)
        data = pd.concat([data, newData], ignore_index=True)
    return data


def constructData():
    """
    Coordinate the construction of the data and write to a CSV file for use in the STM model.
    """
    print("Getting unions... ", end="")
    unions  = getUnions()
    print("done!")
    print("Loading article data")
    data    = getAllArticles(unions)
    print("done!")
    return data


def consoleReport(data):
    print("Number of documents:", data.shape[0])
    print("Number of left-leaning documents:", data[data["leaning"] == "left"].shape[0])
    print("Number of right-leaning documents:", data[data["leaning"] == "right"].shape[0])



def main():
    print("Making data!")
    data = constructData()
    print("Outputting full data... ", end="")
    data.to_csv(outputFilename, sep=",", encoding="utf-8")
    print("done!")
    print("Summary Report")
    consoleReport(data)



if __name__ == "__main__":
    main()
