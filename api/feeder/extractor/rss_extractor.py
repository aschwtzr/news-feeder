import feeder.util.db as db
from feeder.models.source import Source, article_formatter_hash, feed_parser_hash
from bs4 import BeautifulSoup
from re import search
from feeder.util.api import get_data_from_uri, get_summary, get_content_from_uri
from datetime import datetime


def load_source_feeds ():
  sources = db.fetch_sources({})
  sources = list(map(lambda row: source_from_row(row), sources))
  source_dict = {}
  for source in sources:
    source_dict[source.key] = source.get_feed_articles(source.limit)
  return source_dict

def source_from_row(row):
  print(row)
  if row['text_parser_key'] in article_formatter_hash:
    formatter = article_formatter_hash[row['text_parser_key']]
  else:
    formatter = None
  return Source(row['url'], feed_parser_hash[row['feed_extractor_key']], row['name'], row['key'], row['default_limit'], row['id'], formatter)

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

def get_full_text(url):
  content = get_content_from_uri(url)
  if content['ok'] == True:
    soup = BeautifulSoup(content['data'], 'lxml')
    # soup = BeautifulSoup(content, 'html.parser')
    text = ' '.join(map(lambda p: p.text, soup.find_all('p')))
    return {'ok': True, 'text': text}
  else:
    return content

def fetch_rss_feeds(sources):
  now = datetime.now()
  timestamp = now.strftime('%m/%d/%Y, %H:%M:%S')
  
  print(f"""
  *****************************************  
  *****************************************  
    FETCHING NEWS AT {timestamp}
  *****************************************  
  *****************************************  
  """)
  for (description, topics) in sources.items():
    for index, topic in enumerate(topics):
      for article in topic.articles:
        # skip google news articles we can't parse
        if description == 'google-world':
          url = extract_url(article.url)
          if url == 'error' or search('https://www.youtube.com', url):
            continue
        else:
          url = article.url

        if db.article_exists(article.source, url):
          continue
        
        # get paid smmry and build sql
        # print(url)
        # smr = get_free_summary(url)
        # smr = get_summary(url)
        db.insert_article(description, article.keywords, article.title, url, article.source, article.date, article.brief)

def get_feeds():
  sources = load_source_feeds()
  fetch_rss_feeds(sources)

