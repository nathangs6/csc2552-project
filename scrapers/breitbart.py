import xml.etree.ElementTree as ET
import requests
from bs4 import BeautifulSoup
import pandas as pd


def get_urls(m):
    urls = []
    dates = []
    for d in range(1, 32):
        month = "0" + str(m)
        day = "0" + str(d)
        sitemap_url = f"https://www.breitbart.com/sitemap_news-2023-{month[-2:]}-{day[-2:]}.xml"
        temp_urls, temp_dates = parse_sitemap(sitemap_url)
        urls.extend(temp_urls)
        dates.extend(temp_dates)
    return urls, dates

def parse_sitemap(sitemap_url):
    """Parse the sitemap and return a list of article URLs for a specific year."""
    response = requests.get(sitemap_url)
    sitemap_content = response.text
    root = ET.fromstring(sitemap_content)

    urls = []
    dates = []
    for url_tag in root.findall('{http://www.sitemaps.org/schemas/sitemap/0.9}url'):
        loc = url_tag.find('{http://www.sitemaps.org/schemas/sitemap/0.9}loc').text
        publication_date = url_tag.find('{http://www.google.com/schemas/sitemap-news/0.9}news').find('{http://www.google.com/schemas/sitemap-news/0.9}publication_date').text

        if "/sports/" in loc or "/clips/" in loc or "/europe/" in loc or "/asia/" in loc or "/middle-east/" in loc:
            continue

        if '2023' in publication_date:
            urls.append(loc)
            dates.append(publication_date)

    return urls, dates


def scrape(url):
    """Scrape a single article from Washington Examiner and return its title and content."""
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extracting title: first <h1> tag in <section> with id "MainW"
        title_tag = soup.find('section', id='MainW').find('h1')
        title = title_tag.get_text().strip() if title_tag else 'No title found'

        # Extracting content: in <p> tags inside first <div> with class "entry-content" in <section> with id "MainW"
        content_tag = soup.find('section', id='MainW').find('div', class_='entry-content')
        content = ' '.join(p.get_text().strip() for p in content_tag.find_all('p')) if content_tag else 'No content found'

        return title, content

    except Exception as e:
        print(f"Error scraping {url}: {str(e)}")
        return None, None


def main():
    for m in range(11, 13):
        df = {
            "url": [],
            "date": [],
            "title": [],
            "content": [],
            "domain": []
        }
        urls, dates = get_urls(m)
        N = len(urls)
        print("Month: " + str(m) + " - " + str(N) + " articles")
        interval = N // 10
        for i in range(len(urls)):
            title, content = scrape(urls[i])
            if title is None or content is None:
                continue
            df["url"].append(urls[i])
            df["date"].append(dates[i])
            df["title"].append(title)
            df["content"].append(content)
            df["domain"].append("breitbart")
            if i % interval == 0:
                print(f"{round(100*i/N, 2)}% done!")
        print("All done!")
        df = pd.DataFrame(df)
        df.to_csv(f"output/breitbart{str(m)}.csv")
        del df

if __name__ == "__main__":
    main()
