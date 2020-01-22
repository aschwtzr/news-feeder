from bs4 import BeautifulSoup
# to run via command line remember to remove util. from the import
import util.description_parsers
from collections import defaultdict
import logging

# google news world rss feed
def get_google_world_news_feed (topic = None):
  data = util.api.get_feed_for('world' if topic is None else topic)
  soup = BeautifulSoup(data, 'xml')
  items = soup.findAll('item')

  news_bullets = []
  # change headline to topic
  for topic in items:
    result = defaultdict(list)
    media = topic.find('content')

    # get images
    if media is not None:
      result['media'] = media['url']

    # parse soup for list of articles
    item_soup = BeautifulSoup(topic.description.get_text(), "html.parser")
    list_items = item_soup.findAll('li')

    if len(list_items) > 1:
      for index, article in enumerate(list_items):
        strong = article.find('strong')
        if strong is not None:
          # link to google news
          logging.info('skipping list item with strong tag.. eval:')
          logging.info(strong.get_text() == 'View full coverage on Google News')
          continue

        articleObj = util.news_formatter.article_from_google_rss_li(article)

        # get publication date
        if topic.pubDate is not None and index == 0:
          articleObj["date"] = topic.pubDate.string

        result['articles'].append(articleObj)
      headlines = list(map(lambda article: article["title"], result["articles"]))
      result['title'] = util.news_formatter.keywords_from_strings(headlines)
    else:
      article = item_soup
      articleObj = util.news_formatter.article_from_google_rss_li(article)
      result['title'] = articleObj["title"]
      if topic.pubDate is not None and index == 0:
        result["date"] = topic.pubDate.string
      result['articles'] = articleObj

    news_bullets.append(result)
  return news_bullets

# gets headlines from rss feed
def get_news_from_rss (source, limit):
  if source is None:
    print('must provide source')
    return
  soup = util.news_formatter.parse_feed_xml(source)

  ret = defaultdict(list)
  try:
    ret["source"] = soup.title.string
  except:
    print(soup)
  items = soup.find_all("item")
  for item_index, item in enumerate(items):
    parser = util.description_parsers.parsers[source]
    article = {
      'title': item.title.string,
      'preview': parser(item.description.get_text()) if item.description else item.title.string + '...',
      'url': item.link.string,
      'source': ret["source"],
      'date': ('' if item.pubDate is None else item.pubDate.string)
    }

    ret["articles"].append(article)
    if item_index >= limit - 1:
      break
  if len(ret["articles"]) > 1:
    content_list = list(map(lambda article: article["preview"], ret["articles"]))
    ret["summary"] = util.news_formatter.gensim_summ_from_list(content_list)
  else:
    ret["summary"] = "fake summary"
    # print(ret)
  return ret