import psycopg2, psycopg2.extras
import os

def get_db_conn():
  conn = psycopg2.connect(
    dbname=os.environ.get("DB_NAME"), 
    user=os.environ.get("DB_USER"), 
    password=os.environ.get("DB_PASS"), 
    host=os.environ.get("DB_HOST")
  )
  return conn

# fetch list of articles from DB.
# TODO: finish setting up fitlers
def fetch_articles(filters):
  print(filters)
  conn = get_db_conn()
  hours_start = filters.get('hours_start', 18)
  hours_end = filters.get('hours_end', 0)
  source = filters.get('source')
  # source = 
  # source_string = f"and source ilike {filters['source']}" if filters['source'] is not None else ''
  # title_string = f"and title ilike {filters['title']}" if filters['title'] is not None else ''
  # kw_string = f"and keywords @> {filters['keywords']}" if filters['keywords'] is not None else ''
  # smr_string = f"and smr_keywords @> {filters['keywords']}" if filters['keywords'] is not None else ''
  ARTICLE_SQL = f"""
    select 
      source, 
      url, 
      title, 
      smr_summary, 
      date,
      keywords, 
      smr_keywords, 
      id, 
      keywords || smr_keywords as grouped_keywords,
      content 
    from articles
    where date > now() - interval '{hours_start} hours'
    and date < now() - interval '{hours_end} hours'
    {'' if source is None else f"and feed_source in ({source})"}
    ;
  """
  print(ARTICLE_SQL)
  cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
  cur.execute(ARTICLE_SQL)
  articles = cur.fetchall()
  cur.close()
  conn.close()
  print(f"*** FETCHED {len(articles)} ROWS FROM THE DATABASE")
  return articles

def fetch_sources(filters=None):
  conn = get_db_conn()
  SOURCES_SQL = f"""
    select
      id,
      name,
      key,
      category,
      active,
      feed_extractor_key,
      text_parser_key,
      custom_keywords,
      url,
      default_limit
    from sources
    where type = 'rss'
    and active is true
  """
  cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
  cur.execute(SOURCES_SQL)
  sources = cur.fetchall()
  cur.close()
  conn.close()
  return sources

def article_exists(source, url):
  conn = get_db_conn()
  cur = conn.cursor()
  exists_query = """
    select exists (
        select 1
        from articles
        where source = %s
        and url = %s
    )"""
  cur.execute(exists_query, (source, url))
  res = cur.fetchone()[0]
  cur.close()
  conn.close()
  return res

def insert_article(description, keywords, title, url, source, date, brief):
  conn = get_db_conn()
  cur = conn.cursor()
  print(f"Adding {title} - {source} via {description}")
  sql = """
    insert into articles 
    (feed_source, keywords, title, url, source, date, content)
    values (%s, %s, %s, %s, %s, %s, %s)
  """ 
  data = (description, keywords, title, url, source, date, brief)
  
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

def upsert_article(keywords, title, url, source, date, brief, id):
  conn = get_db_conn()
  cur = conn.cursor()
  print(f"Adding {title} - {source} via {feed_source}")
  sql = """
    insert into articles 
    (feed_source, keywords, title, url, source, date, content)
    values (%s, %s, %s, %s, %s, %s, %s)
    where id = %s
  """ 
  data = (keywords, title, url, source, date, brief, id)
  
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