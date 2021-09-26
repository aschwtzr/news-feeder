from feeder.formatter import article_formatter
from feeder.extractor import feed_parser
from feeder.util.api import get_data_from_uri

class Source:
  def __init__(self, url, feed_algorithm, description, key, limit, id=None, description_parser = None):
    self.url = url
    self.feed_algorithm = feed_algorithm
    self.description = description
    self.key = key
    self.limit = limit
    self.description_parser = description_parser
    # self.
    # save feed articles here to access them later
  
  def get_feed_articles(self, limit = 99):
    # fetches a source rss feed and returns it as article objects
    data = get_data_from_uri(self.url)
    if data['ok'] == False:
      print('error pulling feed ', data['error'])
      return []
    elif self.description_parser is not None:
      topic_stream = self.feed_algorithm(data['data'], self.description_parser, limit)
    else:
      topic_stream = self.feed_algorithm(data['data'], limit)

    return topic_stream


def custom_google_source (query, description):
  return Source(f"https://news.google.com/rss/search?q={query}&hl=en-US&gl=US&ceid=US:en", feed_parser.google, description, f"custom-{query}", 10)

# reuters = Source('http://feeds.reuters.com/Reuters/worldNews', feed_getter.rss, 'Reuters - World News', 'reuters-world', article_formatter.reuters)
# yahoo = Source('https://www.yahoo.com/news/rss/world', article_formatter.yahoo, feed_getter.rss)

google = Source('https://news.google.com/rss/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRGx1YlY4U0FtVnVHZ0pWVXlnQVAB?hl=en-US&gl=US&ceid=US:en', feed_parser.google, 'Google - World News', 'google-world', 15)
bbc = Source('http://feeds.bbci.co.uk/news/world/rss.xml', feed_parser.rss, 'BBC - World News', 'bbc-world', 10, article_formatter.bbc)
guardian = Source('https://www.theguardian.com/world/rss', feed_parser.rss, 'The Guardian - World News', 'guardian-world', 10, article_formatter.guardian)
dw = Source('http://rss.dw.com/rdf/rss-en-world', feed_parser.rss, 'Deutsche Welle - World News', 'dw-world', 15, article_formatter.dw)
az_central = Source('http://rssfeeds.azcentral.com/phoenix/local', feed_parser.rss, 'AZ Central - Local', 'azc-local', 10, article_formatter.az_central)

active_topics = [bbc, guardian, dw, google, az_central]
topics_by_key = dict((source.key, source) for source in active_topics)

feed_parser_hash = {
  'rss': feed_parser.rss,
  'google': feed_parser.google
}

article_formatter_hash = {
  'bbc-world': article_formatter.bbc,
  'dw-world': article_formatter.dw,
  'guardian-world': article_formatter.guardian
}