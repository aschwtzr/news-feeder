import news_formatter
import time
import api
import random
import string
import util
import datetime
from gensim.summarization.summarizer import summarize

# TODO: CONVERT TO CLI INTERFACE

filename = filename = "{date:%Y-%m-%d_%H:%M:%S}.txt".format(date=datetime.datetime.now())

news_sources = ["google", "reuters", "bbc", "dw", "guardian"]

def get_feed_for (source):
  results = api.get_feed_for(source)
  return results

def get_all ():
  output_text = ''
  summaries = ''
  for source in news_sources:
    feed = get_feed_for(source)
    # news_formatter.print_summaries(feed)
    briefing, summary = news_formatter.print_briefing(feed, 5)
    output_text += "{}\n\n".format(briefing)
    summaries += "{} ".format(summary)
    time.sleep(5)
  today = summarize(summaries)
  ret_val = "TODAY:\n\n{summ}\n\n\nNEWS\n\n{news}".format(summ=today, news=output_text)
  return ret_val

def get_smmry_for(source):
      feed = get_feed_for(source)
    summ = news_formatter.get_summaries(feed, 4)
    headlines = ''
    for article in summ["articles"]:
      headlines += "{title}\n====\n{content}\n\n".format(title=article["title"], content=article["content"])
      summary += article["content"]
    today = summarize(summary)
    print("TODAY")
    print(today)
    print("SUMMARY")
    print(summary)


def main ():
  global filename
  summary = ''
  with open(filename, "a") as output_file:
    # news = get_all()
    # output_file.write(news)
    get_smmry_for("guardian")
    output_file.write("TODAY\n{today}\n=====\n{source}\n\n{headlines}\n###".format(today=today, source=summ["source"], headlines=headlines))


main()
