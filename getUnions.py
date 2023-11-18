import re
import pandas as pd
from bs4 import BeautifulSoup

USUnionsFilename    = "data/input/us_unions.html"
CAUnionsFilename    = "data/input/ca_unions.html"
outputFilename      = "data/output/unions.txt"

def getUSUnions():
    with open(USUnionsFilename) as html:
        parsed_html = BeautifulSoup(html, features="html.parser")
    # find union text
    header_span = parsed_html.body.find(attrs={'id':'AFL-CIO'})
    list_tag = header_span.parent.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling
    us_unions = []
    for list_item in list_tag.find_all('li'):
        for union_raw in list_item.contents[:2]:
            us_unions.append(union_raw.text.strip().lower().replace("(", "").replace(")", ""))
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
    with open(outputFilename, 'w') as outputFile:
        outputFile.write("\n".join(unions))

if __name__ == "__main__":
    main()
