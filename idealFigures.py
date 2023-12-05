import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import cm
import numpy as np

outputFolder = "output/"
axesColour = 'darkslategrey'
lineColours = [(205/255, 92/255, 92/255), (80/255, 200/255, 120/255), (64/255, 224/255, 208/255)]
lineColours = cm.PuBu(np.linspace(0.4,1.0,3))
alpha = 0.9

def getIdealDocumentDistribution(filename):
    data = []
    for y in range(1970, 2023):
        for x in range(365):
            data.append([y, "left", "text"])
        for x in range(365):
            data.append([y, "right", "text"])
    data = pd.DataFrame(data, columns=["year", "leaning", "text"])
    data = data.groupby(["year", "leaning"]).size().unstack()
    print(data)
    ax = data.plot.area(xlabel="Year", ylabel="Number of Articles", title="Ideal Documents per Year", color=lineColours[1::-1], alpha=alpha)
    ax.spines[:].set_color(axesColour)
    ax.spines[['right', 'top']].set_visible(False)
    ax.tick_params(color=axesColour, labelcolor=axesColour)
    ax.xaxis.label.set_color(axesColour)
    ax.yaxis.label.set_color(axesColour)
    ax.title.set_color(axesColour)
    plt.legend(labelcolor=axesColour)
    plt.savefig(filename, bbox_inches="tight")


def main():
    filename = outputFolder + "idealDocDist.jpg"
    getIdealDocumentDistribution(filename)


if __name__ == "__main__":
    main()
