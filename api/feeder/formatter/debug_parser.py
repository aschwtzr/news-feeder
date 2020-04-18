# A utility for debugging source and keyword extraction 
from feeder.common.source import google, guardian, bbc, reuters, dw
from collections import defaultdict

topics = defaultdict(list)

def add_keywords_to_topics(topic):
  for keyword in topic.keywords:
      # print(keyword)
      topics[keyword.lower()].extend(topic.articles)

limit = 10
# sources can fetch a short history
def print_source_articles ():
  google_results = google.get_feed_articles(limit)
  print('GOOGLE')
  for index, topic in enumerate(google_results):
    topic.woof()
    add_keywords_to_topics(topic)
    if index >= limit - 1:
      break
  print("###\n\n")

  guardian_results = guardian.get_feed_articles(limit)
  print('GUARDIAN')
  for index, topic in enumerate(guardian_results):
    topic.woof()
    add_keywords_to_topics(topic)
    if index >= limit - 1:
      break
  print("###\n\n")

  print('BBC')
  bbc_results = bbc.get_feed_articles(limit)
  for index, topic in enumerate(bbc_results):
    topic.woof()
    add_keywords_to_topics(topic)
    if index >= limit - 1:
      break
  print("###\n\n")

  print('REUTERS')
  reuters_results = reuters.get_feed_articles(limit)
  for index, topic in enumerate(reuters_results):
    topic.woof()
    add_keywords_to_topics(topic)
    if index >= limit - 1:
      break
  print("###\n\n")

  print('DW')
  reuters_results = dw.get_feed_articles(limit)
  for index, topic in enumerate(reuters_results):
    topic.woof()
    add_keywords_to_topics(topic)
    if index >= limit - 1:
      break
  print("###\n\n")
  sorted_keywords = {k: v for k, v in sorted(topics.items(), key=lambda item: len(item[1]), reverse=True)}
  for key, value in sorted_keywords.items():
    print(f"{key}: {len(value)}")
