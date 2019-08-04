from bs4 import BeautifulSoup
import util.api
import json
import time
from gensim.summarization import keywords
from gensim.summarization.summarizer import summarize
from collections import defaultdict
import re

last = ''

def parse_feed_xml (data):
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
def get_headlines_for_rss_feed (data, limit):
  soup = parse_feed_xml(data)
  title = soup.title.string
  ret = defaultdict(list)
  ret["source"] = title

  print(title)
  items = soup.find_all("item")

  item_index = 0
  for item in items:
    item_soup = BeautifulSoup(item.description.get_text(), "html.parser")
    print("SOUP")
    print(item_soup)
    print("TEXT")
    print(item)
    article = {
      'title': item.title.string,
      'content': item_soup.get_text(),
      'link': item.link.get_text()
    }
    ret["articles"].append(article)
    item_index += 1
    if item_index >= limit:
      break

  summary = summarize_articles(ret["articles"])
  ret["summary"] = summary
  return ret

# summarize rss feed articles using SMMRY g
def summarize_articles (articles):
  raw_summary = ""
  print(len(articles))
  for article in articles:
    raw_summary += "{} . ".format(article["content"])
  print(raw_summary)

  return summarize(raw_summary, ratio=.7, split=True)

def get_summaries (data, max = 2):
  soup = parse_feed_xml(data)
  title = soup.title.string
  ret = defaultdict(list)
  ret["source"] = title
  # print(title)

  items = soup.find_all("item")
  item_index = 0
  for item in items:
    result = util.api.get_summary(item.link.string)
    parsed = json.loads(result)
    if "sm_api_error" not in parsed:
      # print("{}\n".format(parsed['sm_api_title']))
      # print("{}\n\n".format(parsed['sm_api_content']))
      article = {
        'title': "{}".format(parsed['sm_api_title']),
        'content': "{}".format(parsed['sm_api_content']),
      }
      ret["articles"].append(article)
      ret["api_limitation"] = '+++ {} +++'.format(parsed["sm_api_limitation"])
      item_index+=1
      if item_index >= max:
        break
      time.sleep(10)

  print(last)
  print(ret)
  print("\n\n\n\n\n")
  return ret


# def summarize_content(articles):
#   summary = ''
#   for article in articles: 
    
