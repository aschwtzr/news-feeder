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
    # filter out youtube
    remaining_articles = []
    for article in topic['articles']:
      # print(article.title)
      # skip google news articles we can't parse
      if source.key == 'google-world':
        url = extract_url(article['url'])
        if url == 'error' or search('https://www.youtube.com', url):
          continue
      else:
        url = article['url']
      remaining_articles.append(article)
      articles_arr.append(article)
      if json_only is False:
        # works in theory
        exists = Article.select().where(Article.source==article['source'], Article.url==article['url'])
        if len(exists.execute()) > 0:
          continue
        topic, keywords, article = kw_art_top(article['raw_text'], article['url'], article['title'], article['source'], article['date'])
        article.save()
    topic['articles'] = remaining_articles
    # print(topic)
    # topic.woof()
    topics_arr.append(topic)
  return topics_arr, articles_arr, events

  ###
  # sample xml
  # <item>
  # <title>
  # Israeli settler leader: 'Kushner took a knife and put it in Netanyahu's back' | TheHill - The Hill
  # </title>
  # <link>
  # https://news.google.com/__i/rss/rd/articles/CBMieGh0dHBzOi8vdGhlaGlsbC5jb20vcG9saWN5L2ludGVybmF0aW9uYWwvbWlkZGxlLWVhc3Qtbm9ydGgtYWZyaWNhLzQ4MTQ0MS1pc3JhZWxpLXNldHRsZXItbGVhZGVyLWt1c2huZXItdG9vay1hLWtuaWZlLWFuZNIBfGh0dHBzOi8vdGhlaGlsbC5jb20vcG9saWN5L2ludGVybmF0aW9uYWwvbWlkZGxlLWVhc3Qtbm9ydGgtYWZyaWNhLzQ4MTQ0MS1pc3JhZWxpLXNldHRsZXItbGVhZGVyLWt1c2huZXItdG9vay1hLWtuaWZlLWFuZD9hbXA?oc=5
  # </link>
  # <guid isPermaLink="false">52780586591920</guid>
  # <pubDate>Tue, 04 Feb 2020 19:47:13 GMT</pubDate>
  # <description>
  # <ol><li><a href="https://news.google.com/__i/rss/rd/articles/CBMieGh0dHBzOi8vdGhlaGlsbC5jb20vcG9saWN5L2ludGVybmF0aW9uYWwvbWlkZGxlLWVhc3Qtbm9ydGgtYWZyaWNhLzQ4MTQ0MS1pc3JhZWxpLXNldHRsZXItbGVhZGVyLWt1c2huZXItdG9vay1hLWtuaWZlLWFuZNIBfGh0dHBzOi8vdGhlaGlsbC5jb20vcG9saWN5L2ludGVybmF0aW9uYWwvbWlkZGxlLWVhc3Qtbm9ydGgtYWZyaWNhLzQ4MTQ0MS1pc3JhZWxpLXNldHRsZXItbGVhZGVyLWt1c2huZXItdG9vay1hLWtuaWZlLWFuZD9hbXA?oc=5" target="_blank">Israeli settler leader: 'Kushner took a knife and put it in Netanyahu's back' | TheHill</a>&nbsp;&nbsp;<font color="#6f6f6f">The Hill</font></li>
  # <li><a href="https://news.google.com/__i/rss/rd/articles/CBMihwFodHRwczovL3d3dy5mb3huZXdzLmNvbS93b3JsZC9uZXRhbnlhaHUtYmFja3RyYWNrcy1mcm9tLXdlc3QtYmFuay1zZXR0bGVtZW50LWFubmV4YXRpb24tcGxhbnMtdGhpcy13ZWVrLXBlci13aGl0ZS1ob3VzZS1yZXF1ZXN0LXJlcG9ydHPSAYsBaHR0cHM6Ly93d3cuZm94bmV3cy5jb20vd29ybGQvbmV0YW55YWh1LWJhY2t0cmFja3MtZnJvbS13ZXN0LWJhbmstc2V0dGxlbWVudC1hbm5leGF0aW9uLXBsYW5zLXRoaXMtd2Vlay1wZXItd2hpdGUtaG91c2UtcmVxdWVzdC1yZXBvcnRzLmFtcA?oc=5" target="_blank">Israel's Netanyahu backtracks from immediate West Bank settlement annexation plan, will wait until after Ma...</a>&nbsp;&nbsp;<font color="#6f6f6f">Fox News</font></li>
  # <li><a href="https://news.google.com/__i/rss/rd/articles/CBMiswFodHRwczovL3d3dy53YXNoaW5ndG9ucG9zdC5jb20vd29ybGQvbWlkZGxlX2Vhc3QvcmVwb3J0cy1qYXJlZC1rdXNobmVyLWFuZ2Vycy1uZXRhbnlhaHUtY2FtcC1ieS1zbG93aW5nLWFubmV4YXRpb24tbW92ZXMvMjAyMC8wMi8wNC84MjM3NmFjNi00NzE5LTExZWEtOTFhYi1jZTQzOWFhNWM3YzFfc3RvcnkuaHRtbNIBAA?oc=5" target="_blank">Netanyahu sees Kushner as blocking settlement annexation: Israeli media - The</a>&nbsp;&nbsp;<font color="#6f6f6f">The Washington Post</font></li>
  # <li><a href="https://news.google.com/__i/rss/rd/articles/CBMiemh0dHBzOi8vd3d3LnJldXRlcnMuY29tL2FydGljbGUvdXMtaXNyYWVsLXN1ZGFuL3N1ZGFuLWNhc3RzLWRvdWJ0LW9uLWVhcmx5LW5vcm1hbGl6YXRpb24tb2YtdGllcy13aXRoLWlzcmFlbC1pZFVTS0JOMVpZMUhE0gE0aHR0cHM6Ly9tb2JpbGUucmV1dGVycy5jb20vYXJ0aWNsZS9hbXAvaWRVU0tCTjFaWTFIRA?oc=5" target="_blank">Sudan casts doubt on early normalization of ties with Israel</a>&nbsp;&nbsp;<font color="#6f6f6f">Reuters</font></li><li><a href="https://news.google.com/__i/rss/rd/articles/CBMiYWh0dHBzOi8vd3d3LmFsamF6ZWVyYS5jb20vbmV3cy8yMDIwLzAyL25ldGFueWFodS1pc3JhZWwtc3VkYW4tbm9ybWFsaXNlLXRpZXMtMjAwMjAzMTgyNTM2OTcyLmh0bWzSAWVodHRwczovL3d3dy5hbGphemVlcmEuY29tL2FtcC9uZXdzLzIwMjAvMDIvbmV0YW55YWh1LWlzcmFlbC1zdWRhbi1ub3JtYWxpc2UtdGllcy0yMDAyMDMxODI1MzY5NzIuaHRtbA?oc=5" target="_blank">Netanyahu says Israel and Sudan to normalise ties soon</a>&nbsp;&nbsp;<font color="#6f6f6f">Al Jazeera English</font></li>
  # <li><strong><a href="https://news.google.com/stories/CAAqOQgKIjNDQklTSURvSmMzUnZjbmt0TXpZd1NoTUtFUWl3emZXQWo0QU1FU0R0Q25iX1JJS2NLQUFQAQ?oc=5" target="_blank">View full coverage on Google News</a></strong></li></ol>
  # </description>
  # <source url="https://thehill.com">The Hill</source>
  # </item>
  # 
  # ###