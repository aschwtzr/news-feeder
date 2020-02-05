from collections import defaultdict
from bs4 import BeautifulSoup
from api.feeder.formatter import formatter
import logging
from datetime import date

def google_feed_to_json(data):
  soup = BeautifulSoup(data, 'xml')
  items = soup.findAll('item')

  news_bullets = []

  for topic in items:
    result = defaultdict(list)
    media = topic.find('content')
    
    # get images
    if media is not None:
      result['media'] = media['url']

    # parse soup for list of articles
    item_soup = BeautifulSoup(topic.description.get_text(), "html.parser")
    list_items = item_soup.findAll('li')

    date = (topic.pubDate.string if topic.pubDate is not None else date.today())
    if len(list_items) > 1:
      for index, article in enumerate(list_items):
        strong = article.find('strong')
        if strong is not None:
          # link to google news
          # print('skipping list item with strong tag.. eval:')
          # print(strong.get_text() == 'View full coverage on Google News')
          continue
 
        articleObj = formatter.article_from_google_item(article, date)
        # articleObj.print()
        result['articles'].append(articleObj)
      headlines = list(map(lambda article: article.title, result["articles"]))
      # print('## HEADLINES ##\n')
      # print(headlines)
      # print(formatter.keywords_from_strings(headlines))
      headlines = list(map(lambda article: article.title, result["articles"]))
      keyword_title = formatter.keywords_from_strings(headlines)
      result['title'] = keyword_title
    else:
      article = item_soup
      articleObj = formatter.article_from_google_item(article, date)
      result['title'] = articleObj.title
      result['articles'] = articleObj

    news_bullets.append(result)
  print(news_bullets)
  return news_bullets