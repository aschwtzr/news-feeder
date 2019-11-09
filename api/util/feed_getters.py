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
  # change headline to topic
  for headline in items:
    result = defaultdict(list)
    media = headline.find('content')

    headlinesCollection = ''
    # title_split = headline.title.string.rpartition(' - ')
    # result['title'] = title_split[0]
    # result['source'] = title_split[2]

    # get images
    if media is not None:
      result['media'] = media['url']

    # get publication date
    if headline.pubDate is not None:
      result["date"] = headline.pubDate.string

    # parse soup for list of articles
    item_soup = BeautifulSoup(headline.description.get_text(), "html.parser")
    list_items = item_soup.findAll('li')

    for article in list_items:
      strong = article.find('strong')
      if strong is not None:
        continue
      a = article.find('a')
      title_text = a.get_text()
      articleObj = {
        'title': title_text,
        'url': a['href'],
        'source': article.find('font').get_text()
      }
      headlinesCollection += f' {title_text}'
      result['articles'].append(articleObj)
    result['title'] = util.news_formatter.summary_from_headlines(headlinesCollection)
    news_bullets.append(result)
  return news_bullets

# gets headlines from rss feed
# return format: {source: source, summary: summary, articles: [{ title: 'headline', content: 'provided article summary', link: 'url'}]}
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
  ret["summary"] = util.news_formatter.summary_from_articles(ret["articles"])
  return ret