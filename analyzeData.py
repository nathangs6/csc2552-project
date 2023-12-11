import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime
from matplotlib import cm
import numpy as np
from textblob import TextBlob

outputFolder = "output/"
axesColour = 'darkslategrey'
colourMap = cm.PuBu

def formatPlot(ax):
    ax.spines[:].set_color(axesColour)
    ax.spines[['right', 'top']].set_visible(False)
    ax.tick_params(color=axesColour, labelcolor=axesColour)
    ax.xaxis.label.set_color(axesColour)
    ax.yaxis.label.set_color(axesColour)
    ax.title.set_color(axesColour)

def getData(cleanedDataFilename: str):
    """
    Get the cleaned data for further analysis.
    """
    data = pd.read_csv(cleanedDataFilename)
    return data

def getDataDescription(data):
    print("Getting brief description of data")
    print("Number of articles:", data.shape[0])
    print("Number of domains:", len(data["domain"].unique()))
    leaning_counts = data["leaning"].value_counts()
    print("Number of documents per " + str(leaning_counts))
    print("Time range:", datetime.fromtimestamp(min(data["date"])), "to", datetime.fromtimestamp(max(data["date"])))

def getDomainCounts(data, outputFilename):
    """
    Get and plot domain counts of articles.
    """
    domainCounts = data[["domain", "leaning"]].value_counts().to_frame(name="count").reset_index()
    colours = colourMap(0.6)
    ax = domainCounts.plot.scatter(title="Number of Articles Per Domain", x="domain", xlabel="Domain", y="count", ylabel="Number of Articles", rot=90, color=colours, alpha=0.9)
    formatPlot(ax)
    plt.savefig(outputFilename, bbox_inches="tight")


def getLeaningCounts(data, outputFilename):
    """
    Get and plot leaning counts of articles.
    """
    leaningCounts = data["leaning"].value_counts().to_frame(name="count").reset_index()
    colours = colourMap(0.6)
    ax = leaningCounts.plot.bar(title="Number of Articles per Leaning", x="leaning", xlabel="Leaning", y="count", ylabel="Number of Articles", color=colours, alpha=0.9, legend=False)
    formatPlot(ax)
    plt.savefig(outputFilename, bbox_inches="tight")


def getTimeCounts(data, outputFilename):
    """
    Get and plot number of articles per year.
    """
    data["year"] = pd.to_datetime(data["date"], unit="s").dt.year
    yearCounts = data["year"].value_counts().to_frame(name="count").reset_index()
    print(yearCounts)
    colours = colourMap(0.6)
    ax = yearCounts.plot(kind="bar", title="Number of Articles per Year", x="year", xlabel="Year", ylabel="Number of Articles", color = colours, alpha=0.9, legend=False)
    formatPlot(ax)
    plt.savefig(outputFilename, bbox_inches="tight")

def main():
    cleanedDataFilename = "data/output/cleanedData.csv"
    fullData = getData(cleanedDataFilename)
    getDataDescription(fullData)
    filename = outputFolder + "domainCounts.jpg"
    getDomainCounts(fullData, filename)
    filename = outputFolder + "leaningCounts.jpg"
    getLeaningCounts(fullData, filename)
    filename = outputFolder + "yearCounts.jpg"
    getTimeCounts(fullData, filename)
    farDataFilename = "data/output/farData.csv"
    farData = getData(farDataFilename)
    getDataDescription(farData)
    filename = outputFolder + "farLeaningCounts.pdf"
    getLeaningCounts(farData, filename)


if __name__ == "__main__":
    main()
