from api.feeder.common.source import google, guardian
limit = 5
# sources can fetch a short history
def print_source_articles ():
  google_results = google.get_feed_articles()

  for index, topic in enumerate(google_results):
    topic.woof()
    if index >= limit - 1:
      break

  guardian_results = guardian.get_feed_articles()
  