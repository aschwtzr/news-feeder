from feeder.common.source import google, guardian, bbc, reuters, dw
from bs4 import BeautifulSoup

topics = {}

limit = 10
# sources can fetch a short history
def print_source_articles ():
  # google_results = google.get_feed_articles(limit)
  # print('GOOGLE')
  # for index, topic in enumerate(google_results):
  #   topic.woof()
  #   add_keywords_to_topics(topic)
  #   if index >= limit - 1:
  #     break
  # print("###\n\n")

  # guardian_results = guardian.get_feed_articles(limit)
  # print('GUARDIAN')
  # for index, topic in enumerate(guardian_results):
  #   topic.woof()
  #   add_keywords_to_topics(topic)
  #   if index >= limit - 1:
  #     break
  # print("###\n\n")

  # print('BBC')
  # bbc_results = guardian.get_feed_articles(limit)
  # for index, topic in enumerate(bbc_results):
  #   topic.woof()
  #   add_keywords_to_topics(topic)
  #   if index >= limit - 1:
  #     break
  # print("###\n\n")

  # print('REUTERS')
  # reuters_results = reuters.get_feed_articles(limit)
  # for index, topic in enumerate(reuters_results):
  #   topic.woof()
  #   add_keywords_to_topics(topic)
  #   if index >= limit - 1:
  #     break
  # print("###\n\n")

  print('DW')
  reuters_results = dw.get_feed_articles(limit)
  for index, topic in enumerate(reuters_results):
    topic.woof()
    add_keywords_to_topics(topic)
    if index >= limit - 1:
      break
  print("###\n\n")

  # for key, value in topics.items():
  #   print(f"{key}: {len(value)}")
  #   for article in value:
  #     print(article.title)


def add_keywords_to_topics(topic):
  # print(topic.keywords)
  word_list = topic.keywords.split(' ')
  for keyword in word_list:
      # print(keyword)
      topics[keyword] = topic.articles