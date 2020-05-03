from feeder.formatter import feed_getter, article_formatter
from feeder.util.api import get_data_from_uri

class Source:
  def __init__(self, url, rss_algorithm, description, description_parser = None):
    self.url = url
    self.rss_algorithm = rss_algorithm
    self.description_parser = description_parser
    self.description = description
    # self.
    # save feed articles here to access them later
  
  def get_feed_articles(self, limit = 99):
    # fetches a source rss feed and returns it as article objects
    data = get_data_from_uri(self.url)
    if self.description_parser is not None:
      topic_stream = self.rss_algorithm(data, self.description_parser, limit)
    else:
      # print(data)
      # print(limit)
      topic_stream = self.rss_algorithm(data, limit)

    return topic_stream


def custom_google_source (query):
  return Source(f"https://news.google.com/rss/search?q={query}&hl=en-US&gl=US&ceid=US:en", f'Google News for {query}', feed_getter.google)

google = Source('https://news.google.com/rss/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRGx1YlY4U0FtVnVHZ0pWVXlnQVAB?hl=en-US&gl=US&ceid=US:en', feed_getter.google, 'Google - World News')
reuters = Source('http://feeds.reuters.com/Reuters/worldNews', feed_getter.rss, 'Reuters - World News', article_formatter.reuters)
bbc = Source('http://feeds.bbci.co.uk/news/world/rss.xml', feed_getter.rss, 'BBC - World News', article_formatter.bbc)
guardian = Source('https://www.theguardian.com/world/rss', feed_getter.rss, 'The Guardian - World News', article_formatter.topics_from_guardian_item)
# yahoo = Source('https://www.yahoo.com/news/rss/world', article_formatter.yahoo, feed_getter.rss)
dw = Source('http://rss.dw.com/rdf/rss-en-world', feed_getter.rss, 'Deutsche Welle - World News', article_formatter.dw)