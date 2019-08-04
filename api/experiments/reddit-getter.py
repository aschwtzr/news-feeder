from datetime import date, timedelta
import praw
import pprint
import requests
from bs4 import BeautifulSoup
from gensim.summarization import keywords
from gensim.summarization.summarizer import summarize
from newsapi import NewsApiClient
import json
import os


wiki_summaries = []
search_terms = []
top_headlines = []

def get_reddit():
  key = os.environ.get('REDDIT_KEY')
  client = os.environ.get('REDDIT_CLIENT')
  reddit = praw.Reddit(client_id=client,
                        client_secret=key,
                        grant_type='client_credentials',
                        user_agent='mytestscript/1.0') 
  hot = reddit.subreddit('all').hot(limit=500)
  top = reddit.subreddit('all').top('day')
  # print('HOT')
  filtered = [s for s in top if not s.is_self]
  pprint.pprint([(s.url, s.title, s.subreddit) for s in filtered])
  # print('TOP')
  # pprint.pprint([(s.score, s.title) for s in top])

def get_wiki_news():
  yesterday = date.today() - timedelta(days=1)
  req = requests.get('https://en.wikipedia.org/api/rest_v1/page/html/Portal%3ACurrent_Events')
  soup = BeautifulSoup(req.text, 'html.parser')
  content = soup.find(id=yesterday.strftime('%Y_%B_%-d')).find_all('li')
  print(yesterday.strftime('%Y_%B_%-d'))
  news_bullets = [topic.get_text() for topic in content]
  global wiki_summaries
  wiki_summaries = news_bullets

  for news_item in news_bullets:
    kwrds = keywords(news_item, ratio=.2)
    search_string = ''
    for word in kwrds:
      search_string += word

    search_terms.append(search_string.replace("\n", " "))

def get_headlines():
  key=os.environ.get('NEWS_API_KEY')
  newsapi = NewsApiClient(api_key=key)
  for search_term in search_terms:
    print('SEARCH TERM: ' + search_term)
    top_headlines = newsapi.get_top_headlines(q='"' + search_term + '"',
                                          language='en')
    print('HEADLINES')
    print(top_headlines)
    if top_headlines['articles']:
      # print(f'search term: {search_term}')
      for article in top_headlines['articles']:
        print('ARTICLE')
        print(article['title'])

def getBingHeadlines():
  for term in search_terms:
    key = os.environ.get('BING_KEY')
    subscription_key = key
    search_term = '"' + term + '"'
    search_url = "https://api.cognitive.microsoft.com/bing/v7.0/news/search"
    headers = {"Ocp-Apim-Subscription-Key" : subscription_key}
    params  = {"q": search_term, "textDecorations": True, "textFormat": "HTML"}
    response = requests.get(search_url, headers=headers, params=params)
    response.raise_for_status()
    search_results = response.json()
    print(search_results)

get_wiki_news()
# get_headlines()
print("++++++ALL SEARCH TERMS++++++")
print(search_terms)
getBingHeadlines()
# print(top_headlines)
# print("++++++ENUMERATING++++++")
# for index, news_item in enumerate(wiki_summaries):
#   print(news_item)
#   print(search_terms[index])
