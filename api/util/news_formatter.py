from bs4 import BeautifulSoup
import util.api
import json
import time
from gensim.summarization import keywords
from gensim.summarization.summarizer import summarize
from collections import defaultdict
import re
from util.api import get_feed_for

import logging

# parse xml feed into soup
def parse_feed_xml (source):
  data = get_feed_for(source)
  soup = BeautifulSoup(data, 'xml')
  return soup

# MARK: refactor line
      
# get keywords from list of strings
def keywords_from_strings (string_list):
  words = 8 if len(string_list) >= 4  else len(string_list)
  reduced = ". ".join([headline for headline in string_list])
  keywordsFromText = keywords(reduced, split=True, scores=False, words=words)
  sentence = ''
  for pair in keywordsFromText:
    sentence += f'{pair} '
  return sentence

# summarize array of sentences using gensim
def gensim_summ_from_list (summaries):
  raw_summary = ""
  if len(summaries) <= 1:
    return summaries[0]
  try:
    for summary in summaries:
      raw_summary += f"{summary} "
    summ = summarize(raw_summary, ratio=.3, split=False)
    return summ 
  except:
    print("Error with GENSIM processing")
    # throws silently when commented
    raise

def summary_from_url (url):
  ret = {}
  result = util.api.get_summary(url)
  parsed = json.loads(result)
  # print(parsed)
  if "sm_api_error" in parsed:
    ret["ok"] = False
    ret["error"] = parsed["sm_api_message"]
    return ret
  
  else:
    ret["summary"] = "{}".format(parsed['sm_api_content'])
    if "sm_api_limitation" in parsed:
      ret["api_limitation"] = ''.format(parsed["sm_api_limitation"])
      # flagged sleep parameter for unpaid API
      # time.sleep(10)
    else:
      ret["api_limitation"] = 'Caution: paid mode is enabled.'
    ret['ok'] = True
    return ret

def article_from_google_rss_li (article):
  a = article.find('a')
  title_text = a.get_text()
  source = article.find('font').get_text()
  articleObj = {
    'title': title_text,
    'url': a['href'],
    'source': source
  }
  return articleObj