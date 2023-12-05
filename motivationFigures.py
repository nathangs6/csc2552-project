import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import cm
import numpy as np

outputFolder = "output/"
axesColour = 'darkslategrey'
lineColours = [(205/255, 92/255, 92/255), (80/255, 200/255, 120/255), (64/255, 224/255, 208/255)]
lineColours = cm.PuBu(np.linspace(0.4,1.0,3))
alpha = 0.9

def unionParticipation():
    """
    Make figure for union participation.
    """
    data = pd.read_csv("data/input/union_participation.csv")
    data = data[data["Country"].isin(["OECD - Total", "Canada", "United States"])]
    dataPivot = data.pivot(index="Time", columns="Country", values="Value")
    print(lineColours[:3])
    ax = dataPivot.plot(kind="line", xlabel="Year", ylabel="% Union Participation", title="Union Participation vs. Year", color=lineColours[:3], alpha=alpha)
    ax.spines[:].set_color(axesColour)
    ax.spines[['right', 'top']].set_visible(False)
    ax.tick_params(color=axesColour, labelcolor=axesColour)
    ax.xaxis.label.set_color(axesColour)
    ax.yaxis.label.set_color(axesColour)
    ax.title.set_color(axesColour)
    plt.legend(labelcolor=axesColour)

    plt.savefig(outputFolder + "unionParticipation.jpg", bbox_inches="tight")


def payProductivity():
    """
    Make figure for pay and productivity.
    """
    chosenCEO = "Realized CEO compensation"
    eliminatedCEO = "Granted CEO compensation"
    data = pd.read_csv("data/input/payData.tsv", sep="\t")
    ceoData = pd.read_csv("data/input/ceoCompensation.tsv", sep="\t")
    data = pd.merge(data, ceoData, on="Year")
    data = data.drop(eliminatedCEO, axis=1)
    data["CEO Compensation"] = 100 * data[chosenCEO] / data.loc[data["Year"] == 1979][chosenCEO].values[0]
    data.set_index("Year")
    data[["Productivity", "Compensation", "CEO Compensation"]] = data[["Productivity", "Compensation", "CEO Compensation"]].astype(float)
    data = data[["Year", "Productivity", "Compensation", "CEO Compensation"]]
    ax = data.plot(kind="line", x="Year", xlabel="Year", ylabel="Index", color=lineColours[-3:], alpha=alpha, title="Indexed Growth")
    ax.spines[:].set_color(axesColour)
    ax.spines[['right', 'top']].set_visible(False)
    ax.tick_params(color=axesColour, labelcolor=axesColour)
    ax.xaxis.label.set_color(axesColour)
    ax.yaxis.label.set_color(axesColour)
    ax.title.set_color(axesColour)
    plt.legend(labelcolor=axesColour)
    plt.savefig(outputFolder + "payProductivity.jpg", bbox_inches="tight")


if __name__ == "__main__":
    unionParticipation()
    payProductivity()
