from api.feeder.formatter.feed_parser import google, reuters, yahoo, guardian, default
from api.feeder.util.api import get


class Source:
  def __init__(self, url, parser):
    self.url = url
    self.parser = parser
  
  def get_feed_xml(self):
    text = get(self.url)
    parsed = self.parser(text)
    # print(parsed)

def custom_google_source (query):
  return Source(f"https://news.google.com/rss/search?q={query}&hl=en-US&gl=US&ceid=US:en", google)

google = Source('https://news.google.com/rss/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRGx1YlY4U0FtVnVHZ0pWVXlnQVAB?hl=en-US&gl=US&ceid=US:en', google)
reuters = Source('http://feeds.reuters.com/Reuters/worldNews', reuters)
guardian = Source('https://www.theguardian.com/world/rss', guardian)
yahoo = Source('https://www.yahoo.com/news/rss/world', yahoo)
bbc = Source('http://feeds.bbci.co.uk/news/world/rss.xml', default)
dw = Source('http://rss.dw.com/rdf/rss-en-world', default)