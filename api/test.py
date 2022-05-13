
from feeder.models.source import active_topics, topics_by_key, custom_google_source, az_central, google
from feeder.formatter.topic_mapper import fetch_articles, map_articles
from feeder.extractor.rss_extractor import get_full_text
# print_source_articles()

# user settings coming soon! 
albert = {
  'email': 'schweitzer.albert@gmail.com',
  'sources': ['guardian', 'bbc', 'reuters', 'dw', 'google'],
  'experimental': True,
  'keywords': False,
  'debug': True,
  'limit': 8
}

mansi = {
  'email': 'mansidhamija24@gmail.com',
  'sources': ['guardian', 'bbc', 'reuters', 'dw', 'google'],
  'keywords': True,
  'debug': False,
  'limit': 8,
  'experimental': True
}

marisel= {
  'email': 'marisel.schweitzer@gmail.com',
  'sources': ['guardian', 'bbc', 'reuters', 'dw', 'google'],
  'keywords': True,
  'debug': False,
  'limit': 8,
  'experimental': True
}

def print_articles_for_sources (sources):
  for (description, topics) in sources.items():
    print(description)
    for index, topic in enumerate(topics):
      # print(topic.keywords)
      for article in topic.articles:
        print(article.title)
        print(article.url)
        print(article.source)
        print(article.date)
        print(article.keywords)

# articles = google.get_feed_articles(10)
# print_articles_for_sources({'google': articles})

db_rows = fetch_articles()
articles = map_articles(db_rows)

for article in articles:
  content = get_full_text(article.url)
  print(article.source)
  print(content)
  print('')