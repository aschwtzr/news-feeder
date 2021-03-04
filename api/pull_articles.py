# from feeder.emailer.emailer import load_sources
import os
import psycopg2
from feeder.common.source import active_topics, topics_by_key, custom_google_source
from feeder.util.api import get_data_from_uri, get_summary
from re import search
from bs4 import BeautifulSoup
from datetime import datetime

def print_articles_for_sources (sources):
  for (description, topics) in sources.items():
    print(description)
    for index, topic in enumerate(topics):
      print(topic.keywords)
      for article in topic.articles:
        print(article.title)
        print(article.url)
        print(article.source)
        print(article.date)

def get_db_conn():
  conn = psycopg2.connect(
    dbname=os.environ.get("DB_NAME"), 
    user=os.environ.get("DB_USER"), 
    password=os.environ.get("DB_PASS"), 
    host=os.environ.get("DB_HOST")
  )
  return conn

def insert_articles(sources):
  cur = conn.cursor()
  for (description, topics) in sources.items():
    for index, topic in enumerate(topics):
      for article in topic.articles:
        try:
          cur.execute("INSERT INTO articles (feed_source, keywords, title, url, source, date) VALUES (%s, %s, %s, %s, %s, %s)",
          (description, topic.keywords, article.title, article.url, article.source, article.date))
          print(f"Added {article.title} - {article.source}")
        except psycopg2.Error as e:
          error = e.pgerror
          code = e.pgcode
          print(error)
  conn.commit()
  cur.close()


def load_sources (user):
  limit = user['articleLimit'] if 'articleLimit' in user else 20
  sources = {}
  for source in user['email_sources']:
    sources[source.key] = source.get_feed_articles(limit)
  return sources

def update_google_news_urls():
  cur = conn.cursor()
  # cur.execute("SELECT * FROM articles WHERE smr_summary IS NULL;")
  cur.execute("SELECT * FROM articles WHERE smr_summary IS NULL and feed_source = %s;", ('google-world',))
  articles = cur.fetchall()
  for article in articles:
    real_url = extract_url(article[3])
    if real_url == 'error' or search('https://www.youtube.com', real_url):
      # print(f"delete article id = {article[10]} titled {article[2]}")
      cur.execute("DELETE from articles where id = %s", (article[10],))
    else:
      # print(f"INSERT {real_url} where article id = {article[10]}")
      cur.execute("UPDATE articles set url = %s WHERE id = %s", (real_url, 1))
  conn.commit()
  cur.close()

def fetch_one():
  cur = conn.cursor()
  cur.execute("SELECT * FROM articles WHERE smr_summary IS NULL and smr_error is not null;")
  article = cur.fetchone()
  res = get_summary(article[3])
  print(res)
  print(res['summary'])
  print(res['keywords'])
  print(res['character_count'])
  print(res['credits_used'])
  cur.close()

def get_summry_data():
  cur = conn.cursor()
  cur.execute("SELECT * FROM articles WHERE smr_summary IS NULL and smr_error is not null;")
  articles = cur.fetchall()
  for article in articles:
    res = get_summary(article[3])
    if res['ok'] == True:
      cur.execute("""
      UPDATE articles set 
      smr_summary = %s,
      smr_keywords = %s, 
      smr_char_count = %s, 
      smr_credits_used = %s 
      WHERE id = %s
      """, (res['summary'], res['keywords'], res['character_count'], res['credits_used'], article[9]))
    else:
      cur.execute("""
      UPDATE articles set 
      smr_error = %s
      WHERE id = %s
      """, (res['error'], article[9]))
      print(res['error'])
    conn.commit()
  cur.close()

def extract_url(google_url):
  print(f'fetching {google_url}')
  data = get_data_from_uri(google_url)
  soup = BeautifulSoup(data, 'html.parser')
  try:
    print('searching for content in soup')
    message = soup.find(property="og:url").attrs['content']
    return message
  except:
    # print(soup)
    # print(google_url)
    return 'error'

def fetch_rss_feeds(sources):
  now = datetime.now()
  timestamp = now.strftime('%m/%d/%Y, %H:%M:%S')
  
  print(f"""
  *****************************************  
  *****************************************  
    FETCHING NEWS AT {timestamp}
  *****************************************  
  *****************************************  
  """)
  cur = conn.cursor()
  for (description, topics) in sources.items():
    for index, topic in enumerate(topics):
      for article in topic.articles:
        # skip google news articles we can't parse
        if description == 'google-world':
          url = extract_url(article.url)
          if url == 'error' or search('https://www.youtube.com', url):
            continue
        else:
          url = article.url

        # skip existing entries
        exists_query = """
            select exists (
                select 1
                from articles
                where source = %s
                and url = %s
            )"""
        cur.execute(exists_query, (article.source, url))
        if cur.fetchone()[0]:
          continue

        # get paid smmry and build sql
        print(url)
        smr = get_summary(url)
        print(f"Adding {article.title} - {article.source} via {description}")
        if smr['ok'] == True:
          sql = """
          insert into articles 
          (feed_source, keywords, title, url, source, date, smr_summary, smr_keywords, smr_char_count, smr_credits_used)
          values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
          """ 
          data = (description, topic.keywords, article.title, url, article.source, article.date, smr['summary'], smr['keywords'], smr['character_count'], smr['credits_used'])
        else:
          sql = """
            insert into articles 
            (feed_source, keywords, title, url, source, date, smr_error)
            values (%s, %s, %s, %s, %s, %s, %s)
            """ 
          data = (description, topic.keywords, article.title, url, article.source, article.date, smr['error'])
        
        # try insert
        print('try insert')
        print(data)
        try:
          cur.execute(sql, data)
          conn.commit()
        except psycopg2.Error as e:
          error = e.pgerror
          code = e.pgcode
          print(error)
  cur.close()

db_user = {
  'email_sources': active_topics
}

sources = load_sources(db_user)
conn = get_db_conn()
fetch_rss_feeds(sources)
conn.close()
