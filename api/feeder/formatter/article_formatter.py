from feeder.common.article import Article
from feeder.common.topic import Topic
from feeder.formatter import formatter
from bs4 import BeautifulSoup
from datetime import date

def topics_from_guardian_item (article):
  url = article.link.string
  title = article.title.string
  timestamp = date.today() if article.pubDate is None else article.pubDate.string
  brief = parse_guardian(article.description.get_text()) if article.description else article.title.string + '...'
  article = Article('The Guardian', url, title, brief, timestamp)
  # keywords = formatter.keywords_from_string_list(brief.split('. '))
  keywords = formatter.keywords_from_string(title)
  topic = Topic([article], keywords)

  return topic

def topics_from_google_item (item):
  item_soup = BeautifulSoup(item.description.get_text(), "html.parser")
  list_items = item_soup.findAll('li')

  timestamp = (item.pubDate.string if item.pubDate is not None else date.today())
  if len(list_items) < 2:
    article = article_from_google_item(item_soup, timestamp)
    # keywords = formatter.keywords_from_string_list([article.title])
    keywords = formatter.keywords_from_string(article.title)
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
    keywords = formatter.keywords_from_string_list(headlines)
    return Topic(articles, keywords)

def article_from_google_item (article, timestamp):
  a = article.find('a')
  title = a.get_text()
  source = article.find('font').get_text()
  article = Article(source, a['href'], title, '', timestamp)
  return article


def yahoo (content):
  soup = BeautifulSoup(content, "html.parser")
  return soup.get_text()

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

def default (article, source):
  url = article.link.string
  title = article.title.string
  timestamp = date.today() 
  if article.pubDate is not None:
   timestamp = article.pubDate.string
  elif article.date is None:
    timestamp = article.date.string
  brief = article.description.get_text() if article.description else article.title.string + '...'
  article = Article(source, url, title, brief, timestamp)
  # keywords = formatter.keywords_from_string_list(brief.split('. '))
  keywords = formatter.keywords_from_string(title)
  topic = Topic([article], keywords)

  return topic

def reuters (article):
  url = article.link.string
  title = article.title.string
  timestamp = date.today() if article.pubDate is None else article.pubDate.string
  brief = parse_reuters(article.description.get_text()) if article.description else article.title.string + '...'
  article = Article('Reuters', url, title, brief, timestamp)
  # keywords = formatter.keywords_from_string_list([brief])
  keywords = formatter.keywords_from_string(title)
  topic = Topic([article], keywords)

  return topic

def parse_reuters (description):
  split = description.split('<div class="feedflare">')
  # soup = BeautifulSoup(description, 'html.parser')
  return split[0]

def bbc (article):
  topic = default(article, 'BBC')
  return topic
