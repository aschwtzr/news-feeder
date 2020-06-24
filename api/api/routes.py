from flask import Blueprint, render_template
from flask import current_app as app
import util.news_formatter
import util.feed_getters
from util.api import get_feed_for, list_rss_sources
from flask import request
from flask import jsonify
# import feeder.common.source
from feeder.common.source import google, guardian, bbc, dw, active_topics
from collections import defaultdict
from util import firebase
# from feeder.test import runrun

# import datetime

default_sources = { 'guardian': guardian, 'bbc': bbc, 'dw': dw  }
sources = []

@app.route('/')
@app.route('/health')
def index():
  ret = {'ok': True}
  return jsonify(ret)

# probably better to rename this feeds
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

@app.route('/topics', methods=(['GET']))
def get_topics():
  req_sources = request.args.getlist('source')
  # user_sources = request.args.getlist('user_source')
  req_limit = (8 if request.args.get('limit') is None else int(request.args.get('limit')))
  
  keywords = defaultdict(int)
  response = defaultdict(list)
  mapped_sources = []
  if req_sources is not None:
    sources = firebase.get_default_sources()
    print(req_sources)
    print(sources)
    mapped = list(map(lambda source: sources[source], req_sources))

  print(mapped_sources)
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
