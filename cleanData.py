import re
import pandas as pd
import csv
import time

articlesFilename        = "data/input/articles.csv"
metadataFilename        = "data/input/unions_full_metadata.csv"
unionFilename           = "data/output/unions.txt"
outputFilename          = "data/output/cleanedData.csv"
farFilename             = "data/output/farData.csv"
eliminatedFilename      = "data/output/eliminatedData.csv"

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

def getArticleData(articlesFilename):
    """
    Get the initial article data.
    """
    # Load data
    data        = pd.read_csv(articlesFilename, encoding="utf-8")
    metadata    = pd.read_csv(metadataFilename, encoding="utf-8")
    metadata    = metadata.drop("title", axis=1)
    data        = pd.merge(data, metadata, on="url")
    # Get relevant columns
    relevantColumns = ["actual_domain", "title", "body", "created_utc", "url"]
    data            = data[relevantColumns]
    # Rename columns
    columnNames = {"actual_domain": "domain", "body": "content", "created_utc": "date"}
    data        = data.rename(columns=columnNames)
    # Drop Duplicates
    data = data.drop_duplicates(subset="title", keep='first')
    # Drop irrelevant dates
    data["year"] = pd.to_datetime(data["date"], unit="s").dt.year
    data = data[data["year"] != 2006]
    data = data[data["year"] != 2007]
    data = data.drop("year", axis=1)
    return data

def getUnions():
    """
    Get the union data.
    """
    with open(unionFilename) as fp:
        potential = fp.read().split("\n")
        # The following union acronyms are overloaded with potentially very common words,
        # so we remove them
        not_allowed = ["pass", "cope", "smart"]
        unions = []
        for union in potential:
            if union not in not_allowed:
                unions.append(union)
    return unions


def articleMask(row, unions) -> bool:
    """
    Row-wise mask for article filtering.
    """
    # Clean content
    tempContent = row.content.lower()
    tempContent = re.sub("[^a-zA-Z0-9]", " ", tempContent)
    tempContent = " " + tempContent + " "

    # Clean title
    tempTitle = row.content.lower()
    tempTitle = re.sub("[^a-zA-Z0-9]", " ", tempTitle)
    tempTitle = " " + tempTitle + " "

    explicitUnionCheck = True

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
    eliminatedData = data[~m]
    keptData = data[m]
    return keptData, eliminatedData



def addLeaning(row):
    """
    For the given row, return the leaning associated with that row's domain.
    """
    return leanings[row.domain][0]


def addFarLeaning(row):
    """
    For a given row, return whether that row's domain leans far in either political direction."
    """
    if leanings[row.domain][1] == True:
        if leanings[row.domain][0] == "right":
            return "right"
        else:
            return "left"
    return -1


def constructMetadata(data):
    """
    Construct the metadata for each article.
    """
    data["leaning"] = data.apply(addLeaning, axis=1)
    data["far"] = data.apply(addFarLeaning, axis=1)
    return data


def constructData(outputTest):
    """
    Coordinate the construction of the data and write to a CSV file for use in the STM model.
    """
    print("Loading article data... ", end="")
    data = getArticleData(articlesFilename)
    print("done!")
    print("Original total number of documents:", data.shape[0])
    if outputTest:
        print("Restricting to test data length... ", end="")
        data = data.sample(200)
        print("done!")
    print("Getting unions... ", end="")
    unions = getUnions()
    print("done!")
    print("Filtering Articles... ", end="")
    data, eliminatedData = filterArticles(data, unions)
    print("done!")
    print("Constructing metadata... ", end="")
    data = constructMetadata(data)
    print("done!")
    return data, eliminatedData


def consoleReport(data, eliminatedData, farData):
    """
    Print a summary of data.
    """
    print("Number of documents:", data.shape[0])
    print("Number of domains:", len(data["domain"].unique()))
    print("Number of left-leaning documents:",
          data[data["leaning"] == "left"].shape[0])
    print("Number of right-leaning documents:",
          data[data["leaning"] == "right"].shape[0])
    print("Number of eliminated documents:", eliminatedData.shape[0])
    print("Number of highly polarized documents:", farData.shape[0])




def main(outputTest):
    startStr = "Cleaning data "
    if outputTest == True:
        startStr += "and outputting test data"
    else:
        startStr += "and outputting complete data"
    print("----------")
    print(startStr)
    data, eliminatedData = constructData(outputTest)
    print("Outputting full data... ", end="")
    data.to_csv(outputFilename, sep=",", encoding="utf-8")
    print("done!")
    print("Outputting eliminated data... ", end="")
    eliminatedData.to_csv(eliminatedFilename, sep=",", encoding="utf-8")
    print("done!")
    print("Outputting far data... ", end="")
    farData = data[data["far"] != -1]
    farData.to_csv(farFilename, sep=",", encoding="utf-8")
    print("done!")
    print("Summary Report")
    consoleReport(data, eliminatedData, farData)



if __name__ == "__main__":
    outputType = input("Type t for test data: ")
    if outputType == "t":
        outputTest = True
    else:
        outputTest = False
    main(outputTest)
