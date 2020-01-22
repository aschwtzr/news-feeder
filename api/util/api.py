# interface with external APIs
import time
import requests
import os

# https://github.com/reddit-archive/reddit/wiki/API
# "reddit": 'https://www.reddit.com/r/worldnews/.rss?sort=new',
# needs Reddit integration
world_news_feeds = {
  "custom": 'https://news.google.com/rss/search?q=&hl=en-US&gl=US&ceid=US:en',
  "world": 'https://news.google.com/rss/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRGx1YlY4U0FtVnVHZ0pWVXlnQVAB?hl=en-US&gl=US&ceid=US:en',
  "reuters": 'http://feeds.reuters.com/Reuters/worldNews',
  "bbc": 'http://feeds.bbci.co.uk/news/world/rss.xml',
  "dw": 'http://rss.dw.com/rdf/rss-en-world',
  "guardian": 'https://www.theguardian.com/world/rss',
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
  result = requests.get(request_uri)
  return result.text

def list_rss_sources ():
  sources = []
  for source in world_news_feeds:
    sources.append(source)
  return list(map(lambda source: source, world_news_feeds))
