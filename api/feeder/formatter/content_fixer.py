
from feeder.formatter.keyword_extractor import keywords_from_text_title, remove_known_junk
is_not_pi3 = True
if is_not_pi3:
  from feeder.formatter.summarizer import summarize_nlp, summarize_nltk
from feeder.formatter.article_formatter import raw_text_from_uri
from feeder.models.article import Article
from feeder.models.source import Source
from feeder.util.time_tools import date_time_string
from datetime import datetime, timedelta
import pandas as pd
import json
from functools import reduce
import operator

def fix_most_recent(hours_ago=12, nlp_kw= False, summary= False, keywords= False, raw_text= False, debug=True):
  articles = fetch_articles_missing(hours_ago=hours_ago, keywords=True, raw_text=True, paragraphs=True, debug=debug)
  process_article_list(articles, nlp_kw, summary, keywords, raw_text, paragraphs, debug)

# Defaults to only fetching articles missing post feed extraction data
def fetch_articles_missing(hours_ago=48, nlp_kw=True, summary=True, keywords=False, raw_text=False, paragraphs=False, debug=True):
  hours_ago_date_time = date_time_string(hours_ago)
  return Article.select().where((Article.date > hours_ago_date_time) & ((Article.nlp_kw.is_null(nlp_kw)) | (Article.summary.is_null(summary)) | (Article.keywords.is_null(keywords)) | (Article.paragraphs.is_null(paragraphs))))

# params override filters that prevent needlessly reprocessing data
def extract_missing_features(articles, nlp_kw=False, summary=False, keywords= False, raw_text=False, paragraphs=False, debug=True):
  process_article_list(articles, nlp_kw, summary, keywords, raw_text, paragraphs, debug)

def process_article_list(articles, nlp_kw, summary, keywords, raw_text, paragraphs, debug):
  print(f"ARTICLES ARE THIS MANY: {len(articles)}\n")
  if paragraphs is True or keywords is True:
    articles = list(map(lambda article: extract_content_kw(article, keywords, paragraphs, debug), articles))
  if nlp_kw is True or summary is True:
    articles = list(map(lambda article: extract_nlp_summ_kw(article, nlp_kw, summary, debug), articles))

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
  if article.paragraphs is not None:
    end = len(article.paragraphs) / 2 if len(article.paragraphs) >= 10 else len(article.paragraphs) / 3
    top_third = article.paragraphs[0:int(end)]
    text = '. '.join(top_third)
  else:
    text = article.raw_text
  try:
    if is_not_pi3:
      summary = summarize_nlp(text, debug)
  except IndexError as e:
    print(f"unable to transform ID: {article.id}, trying NLTK")
    if is_not_pi3:
      summary = summarize_nltk(text, 12)
  article.summary = summary
  nlp_kw, events = keywords_from_text_title(article.summary, article.title)
  article.nlp_kw = nlp_kw
  return article, events

def extract_content_kw(article, body_parser, kw=True, paragraphs=True, debug=False):
  raw_text, paragraphs = raw_text_from_uri(article.url, body_parser)
  article.raw_text = raw_text
  article.paragraphs = paragraphs
  article.save()
  return article

def find_source_id(url):
  if url.find('https://news.google.com/__i'):
    return 1
  if url.find('https://www.bbc.co'):
    return 2
  if url.find('https://www.theguardian.com'):
    return 3
  if url.find('https://www.dw.com'):
    return 4
  if url.find('http://rssfeeds.azcentral.com'):
    return 5

def extract_nlp_summ_kw(article, nlp_kw=True, summ=True, debug=False):
  top_events = []
  print(f"ARTICLE_ID: {article.id}")
  if debug == True:
    print("RAW_TEXT - BEFORE\n")
    print(article.raw_text)
  # if nlp_kw is True:
  #   article, events = update_v1_keywords(article, debug)
  #   top_events.append(events)
  if summ is True:
    article, events = update_article_summary(article, debug)
    top_events.append(events)
  article.save()
  return article