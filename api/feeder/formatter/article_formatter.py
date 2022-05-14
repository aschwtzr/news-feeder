# extract rss feed content and package it into topics and articles

from feeder.models.article import Article
from feeder.models.topic import Topic
from feeder.formatter.keyword_extractor import remove_known_junk, keywords_from_text_title, keywords_from_string, keywords_from_title_list, remove_publication_after_pipe
from feeder.util.time_tools import timestamp_string
from feeder.util.api import get_content_from_uri
from bs4 import BeautifulSoup
import re

# TODO: each method could return a pipeline event with: {method, input, output, events: [event, event]}
# These could pipeline_event objects that can either be saved to the DB, logged, printed or returned to the FE for debugging
def get_soup_paragraphs(soup):
  print('souping')
  # print(content)
  # soup = BeautifulSoup(content, 'html.parser')
  paragraphs = soup.find_all('p')
  print(paragraphs)
  return paragraphs

def get_soup(url):
  content = get_content_from_uri(url)
  if content['ok'] == True:
    print('content ok')
    soup = BeautifulSoup(content['data'], 'lxml')
    return {'ok': True, 'soup': soup}
  else:
    print('content not ok')
    print('### NO TEXT')
    return {'ok': False, 'content': content}

def get_full_text(url):
  soup = get_soup(url)
  # print(soup.prettify())
  if soup['ok'] == True:
    paragraphs = get_soup_paragraphs(soup['soup'])
    text = clean_soup_text(paragraphs)
    return {'ok': True, 'text': text}
  else:
    print('### NO TEXT')
    return {'ok': False, 'text': soup['content']}

def clean_soup_text(string_arrays):
  text = '\n\n'.join(map(lambda p: p.get_text(), string_arrays))
  print("### BEFORE")
  print(text)
  print("###")
  print("### REMOVE JUNK")
  text = remove_known_junk(text, False)
  print(text)
  print("###")
  return text

def filter_in_class(classes_array, filter_class):
  if classes_array is None:
    return True
  return not any(filter_class in s for s in classes_array)

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
  # filtered = list(filter(lambda p: filter_in_class(p.get('class'), "accesstobeta__text"), paragraphs))
  # filtered = list(filter(lambda p: filter_in_class(p.get('class'), "cookie__text"), paragraphs))
  content_p_tags = soup.find_all('p')
  text = ''
  for index, p in enumerate(content_p_tags):
    text += p.get_text()
    if index == 0:
      text += '. '

  return text

def dw (article):
  defaults = default(article[0], 'Deutsche Welle')
  if defaults['ok'] == True:
    paragraphs = defaults['paragraphs']
    filtered = list(filter(lambda p: filter_in_class(p.get('class'), "Deutsche Welle"), paragraphs))
    raw_text = clean_soup_text(filtered)
    topic = kw_art_top(raw_text, defaults['url'], defaults['title'], 'BBC', defaults['timestamp'])
    return topic
  else:
    return defaults
  return topic

def az_central (article):
  defaults = default(article[0], 'AZ Central')
  if defaults['ok'] == True:
    paragraphs = defaults['paragraphs']
    filtered = list(filter(lambda p: filter_in_class(p.get('class'), "PromoHeadline"), paragraphs))
    raw_text = clean_soup_text(filtered)
    topic = kw_art_top(raw_text, defaults['url'], defaults['title'], 'AZ Central', defaults['timestamp'])
    return topic
  else:
    return defaults
  return topic

def bbc (article):
  defaults = default(article[0], 'BBC')
  if defaults['ok'] == True:
    paragraphs = defaults['paragraphs']
    filtered = list(filter(lambda p: filter_in_class(p.get('class'), "PromoHeadline"), paragraphs))
    raw_text = clean_soup_text(filtered)
    topic = kw_art_top(raw_text, defaults['url'], defaults['title'], 'BBC', defaults['timestamp'])
    return topic
  else:
    return defaults

def kw_art_top (raw_text, url, title, source, timestamp):
  keywords = keywords_from_text_title(raw_text, title)
  article = Article(source=source, url=url, title=title, raw_text=raw_text, date=timestamp, keywords=keywords)
  return Topic([article], keywords)

def default (article, source):
  url_title_ts = common_fields(article)
  return url_title_ts
  # raw_text = raw_text_from_uri(url_title['url'])

def raw_text_from_uri(uri):
  raw_text = get_full_text(uri)
  # print(raw_text)
  if raw_text['ok'] == True:
    raw_text = raw_text['text']
  else:
    raw_text = article.description.get_text() if article.description else article.title.string + '...'
  photoless = re.sub('Photos: ', '', raw_text)
  # print(photoless)
  head, sep, tail = photoless.partition('.<div')
  # print(head)
  # print(sep)
  # print(tail)
  return head

def common_fields(article_soup):
  if article_soup.pubDate is not None:
   timestamp = article_soup.pubDate.string
  elif article_soup.date is not None:
    timestamp = article_soup.date.string
  else:
    timestamp = timestamp_string()
  url = article_soup.link.string
  soup = get_soup(url)
  if soup['ok'] == True:
    paragraphs = get_soup_paragraphs(soup['soup'])
    return {
      'ok': True,
      'url': url,
      'title': article_soup.title.string,
      'timestamp': timestamp,
      'paragraphs': paragraphs
    }
  else:
    print('### NO TEXT')
    return {'ok': False, 'text': soup['content']}
  # paragraphs = get_soup_paragraphs(soup)
