from flask import Blueprint, render_template
from flask import current_app as app
import util.news_formatter
import util.feed_getters
from util.api import get_feed_for, list_rss_sources
from flask import request
from flask import jsonify
# import feeder.common.source
from feeder.common.source import google, guardian, bbc, reuters, dw
from collections import defaultdict
from util import firebase
# from feeder.test import runrun

# import datetime

topics = { 'guardian': guardian, 'bbc': bbc, 'reuters': reuters, 'dw': dw, 'google': google  }
default_sources = { 'guardian': guardian, 'bbc': bbc, 'reuters': reuters, 'dw': dw  }

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
  req_limit = (8 if request.args.get('limit') is None else int(request.args.get('limit')))
  
  keywords = defaultdict(int)
  response = defaultdict(list)
  if len(req_sources) == 0:
    for source in topics.values():
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
  else:
    for source in req_sources:
      print('womp womp')
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
  # global default_sources
  sources = firebase.get_default_sources()

  ret = { 'ok': True, 'sources': sources }
  return jsonify(ret)

# # summarize article with smmry API
# @app.route('/smmry', methods=(['GET']))
# def summarize():
#   url = request.args.get('url')
#   if url is None:
#     ret = { 'ok': False, 'error': 'Must provide URL for summarization' }
#   else:
#       summary = util.news_formatter.summary_from_url(url)
#       if summary["ok"]:
#         ret = { 'ok': True, 'summary': summary['summary'], 'api_limitation': summary["api_limitation"] }
#       else:
#         ret = { 'ok': False, 'error': summary["error"]}
#   return jsonify(ret)

# # summarize article with smmry API
# @app.route('/gensim-summary', methods=(['post']))
# def gensim():
#   # 1. get request body data as dict
#   # 2. get text content
#   # 3. send to summary function which returns gensim summarized text
#   # 4. return dictionary with summarized text
#   # 5. convert to JSON object for frontend digestion

#   req_data = request.get_json()
#   content = req_data['content']
#   summary = util.news_formatter.gensim_summ_from_list(content)
#   ret = { 'ok': True, 'summary': summary }
#   return jsonify(ret)
