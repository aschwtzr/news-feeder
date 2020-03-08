from feeder.common.source import google, guardian, bbc, reuters, dw
from bs4 import BeautifulSoup

limit = 5
# sources can fetch a short history
def print_source_articles ():
  google_results = google.get_feed_articles(5)
  print('GOOGLE')
  for index, topic in enumerate(google_results):
    topic.woof()
    if index >= limit - 1:
      break

  guardian_results = guardian.get_feed_articles(5)
  print('GUARDIAN')
  for index, topic in enumerate(guardian_results):
    topic.woof()
    if index >= limit - 1:
      break

  print('BBC')
  bbc_results = guardian.get_feed_articles(5)
  for index, topic in enumerate(bbc_results):
    topic.woof()
    if index >= limit - 1:
      break

  print('REUTERS')
  reuters_results = reuters.get_feed_articles(5)
  for index, topic in enumerate(reuters_results):
    topic.woof()
    if index >= limit - 1:
      break