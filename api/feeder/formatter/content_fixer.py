from feeder.formatter.topic_mapper import keyword_frequency_map, map_article_relationships, make_topics_map, print_topic_map, map_topic
from feeder.formatter.keyword_extractor import keywords_from_text_title, remove_known_junk
from feeder.formatter.summarizer import summarize_nlp, small_summarize_nlp, summarize_nltk
from feeder.models.article import Article
from datetime import datetime, timedelta
import pandas as pd
import json
from functools import reduce
import operator

def fix_most_recent(hours_ago=12, nlp_kw= False, summary= False, keywords= False, raw_text= False, debug=True):
  hours_ago_date_time = datetime.now() - timedelta(hours = hours_ago)
  articles = Article.select().where(Article.date > hours_ago_date_time)
  process_article_list(articles, nlp_kw, summary, keywords, raw_text, debug)

# params override filters that prevent needlessly reprocessing data
def extract_missing_features(hours_ago=48, nlp_kw=False, summary= False, keywords= False, raw_text= False, debug=True):
  hours_ago_date_time = datetime.now() - timedelta(hours = hours_ago)
  articles = Article.select().where((Article.date > hours_ago_date_time) & ((Article.nlp_kw.is_null(not nlp_kw)) | (Article.summary.is_null(not False)) | (Article.keywords.is_null(not False))) & (Article.raw_text.is_null(raw_text)))
  process_article_list(articles, True, True, keywords, raw_text, debug)

def process_article_list(articles, nlp_kw, summary, keywords, raw_text, debug):
  print(f"ARTICLES ARE THIS MANY: {len(articles)}\n")
  processed = list(map(lambda article: clean_article_data(article, nlp_kw, summary, debug), articles))
  if debug == True:
    mapped_kw = keyword_frequency_map(processed)
    print(mapped_kw)

    relationship_map = map_article_relationships(processed, mapped_kw)
    print(json.dumps(relationship_map, sort_keys=True, indent=2))

    df = pd.DataFrame(data = list(map(lambda x: [x.source, x.url, x.title, x.date, x.id, x.keywords, x.raw_text, x.summary, x.nlp_kw], processed)), columns = ['source', 'url', 'title', 'date', 'id', 'keywords', 'content', 'summary', 'nlp_kw'])

    topic_map = make_topics_map(processed, relationship_map, df)
    mapped_topics = map(lambda tuple: map_topic(tuple[1], df), topic_map.items())
    mapped_topics_list = sorted(list(mapped_topics), key=lambda topic: (len(topic.articles), topic.date), reverse=True)  
    print_topic_map(topic_map, df)

    i = iter(range(len(mapped_topics_list)))
    while (x := next(i, None)) is not None and x < 10:
      mapped_topics_list[x].woof()

def filter(filters):
  # https://stackoverflow.com/questions/53640958/combining-optional-passed-query-filters-in-peewee
  # filters = {'nlp_kw':'is_null(True)','summary':'is_null(False)'}
  expression_list = [getattr(Article, field) == value for field, value in filters.items()]
  anded_expr = reduce(operator.and_, expression_list)
  ored_expr = reduce(operator.or_, expression_list)
  return {'or': ored_expr, 'and': anded_expr }

def update_v1_keywords(article, debug=False):
  cleaned = remove_known_junk(article.raw_text, True)
  article.raw_text = cleaned
  keywords, events = keywords_from_text_title(cleaned, article.title)
  article.keywords = keywords
  if debug == True:
    print("AFTER\n")
    print(cleaned)
    print("\nKEYWORDS\n")
    print(keywords)
  return article, events

def update_article_summary(article, debug):
  # TODO: split into nlp_kw and nlp summary
  try:
    summary = summarize_nlp(article.raw_text, debug)
  except IndexError as e:
    print(f"unable to transform ID: {article.id}, trying NLTK")
    summary = summarize_nltk(article.raw_text, 12)
  article.summary = summary
  article.nlp_kw, events = keywords_from_text_title(article.summary, article.title)
  return article, events


def clean_article_data(article, kw=False, summ=False, debug=False):
  top_events = []
  print(f"ARTICLE_ID: {article.id}")
  if debug == True:
    print("RAW_TEXT - BEFORE\n")
    print(article.raw_text)
  if kw is True:
    article, events = update_v1_keywords(article, debug)
    top_events.append(events)
  if summ is True:
    article, events = update_article_summary(article, debug)
    top_events.append(events)
  article.save()
  return article