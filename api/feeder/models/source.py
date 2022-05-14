from feeder.formatter import article_formatter
from feeder.extractor import feed_parser
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
    topic_stream = feed_parser.parse_feed_data(self.key, data, limit, self.description_parser)

    return topic_stream
  
  def description_parser(self, *args):
    article_formatter_hash = {
      'bbc-world': article_formatter.bbc,
      'dw-world': article_formatter.dw,
      'guardian-world': article_formatter.guardian,
      'azc-local': article_formatter.az_central,
      'google-news': article_formatter.topics_from_google_item
    }
    return article_formatter_hash[self.text_parser_key](args)

def custom_google_source (query, description):
  return Source(f"https://news.google.com/rss/search?q={query}&hl=en-US&gl=US&ceid=US:en", feed_parser.google, description, f"custom-{query}", 10)
