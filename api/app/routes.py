from app import app
import util.news_formatter
import util.feed_getters
from util.api import get_feed_for, list_rss_sources
from flask import request
from flask import jsonify
from collections import defaultdict

import datetime

default_sources = util.api.world_news_feeds

@app.route('/')
@app.route('/index')
def index():
  ret = {'ok': True}
  return jsonify(ret)

# rss feeds with local python summaries
@app.route('/briefings', methods=(['GET']))
def get_headlines():
  req_sources = request.args.getlist('source')
  req_limit = request.args.get('limit')

  if req_limit is None:
    limit = 8
  else: limit = int(req_limit)

  ret = defaultdict(list)
  if len(req_sources) == 0:
    for source in default_sources:
      # feed = get_feed_for(item)
      headlines = util.feed_getters.get_news_from_rss(source, limit)
      ret["results"].append(headlines)
  else:
    for source in req_sources:
      headlines = util.feed_getters.get_news_from_rss(source, limit)
      ret["results"].append(headlines)
  
  ret["ok"] = True
  return jsonify(ret)


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
  sources = list_rss_sources()
  ret = { 'ok': True, 'sources': sources }
  return jsonify(ret)

# summarize article with smmry API
@app.route('/smmry', methods=(['GET']))
def summarize():
  url = request.args.get('url')
  if url is None:
    ret = { 'ok': False, 'error': 'Must provide URL for summarization' }
  else:
      summary = util.news_formatter.summary_from_url(url)
      if summary["ok"]:
        ret = { 'ok': True, 'summary': summary['summary'], 'api_limitation': summary["api_limitation"] }
      else:
        ret = { 'ok': False, 'error': summary["error"]}
  return jsonify(ret)

# summarize article with smmry API
@app.route('/gensim-summary', methods=(['post']))
def gensim():
  # 1. get request body data as dict
  # 2. get text content
  # 3. send to summary function which returns gensim summarized text
  # 4. return dictionary with summarized text
  # 5. convert to JSON object for frontend digestion

  req_data = request.get_json()
  content = req_data['content']
  summary = util.news_formatter.gensim_summ_from_list(content)
  ret = { 'ok': True, 'summary': summary }
  return jsonify(ret)
