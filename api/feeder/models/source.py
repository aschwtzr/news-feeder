from feeder.formatter.article_formatter import dw, bbc, guardian,az_central, topics_from_google_item, filter_bbc, filter_dw, filter_az_central
from feeder.extractor.rss_extractor import extract_soup_items
from feeder.util.api import get_data_from_uri
from feeder.util.orm import BaseModel
from peewee import *
from playhouse.postgres_ext import *

class Source(BaseModel):
  class Meta:
    table_name = 'sources'

  feed_extractor_key=TextField()
  text_parser_key=TextField()
  description = TextField(column_name='name')
  key = TextField()
  category = TextField()
  default_limit = TextField()
  url = TextField()
  id = IntegerField()
  active = BooleanField()
  
  def get_raw_data(self):
    # fetches a source rss feed and return xml
    data = get_data_from_uri(self.url)
    if data['ok'] == False:
      print('error pulling feed ', data['error'])
      return []
    return data['data']

  def map_topic_stream(self, limit=20):
    # map over rss feed into articles clustered as topics (to accommodate google news)
    data = self.get_raw_data()
    soup_items = extract_soup_items(data)
    current = 0
    # TODO: return articles instead of topics
    topics = []
    articles = []
    top_events = []
    while current < limit:
      topic, articles, events = self.feed_parser(soup_items[current])
      if len(articles) < 1:
        top_events.append(events)
      else:  
        articles.extend(articles)
        topics.append(topic)
        current += 1
    return topics, articles, top_events
  
  def feed_parser(self, soup_item):
    article_formatter_hash = {
      'bbc-world': bbc,
      'dw-world': dw,
      'guardian-world': guardian,
      'azc-local': az_central,
      'google-news': topics_from_google_item
    }
    return article_formatter_hash[self.text_parser_key](soup_item)

  # TODO: move these class strings to the DB, can live on source
  def body_parser(self, soup_item):
    article_formatter_hash = {
      'bbc-world': filter_bbc,
      'dw-world': filter_dw,
      'guardian-world': guardian,
      'azc-local': filter_az_central,
      'google-news': topics_from_google_item
    }
    return article_formatter_hash[self.text_parser_key](soup_item)

# TODO: can create new Google source
# def custom_google_source (query, description):
  # return Source(f"https://news.google.com/rss/search?q={query}&hl=en-US&gl=US&ceid=US:en", feed_parser.google, description, f"custom-{query}", 10)
