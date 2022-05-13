from datetime import datetime, timedelta
from feeder.models.article import Article
from feeder.formatter.content_fixer import clean_article_data
from feeder.formatter.topic_mapper import map_article_relationships, keyword_frequency_map, map_topic, make_topics_map, print_topic_map
import pandas as pd

# make topic and summary map
def get_summary(hours_ago=18):
  hours_ago_date_time = datetime.now() - timedelta(hours = hours_ago)
  articles = Article.select().where((Article.date > hours_ago_date_time) & (Article.summary.is_null(False)))
  print(f"ARTICLES IS THIS MANY {len(articles)}")
  processed = list(map(lambda article: clean_article_data(article, False, False, True), articles))
  # processed = articles

  mapped_kw = keyword_frequency_map(processed)
  # print(mapped_kw)

  relationship_map = map_article_relationships(processed, mapped_kw)
  # print(json.dumps(relationship_map, sort_keys=True, indent=2))

  df = pd.DataFrame(data = list(map(lambda x: [x.source, x.url, x.title, x.date, x.id, x.keywords, x.raw_text, x.summary, x.nlp_kw], processed)), columns = ['source', 'url', 'title', 'date', 'id', 'keywords', 'content', 'summary', 'nlp_kw'])

  topic_map = make_topics_map(processed, relationship_map, df)
  print_topic_map(topic_map, df)
  mapped_topics = map(lambda tuple: map_topic(tuple[1], df), topic_map.items())
  mapped_topics_list = sorted(list(mapped_topics), key=lambda topic: (len(topic.articles), topic.date), reverse=True)   
      
  counts = {
    'articles': len(processed),
    'topics': len(mapped_topics_list),
  }
  return {
    'counts': counts,
    'topics': mapped_topics_list,
    'mapped_kw': mapped_kw
  }