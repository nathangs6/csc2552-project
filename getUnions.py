import re
import pandas as pd
from bs4 import BeautifulSoup

USUnionsFilename    = "data/input/us_unions.html"
CAUnionsFilename    = "data/input/ca_unions.html"
outputFilename      = "data/output/unions.txt"

def getUSUnions():
    with open(USUnionsFilename) as html:
        parsed_html = BeautifulSoup(html, features="html.parser")
    unions_raw = parsed_html.body.find_all('div', attrs={'class': 'views-field-field-affiliate-name'})
    us_unions = []
    for union_raw in unions_raw:
        union = union_raw.find_all('a')
        if union == []:
            union = union_raw.find_all('div', attrs={'class': 'field-content'})
        union = union[0].text.strip().lower().split(" (")
        us_unions.append(union[0])
        if len(union) > 1:
            us_unions.append(union[1][:-1])
    return us_unions

def getCAUnions():
    with open(CAUnionsFilename) as html:
        parsed_html = BeautifulSoup(html, features="html.parser")
    unions_raw = parsed_html.body.find_all('div', attrs={'class':'affiliate__name mt-3'})
    ca_unions = []
    for union_raw in unions_raw:
        union = union_raw.text.strip().lower().split(" (")
        ca_unions.append(union[0])
        if len(union) > 1:
            ca_unions.append(union[1][:-1])
    return ca_unions

def main():
    unions = getUSUnions()
    ca_unions = getCAUnions()
    unions.extend(ca_unions)
    # Add weird abbreviations
    unions.extend(["rwdsu", "nffe", "tcu", "afa", "iue", "nabet", "ppmw", "tng", "gmp"])
    # Add some alternate names
    unions.extend(["united food and commercial workers"])
    # Add some extra teachers unions
    unions.extend(["new york state united teachers", "nysut",
                   "new york city teachers", "uft",
                   "illinois federation of teachers", "ift",
                   "california federation of teachers", "cft",
                   "chicago teachers union", "ctu"])
    # Add the over arching organizer
    unions.append("afl-cio")
    unions = list(set(unions))
    cleanedUnions = []
    for union in unions:
        cleanedUnions.append(re.sub("[^a-zA-Z0-9 ]", "", union))
    with open(outputFilename, 'w') as outputFile:
        outputFile.write("\n".join(cleanedUnions))

if __name__ == "__main__":
    main()
