from bs4 import BeautifulSoup
# to run via command line remember to remove util. from the import
import util.description_parsers
from collections import defaultdict

# google news world rss feed
# feed <description> is a list of articles
# return format: [{ title: 'high level headline', articles: [{ source, title, url}]},]
def get_google_world_news_feed ():
  data = util.api.get_feed_for('google')
  soup = BeautifulSoup(data, 'xml')
  items = soup.findAll('item')

  news_bullets = []
  print(f'items count: {len(items)}')
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
      article = {
        'title': title_text,
        'url': a['href'],
        'source': bullet.find('font').get_text()
      }
      news_item['articles'].append(article)
    news_bullets.append(news_item)
  return news_bullets

# gets headlines from rss feed
# return format: {source: source, summary: summary, articles: [{ title: 'headline', content: 'provided article summary', link: 'url'}]}
def get_feed_for_source (source, limit):
  if source is None:
    print('must provide source')
    return
  soup = util.news_formatter.parse_feed_xml(source)

  title = soup.title.string
  ret = defaultdict(list)
  ret["source"] = title
  items = soup.find_all("item")
  item_index = 0
  for item in items:
    parser = util.description_parsers.parsers[source]
    article = {
      'title': item.title.string,
      'content': parser(item.description.get_text()),
      'url': item.link.string
    }
    ret["articles"].append(article)
    item_index += 1
    if item_index >= limit:
      break
  ret["summary"] = util.news_formatter.summarize_feed_articles(ret["articles"])
  return ret