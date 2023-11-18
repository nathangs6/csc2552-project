import matplotlib.pyplot as plt
import pandas as pd


def getData(cleanedDataFilename: str):
    """
    Get the cleaned data for further analysis.
    """
    data = pd.read_csv(cleanedDataFilename)
    return data

def getDomainCounts(data, outputFolder):
    """
    Get and plot domain counts of articles.
    """
    outputFilename = outputFolder + "domainCounts.pdf"
    domainCounts = data[["domain", "leaning"]].value_counts().to_frame(name="count").reset_index()
    domainCounts.plot.scatter(title="Number of Articles Per Domain", x="domain", xlabel="Domain", y="count", ylabel="Number of Articles", rot=90, alpha=0.5)
    plt.savefig(outputFilename, bbox_inches="tight")


def getLeaningCounts(data, outputFolder):
    """
    Get and plot leaning counts of articles.
    """
    outputFilename = outputFolder + "leaningCounts.pdf"
    leaningCounts = data["leaning"].value_counts().to_frame(name="count").reset_index()
    leaningCounts.plot.bar(title="Number of Articles per Leaning", x="leaning", xlabel="Leaning", y="count", ylabel="Number of Articles", alpha=0.5)
    plt.savefig(outputFilename, bbox_inches="tight")


def main():
    cleanedDataFilename = "data/cleanedData.csv"
    outputFolder = "output/"
    data = getData(cleanedDataFilename)
    getDomainCounts(data, outputFolder)
    getLeaningCounts(data, outputFolder)


if __name__ == "__main__":
    main()
