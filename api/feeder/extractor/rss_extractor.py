from feeder.models.source import Source
import feeder.util.db as db
from re import search
from datetime import datetime
from feeder.models.article import Article
from feeder.extractor.feed_parser import extract_url
from playhouse.shortcuts import model_to_dict
import json

def fetch_new_articles(sources, json_only = False):
  now = datetime.now()
  timestamp = now.strftime('%m/%d/%Y, %H:%M:%S')
  feed_data = []
  
  print(f"""
  *****************************************  
  *****************************************  
    FETCHING NEWS AT {timestamp}
  *****************************************  
  *****************************************  
  """)
  for source in sources:
    print(f"fetching {source.description}")
    source_topics = fetch_articles_for_feed(source)
    feed_data.append(source_topics)
  return feed_data

def fetch_articles_for_feed(source, json_only = False):
  # print(f"again {source.description}")
  topics = source.map_topic_stream(2)
  topics_arr = []
  # print(topics)
  for topic in topics:
    remaining_articles = []
    for article in topic.articles:
      # print(article.title)
      # skip google news articles we can't parse
      if source.key == 'google-world':
        url = extract_url(article.url)
        if url == 'error' or search('https://www.youtube.com', url):
          continue
      else:
        url = article.url
      remaining_articles.append(article)
      exists = Article.select().where(Article.source==article.source, Article.url==article.url)
      if len(exists.execute()) > 0:
        continue
      # works in theory
      if json_only is False:
        article.save()
    topic.articles = remaining_articles
    # print(topic)
    # topic.woof()
    topics_arr.append(topic.to_dict())
  return topics_arr


# TODO: should be able to merge this with the fetch_new_articles
def get_feeds(feed_ids = None, json_only = False):
  # print(feed_ids)
  query = Source.select()
  if feed_ids is not None:
    query = query.where(Source.id.in_(feed_ids.split(',')))
  # for source in query:
  #   print(f"Fetching articles for {source.description}")
  feeds = fetch_new_articles(query, json_only)
  return feeds

