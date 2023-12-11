import xml.etree.ElementTree as ET
import requests
from bs4 import BeautifulSoup
import pandas as pd

def get_urls_dn():
    sitemap_url = 'https://www.democracynow.org/sitemap_story.xml'
    return parse_sitemap_dn(sitemap_url)


def parse_sitemap_dn(sitemap_url):
    """
    Parse the sitemap and return a list of article URLs for 2023.
    """
    response = requests.get(sitemap_url)
    sitemap_content = response.text
    root = ET.fromstring(sitemap_content)
    urls = []
    dates = []
    for url_tag in root.findall('{http://www.sitemaps.org/schemas/sitemap/0.9}url'):
        loc = url_tag.find('{http://www.sitemaps.org/schemas/sitemap/0.9}loc').text
        lastmod = url_tag.find('{http://www.sitemaps.org/schemas/sitemap/0.9}lastmod').text

        if '2023' in loc and '2023' in lastmod:
            urls.append(loc)
            dates.append(lastmod)

    return urls, dates


def scrape_dn(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extracting title
        title_tag = soup.find('div', id='story_content').find('h1')
        title = title_tag.get_text().strip() if title_tag else 'No title found'

        # Extracting story summary
        summary_tag = soup.find('div', id='story_text').find('div', class_='story_summary').find('p')
        story_summary = summary_tag.get_text().strip() if summary_tag else 'No summary found'

        # Extracting transcript
        transcript_tag = soup.find('div', id='transcript')
        transcript = ' '.join(p.get_text().strip() for p in transcript_tag.find_all('p')) if transcript_tag else 'No transcript found'

        content = story_summary + " " + transcript

        return title, content

    except Exception as e:
        return None, None

def main():
    data = {
        "url": [],
        "date": [],
        "title": [],
        "content": [],
        "domain": []
    }
    urls, dates = get_urls_dn()
    N = len(urls)
    print(N)
    interval = N // 10
    for i in range(len(urls)):
        title, content = scrape_dn(urls[i])
        if title is None or content is None:
            continue
        data["url"].append(urls[i])
        data["date"].append(dates[i])
        data["title"].append(title)
        data["content"].append(content)
        data["domain"].append("democracynow")
        if i % interval == 0:
            print(f"{round(100*i/N, 2)}% done!")
    print("All done!")
    df = pd.DataFrame(data)
    df.to_csv("output/democracynow.csv")



if __name__ == "__main__":
    main()
