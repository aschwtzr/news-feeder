from api.feeder.formatter import feed_parser, article_formatter
from api.feeder.util.api import get
# from api.feeder.formatter import 
# from api.feeder.formatter.article_formatter import default


class Source:
  def __init__(self, url, rss_algorithm, description_parser = None):
    self.url = url
    self.rss_algorithm = rss_algorithm
    self.description_parser = description_parser
  
  def get_feed_articles(self, limit = 99):
    # fetches a source rss feed and returns it as article objects
    data = get(self.url)
    if self.description_parser is not None:
      topic_stream = self.rss_algorithm(data, self.description_parser, limit)
    else:
      topic_stream = self.rss_algorithm(data, limit)

    return topic_stream


def custom_google_source (query):
  return Source(f"https://news.google.com/rss/search?q={query}&hl=en-US&gl=US&ceid=US:en", feed_parser.google)

google = Source('https://news.google.com/rss/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRGx1YlY4U0FtVnVHZ0pWVXlnQVAB?hl=en-US&gl=US&ceid=US:en', feed_parser.google)
reuters = Source('http://feeds.reuters.com/Reuters/worldNews', feed_parser.rss, article_formatter.reuters)
bbc = Source('http://feeds.bbci.co.uk/news/world/rss.xml', feed_parser.rss, article_formatter.default)
guardian = Source('https://www.theguardian.com/world/rss', feed_parser.rss, article_formatter.topics_from_guardian_item)
# yahoo = Source('https://www.yahoo.com/news/rss/world', article_formatter.yahoo, feed_parser.rss)
dw = Source('http://rss.dw.com/rdf/rss-en-world', feed_parser.rss, article_formatter.default)