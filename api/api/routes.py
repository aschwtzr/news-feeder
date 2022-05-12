from flask import Blueprint, render_template
from flask import current_app as app
from flask import request
from flask import jsonify
from feeder.models.source import Source
from feeder.models.article import Article
from collections import defaultdict
from feeder.formatter.summarizer import summarize_nltk
from feeder.reader.reader import get_summary
from markupsafe import escape
# import pandas as pd
# from feeder.util import firebase
from feeder.util import time_tools
from feeder.util.db import fetch_articles
# from feeder.test import runrun
from playhouse.flask_utils import get_object_or_404, object_list

# default_sources = { 'guardian': guardian, 'bbc': bbc, 'dw': dw  }
sources = []

# @app.before_request
# def before_request():
#     database.connect()

# @app.after_request
# def after_request(response):
#     database.close()
#     return response

@app.route('/')
@app.route('/health')
def index():
  ret = {'ok': True}
  return jsonify(ret)

@app.after_request
def after_request(response):
    header = response.headers
    header['Access-Control-Allow-Origin'] = '*'
    header['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    header['Access-Control-Allow-Methods'] = 'OPTIONS, HEAD, GET, POST, DELETE, PUT'
    return response

# probably better to rename this feeds
# old
@app.route('/briefings', methods=(['GET']))
def get_headlines():
  req_sources = request.args.getlist('source')
  req_limit = (8 if request.args.get('limit') is None else int(request.args.get('limit')))
  
  response = defaultdict(list)
  if len(req_sources) == 0:
    for source in default_sources.values():
      source_dict = defaultdict(list)
      source_dict['source'] = source.description
      feed_topics = source.get_feed_articles(req_limit)
      for index, topic in enumerate(feed_topics):
        for article in topic.articles:
          formatted = {
            'title': article.title,
            'preview': article.raw_text,
            'url': article.url,
            'source': source.description,
            'date': article.date
          }
          source_dict['articles'].append(formatted)

      response['results'].append(source_dict)
  else:
    for source in req_sources:
      print('womp womp')
  response["ok"] = True
  return jsonify(response)

@app.route('/summaries', methods=(['GET']))
def get_topics_new():
  req_limit = (16 if request.args.get('hours_ago') is None else int(request.args.get('hours_ago')))
  res = get_summary(req_limit)
  results = []
  for topic in res['topics']:
    topic_dict = {
      'keywords': topic.keywords,
      'nlp_keywords': topic.nlp_kw,
      'date': topic.date.strftime('%m/%d/%Y, %H:%M'),
      'articles': [],
    }
    topic_dict['title'] = topic.headline
    for article in topic.articles:
      formatted = {
        'title': article.title,
        'summary': article.summary,
        'raw_text': article.raw_text,
        'url': article.url,
        'source': article.source,
        'date': article.date.strftime('%m/%d/%Y, %H:%M'),
        'keywords': article.keywords,
        'nlp_kw': article.nlp_kw,
        'id': int(article.id)
      }
      topic_dict['articles'].append(formatted)

    topic_dict['topic_summ'] = topic.summary
    results.append(topic_dict)
  source = {
    'description': f"News at {time_tools.timestamp_string()}",
    'topics': results
  }
  response = {
    'ok': True,
    'results': [source],
    'keywords': res['mapped_kw'],
    'counts': res['counts'],
    'topics': results
  }
  return jsonify(response)

@app.route('/topics', methods=(['GET']))
def get_topics():
  req_sources = request.args.getlist('source')
  user_sources = request.args.getlist('user_source')
  req_limit = (8 if request.args.get('limit') is None else int(request.args.get('limit')))
  
  keywords = defaultdict(int)
  response = defaultdict(list)
  mapped_sources = []
  if len(req_sources) > 0:
    # sources = firebase.get_default_sources()
    mapped_keys = list(map(lambda source: sources[source]["key"], req_sources[0].split(',')))
    for key in mapped_keys:
      mapped_sources.append(topics_by_key[key])

  # custom_feeds = firebase.get_custom_feeds()
  if len(user_sources) > 0:
    for key in user_sources[0].split(','):
      config = custom_feeds[key]
      query_string =  "+".join(config['keywords'])
      custom_feed = custom_google_source(query_string, config['description'])
      mapped_sources.append(custom_feed)

  for source in (active_topics if len(mapped_sources) < 1 else mapped_sources):
    source_dict = defaultdict(list)
    source_dict['description'] = source.description
    feed_topics = source.get_feed_articles(req_limit)
    for index, topic in enumerate(feed_topics):
      topic_dict = { 'keywords': topic.keywords, 'articles': [] }
      for keyword in topic.keywords:
        keywords[keyword.lower()] += len(topic.articles)
      for article in topic.articles:
        formatted = {
          'title': article.title,
          'preview': article.raw_text,
          'url': article.url,
          'source': article.source if article.source else source.description,
          'date': article.date
        }
        topic_dict['articles'].append(formatted)
      source_dict['topics'].append(topic_dict)
    response['results'].append(source_dict)

  response["ok"] = True
  response["keywords"] = keywords
  return jsonify(response)

# list of available news sources
@app.route('/articles_dead', methods=(['GET']))
def get_articles_dead():
  print(request.args)
  filters = request.args.to_dict()
  print(request.args.get('source'))
  res = fetch_articles(filters)
  return jsonify(res)

# list of available news sources
@app.route('/sources', methods=(['GET']))
def get_sources():
  # sources = firebase.get_default_sources()
  res = []
  for key in sources.keys():
    source = {}
    source.update(sources[key])
    source.update({"id": key})
    res.append(source)
  ret = { 'ok': True, 'sources': res }
  return jsonify(ret)

@app.route('/custom-feeds', methods=(['GET']))
def get_custom_feeds():
  user_id = request.args.get('id')

# not implemented
@app.route('/create-user', methods=(['POST']))
def create_user():
  user_id = request.args.get('userId')
  name = request.args.get('name')
  email = request.args.get('email')
  firebase.create_user(user_id, name, email)

@app.route('/get-user-profile', methods=(['GET']))
def get_user_profile():
  user_id = request.args.get('user_id')
  profile = firebase.get_user_profile(user_id)
  ret = { 'ok': True, 'profile': profile }
  return jsonify(ret)

@app.route('/articles/<post_id>', methods=(['GET']))
def get_article(post_id):
  row = Article.select().where(Article.id == post_id).dicts()
  if len(row) > 0:
    return jsonify(row[0])
  else:
    return {}

@app.route('/articles', methods=(['GET']))
def get_articles(*kwargs):
  rows = Article.select().order_by(Article.date.desc()).limit(150).dicts()
  articles = []
  for row in rows.iterator():
    articles.append(row)
  return jsonify({'articles': articles})