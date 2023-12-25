from bs4 import BeautifulSoup
import PyRSS2Gen
import datetime
import requests

url = 'https://www.afl.com.au/news/all-news'  # Replace with the target website's URL
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

base_url = 'https://www.afl.com.au'
articles = soup.find_all('article')  # Or the appropriate HTML tag

rss_items = []
for article in articles:
    title = article.find('h2').text  # Find the title
    relative_link = article.find('a')['href']  # Extract the relative link

    # Skip the article if the link contains '/aflw/'
    if '/aflw/' in relative_link:
        continue  # Skips the rest of the loop and proceeds to the next article
    
    # Check if the link is already absolute or not
    if not relative_link.startswith('http'):
        link = base_url + relative_link  # Concatenate to form the full URL
    else:
        link = relative_link  # Use the link as it is

    description = article.find('p').text  # Extract description
    publication_date = datetime.datetime.now()  # Publication date

    rss_item = PyRSS2Gen.RSSItem(
        title=title,
        link=link,
        description=description,
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