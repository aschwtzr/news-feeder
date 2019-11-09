from bs4 import BeautifulSoup
# to run via command line remember to remove util. from the import
import util.description_parsers
from collections import defaultdict
import logging

# google news world rss feed
def get_google_world_news_feed ():
  data = util.api.get_feed_for('google')
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

    # get publication date
    if topic.pubDate is not None:
      result["date"] = topic.pubDate.string

    # parse soup for list of articles
    item_soup = BeautifulSoup(topic.description.get_text(), "html.parser")
    list_items = item_soup.findAll('li')

    if len(list_items) > 1:
      for article in list_items:
        strong = article.find('strong')
        if strong is not None:
          # link to google news
          logging.info('skipping list item with strong tag.. eval:')
          logging.info(strong.get_text() == 'View full coverage on Google News')
          continue
        articleObj = util.news_formatter.article_from_google_rss_li(article)
        result['articles'].append(articleObj)
      headlines = list(map(lambda article: article["title"], result["articles"]))
      result['title'] = util.news_formatter.keywords_from_strings(headlines)
    else:
      article = item_soup
      articleObj = util.news_formatter.article_from_google_rss_li(article)
      result['title'] = articleObj["title"]
      result['articles'] = articleObj

    news_bullets.append(result)
  return news_bullets

# gets headlines from rss feed
def get_news_from_rss (source, limit):
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
      'url': item.link.string,
    }
    if item.pubDate is not None:
      article["date"] = item.pubDate.string
    ret["articles"].append(article)
    item_index += 1
    if item_index >= limit:
      break
  if len(ret["articles"]) > 1:
    content_list = list(map(lambda article: article["content"], ret["articles"]))
    ret["summary"] = util.news_formatter.gensim_summ_from_list(content_list)
  else:
    ret["summary"] = "fake summary"
    # print(ret)
  return ret