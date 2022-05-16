from feeder.models.source import Source
from feeder.util.time_tools import print_timestamp
from feeder.extractor.rss_extractor import fetch_articles_for_feed

def get_feeds(feed_ids = None, json_only = False, limit = None):
  query = Source.select()
  if feed_ids is not None:
    query = query.where(Source.id.in_(feed_ids.split(',')))
  # for source in query:
  #   print(f"Fetching articles for {source.description}")
  print_timestamp("FETCHING NEWS")

  feed_data = []
  for source in query:
    print(f"fetching {source.description}")
    source_topics = fetch_articles_for_feed(source, json_only, limit)
    source_dict = {
      'description': source.description,
      'id': source.id,
      'topics':  source_topics
    }
    feed_data.append(source_dict)
  return feed_data