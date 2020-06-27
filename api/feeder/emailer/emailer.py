import yagmail
import os
import logging
from feeder.common.source import google, guardian, bbc, reuters, dw
from collections import defaultdict
from feeder.util.time_tools import timestamp_string

password = os.environ.get('EMAIL_PASSWORD')
email = os.environ.get('EMAIL_ADDRESS')

def run_digest (users):
  sources = load_sources()
  topic_keywords = map_keywords(sources)
  for user in users:
    logging.info(f"emailing {user['email']}")
    body = email_body_for_user(user, sources, topic_keywords)
    yagmail.SMTP(email, password).send(
      to=user['email'],
      subject="Here is your daily news briefing", 
      contents=body)
    logging.info(f"email sent at {timestamp_string()}")

def fancy_source (key):
  fancies = {
    'google': 'Google News',
    'guardian': 'The Guardian',
    'bbc': 'BBC News',
    'reuters': 'Reuters',
    'dw': 'Deutsche Welle'
  }
  return fancies[key]

def email_body_for_user (user, sources, keywords):
  contents = ['<body>']

  for source in user['sources']:
    head = fancy_source(source)
    results = sources[source]
    contents.append(f'<h2 style="color: #33658A; font-weight: 800; margin: 0;">{head}</h2>')
    for index, topic in enumerate(results):
      contents.append(f'<strong style="font-weight=500;"> keywords: {topic.keywords}</strong><br>')
      print(len(topic.articles))
      for article in topic.articles:
        contents.append(f"<a href='{article.url}'><strong>{article.title}</strong></a><br>")
        contents.append(f"<strong>{article.source}</strong>")
        contents.append(f"<em>{article.date}</em><br>")
        contents.append(f"<div>{article.brief}<div> {'<br>' if len(article.brief) > 0 else '' } ")
        contents.append("<br>")    
      if index >= user['limit'] - 1:
        break
    contents.append("<br><br>")

  if user['experimental'] == True:
    for key, value in keywords.items():
      contents.append(f"{key}: {len(value)}")
      if len(value) < 3:
        continue

  return contents


def load_sources ():
  sources = {}
  sources['google'] = google.get_feed_articles(20)
  sources['guardian'] = guardian.get_feed_articles(20)
  sources['bbc'] = bbc.get_feed_articles(20)
  sources['dw'] = dw.get_feed_articles(20)
  return sources

def map_keywords (sources):
  topic_keywords = defaultdict(list)
  for stream in sources.values():
    for topic in stream:
      for keyword in topic.keywords:
        topic_keywords[keyword.lower()].extend(topic.articles)
  sorted_keywords = {k: v for k, v in sorted(topic_keywords.items(), key=lambda item: len(item[1]), reverse=True)}
  # for key, value in topic_keywords.items():
  #   print(f"{key}: {len(value)}")
  return sorted_keywords
