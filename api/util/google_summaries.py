from bs4 import BeautifulSoup
# to run via command line remember to remove util. from the import
import util.api
from collections import defaultdict

def get_google_world_news ():
  data = util.api.get_feed_for('google')
  soup = BeautifulSoup(data, 'xml')
  items = soup.findAll('item')
  news_bullets = []
  # print(items)
  for headline in items:
    news_item = defaultdict(list)
    media = headline.find('content')
    news_item['title'] = headline.title.string
    if media is not None:
      news_item['media'] = media['url']
    item_soup = BeautifulSoup(headline.description.get_text(), "html.parser")
    list_items = item_soup.findAll('li')
    for bullet in list_items:
      strong = bullet.find('strong')
      if strong is not None:
        continue
      a = bullet.find('a')
      title_text = a.get_text()
      break_index = title_text.find('-')
      article = {
        'title': title_text[0:break_index + 1],
        'url': a['href'],
        'source': bullet.find('font').get_text()
      }
      news_item['articles'].append(article)
    news_bullets.append(news_item)
  return news_bullets

get_google_world_news()