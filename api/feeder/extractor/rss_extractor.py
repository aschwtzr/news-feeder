from feeder.models.source import Source
import feeder.util.db as db
from re import search
from datetime import datetime
from feeder.models.article import Article
from feeder.extractor.feed_parser import extract_url

def fetch_new_articles(sources):
  now = datetime.now()
  timestamp = now.strftime('%m/%d/%Y, %H:%M:%S')
  
  print(f"""
  *****************************************  
  *****************************************  
    FETCHING NEWS AT {timestamp}
  *****************************************  
  *****************************************  
  """)
  for source in sources:
    print(f"Fetching articles for {source.description}")
    topics = source.map_topic_stream(20)
    for topic in topics:
      for article in topic.articles:
        # skip google news articles we can't parse
        if source.key == 'google-world':
          url = extract_url(article.url)
          if url == 'error' or search('https://www.youtube.com', url):
            continue
        else:
          url = article.url
        exists = Article.select().where(Article.source==article.source, Article.url==article.url)
        if len(exists.execute()) > 0:
          continue
        # works in theory
        article.save()

# TODO: takes a source param or config
def get_feeds():
  sources = Source.select()
  fetch_new_articles(sources)

