# extract rss feed content and package it into topics and articles

from feeder.models.article import Article
from feeder.models.topic import Topic
from feeder.formatter.keyword_extractor import remove_known_junk, keywords_from_text_title, keywords_from_string, keywords_from_title_list, remove_publication_after_pipe
from feeder.util.time_tools import timestamp_string
from feeder.util.api import get_content_from_uri
from bs4 import BeautifulSoup
import re

def get_full_text(url):
  content = get_content_from_uri(url)
  if content['ok'] == True:
    soup = BeautifulSoup(content['data'], 'lxml')
    # soup = BeautifulSoup(content, 'html.parser')
    text = ' '.join(map(lambda p: p.get_text(), soup.find_all('p')))
    text = remove_known_junk(text, False)
    return {'ok': True, 'text': text}
  else:
    print('### NO TEXT')
    return {'ok': False, 'text': content}

def topics_from_google_item (item):
  item = item[0]
  item_soup = BeautifulSoup(item.description.get_text(), "html.parser")
  list_items = item_soup.findAll('li')

  timestamp = (item.pubDate.string if item.pubDate is not None else timestamp_string())
  if len(list_items) < 2:
    article = article_from_google_item(item_soup, timestamp)
    if len(article.raw_text) > 1:
      keywords = keywords_from_text_title(article.raw_text, article.title)
    else:
      keywords = keywords_from_string(article.title)
    if len(keywords) < 1:
      keywords = article.title.split(' ')
    return Topic([article], keywords)
  else:
    articles = []
    for item in list_items:
      if item.find('strong') is not None:
        # link to google news
        continue

      article = article_from_google_item(item, timestamp)
        
      articles.append(article)
    headlines = list(map(lambda article: article.title, articles))
    keywords = keywords_from_title_list(headlines)
    for article in articles:
      article_kw = set(article.keywords)
      topic_kw = set(keywords)
      article.keywords += list(topic_kw - article_kw)

    return Topic(articles, keywords)

def article_from_google_item (article, timestamp):
  a = article.find('a')
  title = a.get_text()
  clean_title = remove_publication_after_pipe(title)
  source = article.find('font').get_text()
  raw_text = get_full_text(a['href'])
  if raw_text['ok'] == True:
    raw_text = raw_text['text']
  else:
    raw_text = ''
  article = Article(source=source, url=a['href'], title=clean_title, raw_text=raw_text, date=timestamp)
  return article

def yahoo (content):
  soup = BeautifulSoup(content, "html.parser")
  return soup.get_text()

def guardian (article):
  article = article[0]
  url_title = common_fields(article)
  timestamp = timestamp_string() if article.pubDate is None else article.pubDate.string
  raw_text = get_full_text(url_title['url'])
  if raw_text['ok'] == True:
    raw_text = raw_text['text']
  else:
    raw_text = parse_guardian(article.description.get_text()) if article.description else article.title.string + '...'
  keywords = keywords_from_text_title(raw_text, url_title['title'])
  article = Article(source='The Guardian', url=url_title['url'], title=url_title['title'], raw_text=raw_text, date=timestamp, keywords=keywords)
  topic = Topic([article], keywords)

  return topic

def parse_guardian (content):
  soup = BeautifulSoup(content, "html.parser")
  content_p_tags = soup.find_all('p')
  text = ''
  for index, p in enumerate(content_p_tags):
    text += p.get_text()
    if index == 0:
      text += '. '

  return text

def dw (article):
  topic = default(article[0], 'Deutsche Welle')
  return topic

def az_central (article):
  topic = default(article[0], 'AZ Central')
  return topic

def default (article, source):
  url_title = common_fields(article)
  if article.pubDate is not None:
   timestamp = article.pubDate.string
  elif article.date is not None:
    timestamp = article.date.string
  else:
    timestamp = timestamp_string()
  raw_text = get_full_text(url_title['url'])
  if raw_text['ok'] == True:
    raw_text = raw_text['text']
  else:
    raw_text = article.description.get_text() if article.description else article.title.string + '...'
  photoless = re.sub('Photos: ', '', raw_text)
  head, sep, tail = photoless.partition('.<div')
  keywords = keywords_from_text_title(head, url_title['title'])
  article = Article(source=source, url=url_title['url'], title=url_title['title'], raw_text=head, date=timestamp, keywords=keywords)
  topic = Topic([article], keywords)

  return topic
  
def bbc (article):
  topic = default(article[0], 'BBC')
  return topic

def common_fields(article_soup):
  return {
    'url': article_soup.link.string,
    'title': article_soup.title.string
  }
