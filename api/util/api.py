# interface with external APIs
import time
import requests
import os

world_news_feeds = {
  "google": 'https://news.google.com/rss/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRGx1YlY4U0FtVnVHZ0pWVXlnQVAB?hl=en-US&gl=US&ceid=US:en',
  "reuters": 'http://feeds.reuters.com/Reuters/worldNews',
  "bbc": 'http://feeds.bbci.co.uk/news/world/rss.xml',
  "dw": 'http://rss.dw.com/rdf/rss-en-world',
  "guardian": 'https://www.theguardian.com/world/rss',
  "reddit": 'https://www.reddit.com/.rss',
  "custom": 'https://news.google.com/rss/search?q=&hl=en-US&gl=US&ceid=US:en',
  "yahoo": "https://www.yahoo.com/news/rss/world",
}

# if source is not in feeds object, fetches resutls with google search (world_news_feeds["custom"])
def get_feed_for (resource):
  if resource in world_news_feeds:
    uri = world_news_feeds[resource]
  else:
    split_uri = world_news_feeds["custom"].split('q=')
    uri = split_uri[0] + "q=" + resource + split_uri[1]

  results = requests.get(uri)
  return results.text

def get_article (uri):
  results = requests.get(uri)
  return results.text

def get_summary (uri):
  key = os.environ.get('SUMMRY_KEY')
  request_uri = f"https://api.smmry.com?SM_API_KEY={key}&SM_LENGTH=5&SM_URL={uri}"
  print(request_uri)
  result = requests.get(request_uri)
  return result.text

def get_rss_sources ():
  sources = []
  for source in world_news_feeds:
    sources.append(source)
  return sources