from bs4 import BeautifulSoup
import PyRSS2Gen
import datetime
import requests

url = 'https://www.afl.com.au/news/all-news'  # Replace with the target website's URL
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# This is an example and will vary depending on the website's HTML structure
articles = soup.find_all('article')  # Or the appropriate HTML tag

def get_article_content(article_url):
    response = requests.get(article_url)
    article_soup = BeautifulSoup(response.text, 'html.parser')

    # Assuming the article content is within <div class="article-content">
    content_div = article_soup.find('div', class_='article')

    if content_div:
        return content_div.get_text(strip=True)  # Extracts text from the div
    else:
        return 'No content available'


rss_items = []
for article in articles:
    title = article.find('h2').text
    link = article.find('a')['href']
    publication_date = datetime.datetime.now()  # Replace with actual date, if available

    # Fetch the full content
    full_content = get_article_content("https://www.afl.com.au/" + link)

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