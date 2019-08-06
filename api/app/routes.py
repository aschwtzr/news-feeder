from app import app
import util.news_formatter
from util.api import get_feed_for, get_rss_sources
from flask import request
from flask import jsonify
from collections import defaultdict

import datetime

news_sources = ["google", "bbc", "dw", "guardian"]

@app.route('/')
@app.route('/index')
@app.route('/index')
def index():
  ret = {'ok': True}
  return jsonify(ret)

# news briefing with smmry API
@app.route('/briefing', methods=(['GET']))
def get_briefing():
  try: source = request.args.get('source')
  except NameError: source = None

  if source is None:
    get_briefing() 

# rss feeds with local python summaries
@app.route('/headlines', methods=(['GET']))
def get_headlines():
  req_source = request.args.get('source')
  req_limit = request.args.get('limit')
  if req_limit is None:
    limit = 4
  else: limit = int(req_limit)

  ret = defaultdict(list)
  if req_source is None:
    for source in news_sources:
      # feed = get_feed_for(item)
      headlines = util.news_formatter.get_headlines_for_source(source, limit)
      ret["headlines"].append(headlines)
  else:
    headlines = util.news_formatter.get_headlines_for_source(req_source, limit)
    ret["headlines"].append(headlines)
  ret["ok"] = True
  return jsonify(ret)

# list of available news sources
@app.route('/sources', methods=(['GET']))
def get_sources():
  sources = get_rss_sources()
  ret = { 'ok': True, 'sources': sources }
  return jsonify(ret)

# get smmry summaries for news sources
@app.route('/smmry', methods=(['GET']))
def get_summaries():
  req_source = request.args.get('source')
  req_limit = request.args.get('limit')
  if req_limit is None:
    limit = 4
  else: limit = int(req_limit)

  ret = defaultdict(list)
  if req_source is None:
    ret['ok'] = False
    ret['error'] = 'Currently need at least one source for news summaries.'
    return jsonify(ret)
  else:
    # feed = get_feed_for(req_source)
    headlines = util.news_formatter.get_summaries_from_source(req_source, limit)
    ret["headlines"].append(headlines)
  ret["ok"] = True
  print(ret)
  return jsonify(ret)
