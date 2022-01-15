# extract rss feed content and package it into topics and articles
# extract keywords
from feeder.models.article import Article
from feeder.models.topic import Topic
from feeder.formatter import keyword_extractor
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
    text = clean_content(text)
    return {'ok': True, 'text': text}
  else:
    print('### NO TEXT')
    return content

# remove junk content from article body text
def clean_content(string):
  string = re.sub("Take a look at the beta version of dw.com. We're not done yet! Your opinion can help us make it better.", '', string)
  string = re.sub("We use cookies to improve our service for you. You can find more information in our data protection declaration.", '', string)
  string = re.sub("Got a confidential news tip? We want to hear from you.", '', string)
  string = re.sub("By subscribing I accept the terms of use and privacy policy", '', string)
  string = re.sub(r"(© 2021 Deutsche Welle.*)", '', string)
  string = re.sub(r"(Sign up for.*).", '', string)
  string = re.sub(r"(© 2021 CNBC.*)", '', string)
  string = re.sub(r"(\\n\\n.*\\n\\n)", '', string)
  string = re.sub(r'(( \| )|( \- )).*', '', string)
  return string

def topics_from_google_item (item):
  item_soup = BeautifulSoup(item.description.get_text(), "html.parser")
  list_items = item_soup.findAll('li')

  timestamp = (item.pubDate.string if item.pubDate is not None else timestamp_string())
  if len(list_items) < 2:
    article = article_from_google_item(item_soup, timestamp)
    # keywords = keyword_extractor.keywords_from_string_list([article.title])
    if len(article.brief) > 1:
      keywords = keyword_extractor.keywords_from_article(article)
    else:
      keywords = keyword_extractor.keywords_from_string(article.title)
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
    keywords = keyword_extractor.keywords_from_string_list(headlines)
    for article in articles:
      article_kw = set(article.keywords)
      topic_kw = set(keywords)
      article.keywords += list(topic_kw - article_kw)

    if len(keywords) < 1:
      keywords = keyword_extractor.word_ranker(headlines)
      print(f"first keywords failed, using word ranker keywords")
      print(keywords)
    return Topic(articles, keywords)

def article_from_google_item (article, timestamp):
  a = article.find('a')
  title = a.get_text()
  clean_title = keyword_extractor.remove_publication_after_pipe(title)
  source = article.find('font').get_text()
  keywords = keyword_extractor.keywords_from_string(title)
  brief = get_full_text(a['href'])
  if brief['ok'] == True:
    brief = brief['text']
  else:
    brief = ''
  article = Article(source, a['href'], clean_title, brief, timestamp, keywords)
  return article

def yahoo (content):
  soup = BeautifulSoup(content, "html.parser")
  return soup.get_text()

def guardian (article):
  url = article.link.string
  title = article.title.string
  timestamp = timestamp_string() if article.pubDate is None else article.pubDate.string
  brief = get_full_text(url)
  if brief['ok'] == True:
    brief = brief['text']
  else:
    brief = parse_guardian(article.description.get_text()) if article.description else article.title.string + '...'
  article = Article('The Guardian', url, title, brief, timestamp)
  keywords = keyword_extractor.keywords_from_article(article)
  article.keywords = keywords
  # keywords = keyword_extractor.keywords_from_string_list(brief.split('. '))
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
  topic = default(article, 'Deutsche Welle')
  return topic

def az_central (article):
  topic = default(article, 'AZ Central')
  return topic

def default (article, source):
  url = article.link.string
  title = article.title.string
  if article.pubDate is not None:
   timestamp = article.pubDate.string
  elif article.date is not None:
    timestamp = article.date.string
  else:
    timestamp = timestamp_string()
  brief = get_full_text(url)
  if brief['ok'] == True:
    brief = brief['text']
  else:
    brief = article.description.get_text() if article.description else article.title.string + '...'
  photoless = re.sub('Photos: ', '', brief)
  head, sep, tail = photoless.partition('.<div')
  article = Article(source, url, title, head, timestamp)
  # keywords = keyword_extractor.keywords_from_string_list(brief.split('. '))
  keywords = keyword_extractor.keywords_from_article(article)
  article.keywords = keywords
  topic = Topic([article], keywords)

  return topic

def reuters (article):
  url = article.link.string
  title = article.title.string
  timestamp = timestamp_string() if article.pubDate is None else article.pubDate.string
  brief = parse_reuters(article.description.get_text()) if article.description else article.title.string + '...'
  article = Article('Reuters', url, title, brief, timestamp)
  keywords = keyword_extractor.keywords_from_article(article)
  article.keywords = keywords
  # keywords = keyword_extractor.keywords_from_string_list([brief])
  topic = Topic([article], keywords)

  return topic

def parse_reuters (description):
  split = description.split('<div class="feedflare">')
  # soup = BeautifulSoup(description, 'html.parser')
  return split[0]

def bbc (article):
  topic = default(article, 'BBC')
  return topic
