import datetime
import os
import yagmail

import pandas as pd

import feeder.formatter.topic_mapper as topic_mapper
from feeder.util.api import summarize_text


def build_email_body (topics, counts, dev_mode = False):
  contents = ['<body>']
  contents.append(f'<h2 style="color: #33658A; font-weight: 800px; margin: 0;">Hello from the newly Artificially Intelligent News Feeder</h2><br>')
  contents.append(f"<div>I scanned {counts['articles']} articles into {counts['topics']} news items. Here's the latest news:</div><br>")
  other_news = False
  for topic in topics:
    long_string = ''
    articles_html = []
    if len(topic.articles) > 1:
      headline = topic_mapper.summarize('. '.join(list(map(lambda x: x.title, topic.articles))), 1)
      contents.append(f'<strong style="font-size: 15px;">{headline}</strong><br>')
      contents.append(f"<div style='{'' if dev_mode is True else 'display: none;'}'>{topic.keywords}</div>{'<br>' if dev_mode is True else ''}")
      for article in topic.articles:
        articles_html.append(f"<a href='{article.url}'><strong>{article.title}</strong></a><br>")
        articles_html.append(f"<strong>{article.source}</strong>")
        articles_html.append(f"<em>{article.date.strftime('%m/%d/%Y, %H:%M')}</em><br>")
        articles_html.append(f"<div style='{'' if dev_mode is True else 'display: none;'}'>{article.keywords}</div>{'<br>' if dev_mode is True else ''}")
        # if article.brief is not None:
        articles_html.append(f"<div>{'. '.join(list(article.brief.split('. '))[:2])}<div> {'<br>' if len(article.brief) > 0 else '' } ")
        long_string += article.brief
      if len(topic.articles) > 10:
        # sentences = 10
        sentences = 4
      elif len(topic.articles) > 6:
        # sentences = 8
        sentences = 3
      elif len(topic.articles) > 3:
        # sentences = 6
        sentences = 2
      else:
        # sentences = 4
        sentences = 1
      long_string.rstrip()
      print(long_string)
      # if len(long_string) > 0:
      topic_sum = topic_mapper.summarize(long_string, sentences)
      # topic_sum = summarize_text(long_string, sentences)
      contents.append(f'<div>{topic_sum}</div>')
      contents.append('<br>')
      contents.append('<strong> *** Articles *** </strong>')
      contents += articles_html
    else:
      article = topic.articles[0]
      if other_news is False:
        contents.append('<br><br><h4>Other News </h4>')
        other_news = True
      contents.append(f"<strong style='font-size:15px; font-weight: bold!important'><a href='{article.url}'>{article.title}</a></strong>")
      articles_html.append(f"<strong>{article.source}</strong>")
      articles_html.append(f"<em>{article.date.strftime('%m/%d/%Y, %H:%M')}</em><br>")
      articles_html.append(f"<div style='{'' if dev_mode is True else 'display: none;'}'>{article.keywords}</div>{'<br>' if dev_mode is True else ''}")
      articles_html.append(f'<div>{topic.articles[0].brief}</div>')
      contents += articles_html
    contents.append("###<br>")
    contents.append("<br>")
  contents.append('</body>')
  return contents

res = topic_mapper.get_summary(24)
body = build_email_body(res['topics'], res['counts'])
dev_body = build_email_body(res['topics'], res['counts'], True)

all_users = [
  {
    'email': 'schweitzer.albert@gmail.com',
    'body': dev_body
  },
  {
    'email': 'mansidhamija24@gmail.com',
    'body': dev_body
  },
  {
    'email': 'heschwei@gmail.com',
    'body': dev_body
  },
  {
    'email': 'kerygma01@yahoo.com',
    'body': dev_body
  },
  {
    'email': 'mariselp_1305@yahoo.com',
    'body': dev_body
  }
]

users_dev = [
  {
    'email': 'schweitzer.albert@gmail.com',
    'body': dev_body
  }
]

now = datetime.datetime.now()
timestamp = now.strftime('%m/%d/%Y, %H:%M')

print(f"""
*****************************************  
*****************************************  
  SENDING NEWS AT {timestamp}
*****************************************  
*****************************************  
""")

users = all_users if os.environ.get("PROD") is True else users_dev

for user in users:
  yagmail.SMTP(os.environ.get('EMAIL_ADDRESS'), os.environ.get('EMAIL_PASSWORD')).send(
    to=user['email'],
    subject=f"Your {timestamp} News Briefing",
    contents=user['body']
  )
  print(f"EMAIL SENT TO {user['email']}")
