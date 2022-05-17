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
  paragraphs = soup.find_all('p')
  return paragraphs

def get_soup(url):
  content = get_content_from_uri(url)
  if content['ok'] == True:
    soup = BeautifulSoup(content['data'], 'lxml')
    return {'ok': True, 'soup': soup}
  else:
    print('### NO TEXT')
    return {'ok': False, 'content': content}

def get_full_text(url):
  soup = get_soup(url)
  # print(soup.prettify())
  if soup['ok'] == True:
    paragraphs = get_soup_paragraphs(soup['soup'])
    text = clean_soup_text(paragraphs)
    return {'ok': True, 'text': text, 'paragraphs': paragraphs}
  else:
    print('### NO TEXT')
    return {'ok': False, 'text': soup['content']}

def clean_soup_text(string_arrays):
  mapped = list(map(lambda p: remove_known_junk(p.get_text(), False), string_arrays))
  text = '\n\n'.join(mapped)
  return text, mapped

def filter_in_class(classes_array, filter_class):
  if classes_array is None:
    return True
  return not any(filter_class in s for s in classes_array)

def topics_from_google_item (item):
  events = []
  item_soup = BeautifulSoup(item.description.get_text(), "html.parser")
  list_items = item_soup.findAll('li')
  timestamp = (item.pubDate.string if item.pubDate is not None else timestamp_string())
  # if item.find('strong') is not None == item is a link to google new
  filtered = [i for i in list_items if any(item.find('strong') for item in i.contents)]
  articles = list(map(lambda a: article_from_google_item(a, timestamp), filtered))
  headlines = list(map(lambda article: article['title'], articles))
  keywords = keywords_from_title_list(headlines)
  for article in articles:
    article_kw = set(article['keywords'])
    topic_kw = set(keywords)
    article['keywords'] += list(topic_kw - article_kw)
  topic = {'articles': articles, 'keywords': []}
  return topic, articles, events

def article_from_google_item (article, timestamp):
  events = []
  a = article.find('a')
  title = a.get_text()
  clean_title = remove_publication_after_pipe(title)
  events.append({'input': title, 'output': clean_title, 'operation': 'remove_publication_after_pipe'})
  source = article.find('font').get_text()
  res = get_full_text(a['href'])
  if res['ok'] == True:
    raw_text = res['text']
  else:
    raw_text = ''
  return article_from_soup_paragraphs(res['paragraphs'], clean_title, a['href'], timestamp, events, source)

def yahoo (content):
  soup = BeautifulSoup(content, "html.parser")
  return soup.get_text()

def guardian (article):
  events = []
  defaults = common_fields(article)
  # timestamp = timestamp_string() if article.pubDate is None else article.pubDate.string
  if defaults['ok'] == True:
    paragraphs = defaults['paragraphs']
    filtered = filter_none(paragraphs)
    return kw_art_top_json(filtered, defaults['title'], defaults['url'], defaults['timestamp'], events, 'The Guardian')
  else:
    events.append({'input': defaults['text'], 'output': 'Failed to Extract defaults.', 'operation': 'common_fields'})
    return None, [], events

def dw (article):
  events = []
  defaults = common_fields(article)
  if defaults['ok'] == True:
    paragraphs = defaults['paragraphs']
    filtered = filter_dw(paragraphs)
    return kw_art_top_json(filtered, defaults['title'], defaults['url'], defaults['timestamp'], events, 'Deutsche World')
  else:
    events.append({'input': defaults['text'], 'output': 'Failed to Extract defaults.', 'operation': 'common_fields'})
    return None, [], events

def filter_dw(paragraphs):
  filtered = list(filter(lambda p: filter_in_class(p.get('class'), "accesstobeta__text"), paragraphs))
  filtered = list(filter(lambda p: filter_in_class(p.get('class'), "cookie__text"), filtered))
  return list(filter(lambda p: filter_in_class(p.get('id'), "copyright"), filtered))

def az_central (article):
  events = []
  defaults = common_fields(article)
  if defaults['ok'] == True:
    paragraphs = defaults['paragraphs']
    filtered = filter_none(paragraphs)
    return kw_art_top_json(filtered, defaults['title'], defaults['url'], defaults['timestamp'], events, 'AZ Central')
  else:
    events.append({'input': defaults['text'], 'output': 'Failed to Extract defaults.', 'operation': 'common_fields'})
    return None, [], events

def filter_none(paragraphs):
  return paragraphs

def bbc(article):
  events = []
  defaults = common_fields(article)
  if defaults['ok'] == True:
    paragraphs = defaults['paragraphs']
    filtered = filter_bbc(paragraphs)
    # events.append({'input': paragraphs, 'output': filtered, 'operation': 'article_formatter.bbc'})
    return kw_art_top_json(filtered, defaults['title'], defaults['url'], defaults['timestamp'], events, 'BBC')
  else:
    events.append({'input': defaults['text'], 'output': 'Failed to Extract defaults.', 'operation': 'common_fields'})
    return None, [], events

def kw_art_top_json(soup, title, url, timestamp, events, source):
    article = article_from_soup_paragraphs(soup, title, url, timestamp, events, source)
    topic = {'articles': [article], 'keywords': []}
    return topic, [article], events

def filter_bbc(paragraphs):
  filtered = list(filter(lambda p: filter_in_class(p.get('class'), "Contributor"), paragraphs))
  return list(filter(lambda p: filter_in_class(p.get('class'), "PromoHeadline"), filtered))

def article_from_soup_paragraphs(soup_ps, title, url, timestamp, events, source):
  raw_text, raw_paras = clean_soup_text(soup_ps)
  # events.append({'input': filtered, 'output': raw_text, 'operation': 'clean_soup_text'})
  keywords = keywords_from_text_title(raw_text, title)
  events.append({'input': f"{raw_text} -- {title}", 'output': keywords, 'operation': 'keywords_from_text_title'})
  return {
    'source': source, 
    'url': url, 
    'title': title, 
    'raw_text': raw_text, 
    'date': timestamp, 
    'keywords': keywords, 
    'paragraphs': raw_paras,
    'events': events
  }

def kw_art_top (raw_text, url, title, source, timestamp):
  keywords = keywords_from_text_title(raw_text, title)
  article = Article(source=source, url=url, title=title, raw_text=raw_text, date=timestamp, keywords=keywords)
  return Topic([article], keywords), keywords, article

def raw_text_from_uri(uri, body_parser):
  soup = get_soup(uri)
  # print(soup)
  paragraphs = get_soup_paragraphs(soup['soup'])
  filtered = body_parser(paragraphs)
  raw_text, mapped = clean_soup_text(filtered)
  # raw_text = get_full_text(uri)
  photoless = re.sub('Photos: ', '', raw_text)
  head, sep, tail = photoless.partition('.<div')
  return head, mapped

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
      'paragraphs': paragraphs,
    }
  else:
    print('### NO TEXT')
    return {'ok': False, 'text': soup['content']}
  # paragraphs = get_soup_paragraphs(soup)

# def filtered(source):