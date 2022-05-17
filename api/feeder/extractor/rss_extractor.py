from re import search
from datetime import datetime
from feeder.models.article import Article
from playhouse.shortcuts import model_to_dict
import json
from bs4 import BeautifulSoup
from feeder.util.api import get_data_from_uri
from feeder.formatter.article_formatter import kw_art_top

def extract_url(google_url):
  print(f'fetching {google_url}')
  data = get_data_from_uri(google_url)
  if data['ok'] == True:
    soup = BeautifulSoup(data['data'], 'html.parser')
  else:
    print('error pulling feed ', data['error'])
    
  try:
    print('searching for content in soup')
    message = soup.find(property="og:url").attrs['content']
    return message
  except:
    # print(soup)
    # print(google_url)
    return 'error'

def extract_soup_items(raw_data):
  soup = BeautifulSoup(raw_data, 'xml')
  items = soup.findAll('item')
  return items

def fetch_articles_for_feed(source, json_only = False, limit = None):
  # TODO: return articles instead of topics
  # print(f"again {source.description}")
  if limit is not None:
    topics, articles, events = source.map_topic_stream(limit)
  else:
    topics, articles, events = source.map_topic_stream()
  topics_arr = []
  articles_arr = []
  # print(topics)
  for topic in topics:
    has_many = len(topic['articles']) > 1
    if has_many is True:
      articles_arr.extend(topic['articles'])
    for article in topic['articles']:
      if has_many is False:
        articles_arr.append(article)
      if json_only is False:
        # works in theory
        exists = Article.select().where(Article.source==article['source'], Article.url==article['url'])
        if len(exists.execute()) > 0:
          continue
        topic, keywords, article = kw_art_top(article['raw_text'], article['url'], article['title'], article['source'], article['date'], article['paragraphs'])
        article.save()
    topics_arr.append(topic)
  return topics_arr, articles_arr, events
