from bs4 import BeautifulSoup
import PyRSS2Gen
import datetime
import requests

url = 'https://www.afl.com.au/news/all-news'  # Replace with the target website's URL
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# This is an example and will vary depending on the website's HTML structure
articles = soup.find_all('article')  # Or the appropriate HTML tag

rss_items = []
for article in articles:
    title = article.find('h2').text
    link = article.find('a')['href']
    publication_date = datetime.datetime.now()  # Replace with actual date, if available

    rss_item = PyRSS2Gen.RSSItem(
        title=title,
        link=link,
        description=title,  # You can add a more detailed description
        pubDate=publication_date
    )
    rss_items.append(rss_item)

rss = PyRSS2Gen.RSS2(
    title="AFL.com.au",  # Title of the feed
    link=url,
    description="AFL Website",
    lastBuildDate=datetime.datetime.now(),
    items=rss_items
)

# Save the RSS feed to a file
with open("feed.xml", "w") as f:
    rss.write_xml(f)