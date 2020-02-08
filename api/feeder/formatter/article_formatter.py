from api.feeder.common.article import Article
from api.feeder.common.topic import Topic
from api.feeder.formatter import formatter
from bs4 import BeautifulSoup


def topics_from_guardian_item (article):
  url = article.link.string
  title = article.title.string
  date = date.today() if article.pubDate is None else article.pubDate.string
  brief = parse_guardian(article.description.get_text()) if article.description else article.title.string + '...'
  article = Article('The Guardian', url, title, brief, date)
  keywords = formatter.keywords_from_strings(brief.split('. '))
  topic = Topic([article], keywords)

  return topic

def topics_from_google_item (item):
  item_soup = BeautifulSoup(item.description.get_text(), "html.parser")
  list_items = item_soup.findAll('li')

  date = (item.pubDate.string if item.pubDate is not None else date.today())
  if len(list_items) < 2:
    article = article_from_google_item(item_soup, date)
    keywords = formatter.keywords_from_strings([article.title])
    return Topic([article], keywords)
  else:
    articles = []
    for item in list_items:
      if item.find('strong') is not None:
        # link to google news
        continue

      article = article_from_google_item(item, date)
        
      articles.append(article)
    headlines = list(map(lambda article: article.title, articles))
    keywords = formatter.keywords_from_strings(headlines)
    return Topic(articles, keywords)

def article_from_google_item (article, date):
  a = article.find('a')
  title = a.get_text()
  source = article.find('font').get_text()
  article = Article(source, a['href'], title, '', date)
  return article

def reuters (content):
  soup = BeautifulSoup(content, "html.parser")
  return soup.get_text()


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

def default (article):
  url = article.link.string
  title = article.title.string
  date = date.today() if article.pubDate is None else article.pubDate.string
  brief = parse_guardian(article.description.get_text()) if article.description else article.title.string + '...'
  article = Article('SOURCE', url, title, brief, date)
  keywords = formatter.keywords_from_strings(brief.split('. '))
  topic = Topic([article], keywords)

  return topic

def reuters (article):
  url = article.link.string
  title = article.title.string
  date = date.today() if article.pubDate is None else article.pubDate.string
  brief = parse_reuters(article.description.get_text()) if article.description else article.title.string + '...'
  article = Article('Reuters', url, title, brief, date)
  keywords = formatter.keywords_from_strings([brief])
  topic = Topic([article], keywords)

  return topic

def parse_reuters (description):
  split = description.split('<div class="feedflare">')
  # soup = BeautifulSoup(description, 'html.parser')
  print(split)
  return split[0]
