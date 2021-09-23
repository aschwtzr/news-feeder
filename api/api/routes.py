from flask import Blueprint, render_template
from flask import current_app as app
import util.news_formatter
import util.feed_getters
from util.api import get_feed_for, list_rss_sources
from flask import request
from flask import jsonify
# import feeder.common.source
from feeder.common.source import google, guardian, bbc, dw, active_topics, topics_by_key, custom_google_source
from collections import defaultdict
from feeder.formatter import topic_mapper
import pandas as pd
from util import firebase
from feeder.util import time_tools
from feeder.util.db import fetch_articles
# from feeder.test import runrun

import datetime

default_sources = { 'guardian': guardian, 'bbc': bbc, 'dw': dw  }
sources = []

@app.route('/')
@app.route('/health')
def index():
  ret = {'ok': True}
  return jsonify(ret)

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
            'preview': article.brief,
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

@app.route('/topics_new', methods=(['GET']))
def get_topics_new():
  req_limit = (18 if request.args.get('hours_ago') is None else int(request.args.get('hours_ago')))
  res = topic_mapper.get_summary(req_limit)
  results = []
  for topic in res['topics']:
    topic_dict = {
      'keywords': topic.keywords,
      'articles': [],
    }
    if len(topic.articles) > 1:
      topic_dict['title'] = topic_mapper.summarize('. '.join(list(map(lambda x: x.title, topic.articles))), 1)
      long_string = ''
      for article in topic.articles:
        formatted = {
          'title': article.title,
          'preview': article.brief,
          'url': article.url,
          'source': article.source,
          'date': article.date.strftime('%m/%d/%Y, %H:%M'),
          'keywords': article.keywords,
          'id': int(article.id)
        }
        topic_dict['articles'].append(formatted)
        long_string += article.brief
      if len(topic.articles) > 10:
        sentences = 10
      elif len(topic.articles) > 6:
        sentences = 8
      elif len(topic.articles) > 3:
        sentences = 6
      else:
        sentences = 4
      long_string.rstrip()
      topic_dict['topic_summ'] = topic_mapper.summarize(long_string, sentences)
    else:
      article = topic.articles[0]
      topic_dict['title'] = article.title
      topic_dict['topic_summ'] = article.brief
      topic_dict['keywords'] = article.keywords
      formatted = {
        'title': article.title,
        'preview': article.brief,
        'url': article.url,
        'source': article.source,
        'date': article.date.strftime('%m/%d/%Y, %H:%M'),
        'keywords': article.keywords,
        'id': int(article.id)
      }
      topic_dict['articles'].append(formatted)
    results.append(topic_dict)
  source = {
    'description': f"News at {time_tools.timestamp_string()}",
    'topics': results
  }
  response = {
    'ok': True,
    'results': [source],
    'keywords': res['mapped_kw'],
    'counts': res['counts']
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
    sources = firebase.get_default_sources()
    mapped_keys = list(map(lambda source: sources[source]["key"], req_sources[0].split(',')))
    for key in mapped_keys:
      mapped_sources.append(topics_by_key[key])

  custom_feeds = firebase.get_custom_feeds()
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
          'preview': article.brief,
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

# get google news summaries 
@app.route('/google-news', methods=(['GET']))
def get_google():
  topic = request.args.get('topic')
  if topic is not None:
    # TODO: custom topics search
    news = util.feed_getters.get_google_world_news_feed(topic = topic)
  else:
    news = util.feed_getters.get_google_world_news_feed()
  
  ret = { 'ok': True, 'news': news }
  return jsonify(ret)

# list of available news sources
@app.route('/articles', methods=(['GET']))
def get_articles():
  print(request.args)
  filters = request.args.to_dict()
  print(request.args.get('source'))
  res = fetch_articles(filters)
  return jsonify(res)

# list of available news sources
@app.route('/sources', methods=(['GET']))
def get_sources():
  sources = firebase.get_default_sources()
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