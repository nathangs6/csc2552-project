import xml.etree.ElementTree as ET
import requests
from bs4 import BeautifulSoup
import pandas as pd

###################
### Vox Scraper ###
###################
def get_urls():
    urls = []
    dates = []
    for m in range(1, 13):
        month = str(m)
        sitemap_url = f"https://www.vox.com/sitemaps/entries/2023/{month}"
        temp_urls, temp_dates = parse_sitemap(sitemap_url)
        urls.extend(temp_urls)
        dates.extend(temp_dates)
    return urls, dates

def parse_sitemap(sitemap_url):
    """Parse the sitemap from Vox and return a list of tuples containing article URLs and last modified dates."""
    response = requests.get(sitemap_url)
    sitemap_content = response.text
    root = ET.fromstring(sitemap_content)

    urls = []
    dates = []
    for url_tag in root.findall('{http://www.sitemaps.org/schemas/sitemap/0.9}url'):
        loc = url_tag.find('{http://www.sitemaps.org/schemas/sitemap/0.9}loc').text
        lastmod = url_tag.find('{http://www.sitemaps.org/schemas/sitemap/0.9}lastmod').text
        urls.append(loc)
        dates.append(lastmod)

    return urls, dates

def scrape(url):
    """Scrape a Vox article and return its title, summary, and content."""
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extracting the title from the first <h1> tag with class "c-page-title"
        title_tag = soup.find('h1', class_='c-page-title')
        title = title_tag.get_text().strip() if title_tag else 'No title found'

        # Extracting the summary from the first <p> tag with class "c-entry-summary"
        summary_tag = soup.find('p', class_='c-entry-summary')
        summary = summary_tag.get_text().strip() if summary_tag else 'No summary found'

        # Extracting the content from all <p> tags inside <div> tag with class "c-entry-content"
        content_tag = soup.find('div', class_='c-entry-content')
        content = ' '.join(p.get_text().strip() for p in content_tag.find_all('p')) if content_tag else 'No content found'

        content = summary + " " + content

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
    urls, dates = get_urls()
    N = len(urls)
    print(N)
    interval = N // 10
    for i in range(len(urls)):
        title, content = scrape(urls[i])
        if title is None or content is None:
            continue
        data["url"].append(urls[i])
        data["date"].append(dates[i])
        data["title"].append(title)
        data["content"].append(content)
        data["domain"].append("vox")
        if i % interval == 0:
            print(f"{round(100*i/N, 2)}% done!")
    print("All done!")
    df = pd.DataFrame(data)
    df.to_csv("output/vox.csv")

if __name__ == "__main__":
    main()
