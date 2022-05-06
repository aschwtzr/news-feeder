from datetime import datetime
import os
import yagmail

import pandas as pd

import feeder.formatter.topic_mapper as topic_mapper
from feeder.util.api import summarize_text
from content_fixer import fix_most_recent


def build_email_body (topics, counts, dev_mode = False):
  contents = ['<body>']
  contents.append(f'<h2 style="color: #33658A; font-weight: 800px; margin: 0;">Hello from the newly Artificially Intelligent News Feeder</h2><br>')
  contents.append(f"<div>I scanned {counts['articles']} articles into {counts['topics']} news items. Here's the latest news:</div><br>")
  other_news = False
  for topic in topics:
    long_string = ''
    articles_html = []
    if len(topic.articles) > 2:
      contents.append(f'<strong style="font-size: 15px;">{topic.headline}</strong>')
      if topic.keywords is not None:
        contents.append(f"<br><div style=''>KW: {topic.keywords}</div>")
      if topic.nlp_kw is not None:
        contents.append(f"<br><div style=''>NLP KW: {topic.nlp_kw}</div>")
      if topic.summary is not None:
        contents.append(f"<br><div style=''>SUMMARY: {topic.summary}</div>")
      contents.append("<br>")
        
      
      article_len = len(topic.articles)
      i = iter(range(article_len))
      while (x := next(i, None)) is not None and x < 3:
        article = topic.articles[x]
        articles_html.append(f"<a href='{article.url}'><strong>{article.source} {article.title}</strong></a><br>")
        articles_html.append(f"<em>{article.date.strftime('%m/%d/%Y, %H:%M')}</em><br>")
        articles_html.append(f"<div style=''>{article.summary}</div>")
        articles_html.append(f"<div style='{'' if dev_mode is True else 'display: none;'}'>{article.keywords}</div>{'<br>' if dev_mode is True else ''}")
      if article_len > 3:
        for x in range(article_len - 4):
          article = topic.articles[x]
          articles_html.append(f"<a href='{article.url}'><strong>{article.title}</strong></a><br>")

        # if article.raw_text is not None:
        # articles_html.append(f"<div>{'. '.join(list(article.raw_text.split('. '))[:2])}<div> {'<br>' if len(article.raw_text) > 0 else '' } ")
        # long_string += article.raw_text
   
      # topic_sum = summarize_text(long_string, sentences)
      contents.append('<strong> *** Articles *** </strong>')
      contents += articles_html
    else:
      article = topic.articles[0]
      if other_news is False:
        contents.append('<br><br><h4>Other News </h4>')
        other_news = True
      contents.append(f"<strong style='font-size:15px; font-weight: bold!important'><a href='{article.url}'>{article.source} {article.title}</a></strong>")
      contents.append(f"<div style=''>{article.keywords}</div><br>")
      
      # articles_html.append(f"<strong></strong>")
      # articles_html.append(f"<em>{article.date.strftime('%m/%d/%Y, %H:%M')}</em><br>")
      # articles_html.append(f'<div>{topic.articles[0].raw_text}</div>')
      # contents += articles_html
    contents.append("###<br>")
    contents.append("<br>")
  contents.append('</body>')
  return contents


start = datetime.now()
st_timestamp = start.strftime('%m/%d/%Y, %H:%M')
hours_ago = 16

print(f"""
*****************************************  
*****************************************  
  START SENDING AT {st_timestamp}
  GOING BACK {hours_ago} HOURS
*****************************************  
*****************************************  
""")

# fix_most_recent(hours_ago)
res = topic_mapper.get_summary(hours_ago)
# body = build_email_body(res['topics'], res['counts'])
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

now = datetime.now()
timestamp = now.strftime('%m/%d/%Y, %H:%M')

print(f"""
*****************************************  
*****************************************  
  SENDING NEWS AT {timestamp}
*****************************************  
*****************************************  
""")

# users = all_users if os.environ.get("PROD") is True else users_dev
users = users_dev
for user in users:
  yagmail.SMTP(os.environ.get('EMAIL_ADDRESS'), os.environ.get('EMAIL_PASSWORD')).send(
    to=user['email'],
    subject=f"Your {timestamp} News Briefing",
    contents=user['body']
  )
  print(f"EMAIL SENT TO {user['email']}")
