from bs4 import BeautifulSoup
import util.api
import json
import time
from gensim.summarization import keywords
from gensim.summarization.summarizer import summarize
from collections import defaultdict
import re
from util.api import get_feed_for

# parse xml feed into soup
def parse_feed_xml (source):
  data = get_feed_for(source)
  soup = BeautifulSoup(data, 'xml')
  return soup

# summarize text using gensim
# takes a list of article objects with a content field
def summary_from_articles (summaries):
  raw_summary = ""
  try:
    for summary in summaries:
      raw_summary += """{} """.format(summary)
    summ = summarize(raw_summary, ratio=.5, split=True)

    return { 'ok': True, 'data': summ }
  except:
    return { 'ok': False, 'err': 'Error with GENSIM processing.' }
  
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
        'url': item.link.string
      }
      ret["articles"].append(article)
      ret["api_limitation"] = '+++ {} +++'.format(parsed["sm_api_limitation"])
      item_index+=1
      if item_index >= max:
        break
      time.sleep(10)

  return ret

def get_summaries_from_google_feed (news, max = 2):
  ret = news
  api_limitation = ''
  news_index = 0
  for news_obj in news:
    article_index = 0
    raw_summary = ''
    for article in news_obj['articles']:
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
  return {'news': ret, 'api_limitation': api_limitation}
      
def summry_from_url (url):
  ret = {}
  result = util.api.get_summary(url)
  parsed = json.loads(result)
  if "sm_api_error" not in parsed:
    ret["summary"] = "{}".format(parsed['sm_api_content'])
    if "sm_api_limitation" in parsed:
      ret["api_limitation"] = ''.format(parsed["sm_api_limitation"])
      # time.sleep(10)
    else:
      ret["api_limitation"] = 'Caution: paid mode is enabled.'
    ret['ok'] = True
    return ret
  else:
    return {'ok': False, 'err': parsed['sm_api_error']}

# get keywords from paragraph
# TODO: ultimately this should take an array of sentences that is formatted by the caller
def summary_from_headlines (text):
  keywordsFromText = keywords(text, split=True, scores=False, words=8)
  sentence = ''
  for pair in keywordsFromText:
    sentence += f'{pair} '
  return sentence
