from feeder.models.source import Source, feed_parser_hash, article_formatter_hash
import feeder.util.db as db
from bs4 import BeautifulSoup
from re import search
from feeder.util.api import get_data_from_uri
from datetime import datetime
from feeder.models.article import Article

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

def fetch_new_articles(sources):
  now = datetime.now()
  timestamp = now.strftime('%m/%d/%Y, %H:%M:%S')
  
  print(f"""
  *****************************************  
  *****************************************  
    FETCHING NEWS AT {timestamp}
  *****************************************  
  *****************************************  
  """)
  for source in sources:
    topics = source.map_topic_stream(20)
    for topic in topics:
      for article in topic.articles:
        # skip google news articles we can't parse
        if source.key == 'google-world':
          url = extract_url(article.url)
          if url == 'error' or search('https://www.youtube.com', url):
            continue
        else:
          url = article.url
        exists = Article.select().where(Article.source==article.source, Article.url==article.url)
        if len(exists.execute()) > 0:
          continue
        # works in theory
        article.save()

def get_feeds():
  sources = Source.select()
  fetch_new_articles(sources)

