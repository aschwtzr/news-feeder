import requests
from bs4 import BeautifulSoup
from gensim.summarization import keywords

wiki_summaries = []
search_terms = []

def get_wiki_news():
  yesterday = date.today() - timedelta(days=1)
  req = requests.get('https://en.wikipedia.org/api/rest_v1/page/html/Portal%3ACurrent_Events')
  soup = BeautifulSoup(req.text, 'html.parser')
  content = soup.find(id=yesterday.strftime('%Y_%B_%-d')).find_all('li')
  print(yesterday.strftime('%Y_%B_%-d'))
  news_bullets = [topic.get_text() for topic in content]
  global wiki_summaries
  wiki_summaries = news_bullets

  for news_item in news_bullets:
    kwrds = keywords(news_item, ratio=.2)
    search_string = ''
    for word in kwrds:
      search_string += word

    search_terms.append(search_string.replace("\n", " "))