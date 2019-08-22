from bs4 import BeautifulSoup
import util.api
import json
import time
from gensim.summarization import keywords
from gensim.summarization.summarizer import summarize
from collections import defaultdict
import re
from util.description_parsers import parsers
from util.api import get_feed_for

last = ''

# parse xml feed into soup
def parse_feed_xml (source):
  data = get_feed_for(source)
  soup = BeautifulSoup(data, 'xml')
  return soup

# assembles text output of summaries
def get_briefing (data, max):
  summary = ''
  output_text = ''
  get_headlines()
  # print(items)
  item_index = 0
  for item in items:
    item_title = item.title.string
    # print(item_title)
    output_text += "{}\n\n".format(item_title)
    item_soup = BeautifulSoup(item.description.get_text(), "html.parser")
    description = item_soup.get_text()
    output_text += "{}\n\n\n".format(description)
    summary += "{} ".format(description)
    item_index += 1
    if item_index >= max:
      break
  print("collection")
  print(summary)
  output_text += '###\n\n\n'
  summ = summarize(summary)
  print("summarized")
  print(summ)
  ret_val = "SUMMARY\n\n{summ}===========\n\nHEADLINES\n\n{headlines}".format(summ=summ, headlines=output_text)

  return ret_val, summary

# gets headlines and summary for rss feed
def get_headlines_for_source (source, limit):
  soup = parse_feed_xml(source)
  title = soup.title.string
  ret = defaultdict(list)
  ret["source"] = title
  print(title)

  items = soup.find_all("item")
  item_index = 0
  for item in items:
    article = {
      'title': item.title.string,
      'content': item.description.get_text(),
      'link': item.link.string
    }
    ret["articles"].append(article)
    item_index += 1
    if item_index >= limit:
      break
  print(ret)
  # summary = summarize_articles(ret["articles"])
  # ret["summary"] = summary
  return ret

# summarize text using gensim
def summarize_articles (articles):
  raw_summary = ""
  print(len(articles))
  for article in articles:
    raw_summary += "{} . ".format(article["content"])

  summ = summarize(raw_summary, ratio=.7, split=False)
  print(raw_summary)
  print(summ)

  return summ

# summarize rss feed articles using SMMRY
def get_summaries_from_source (source, max = 2):
  soup = parse_feed_xml(source)
  title = soup.title.string
  ret = defaultdict(list)
  ret["source"] = title

  items = soup.find_all("item")
  item_index = 0
  for item in items:
    result = util.api.get_summary(item.link.string)
    parsed = json.loads(result)
    if "sm_api_error" not in parsed:
      article = {
        'title': "{}".format(parsed['sm_api_title']),
        'content': "{}".format(parsed['sm_api_content']),
        'link': item.link.string
      }
      ret["articles"].append(article)
      ret["api_limitation"] = '+++ {} +++'.format(parsed["sm_api_limitation"])
      item_index+=1
      if item_index >= max:
        break
      time.sleep(10)

  return ret

def get_summaries_from_google_headlines (news, max = 2):
  ret = news
  api_limitation = ''
  news_index = 0
  for news_obj in news:
    article_index = 0
    raw_summary = ''
    for article in news_obj['articles']:
      print(article['title'])
      res = summry_from_url(article['url'])
      if res['ok'] == True:
        api_limitation = res['api_limitation']
        ret[news_index]['articles'][article_index]['summary'] = res['summary']
        raw_summary += "{} . ".format(res['summary'])
      article_index += 1
    
    ret[news_index]['summary'] = summarize(raw_summary, ratio=.7, split=False)
    news_index += 1
    if news_index >= max:
      break
  # ret['api_limitation'] = api_limitation
  return {'news': ret, 'api_limitation': api_limitation}
      
def summry_from_url (url):
  ret = {}
  result = util.api.get_summary(url)
  parsed = json.loads(result)
  if "sm_api_error" not in parsed:
    ret["summary"] = "{}".format(parsed['sm_api_content'])
    ret["api_limitation"] = '+++ {} +++'.format(parsed["sm_api_limitation"])
    ret['ok'] = True
    time.sleep(10)
    return ret
  else:
    return {'ok': False, 'err': parsed['sm_api_error']}