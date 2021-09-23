import psycopg2
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
  cur = conn.cursor()
  cur.execute(ARTICLE_SQL)
  articles = cur.fetchall()
  cur.close()
  conn.close()
  print(f"*** FETCHED {len(articles)} ROWS FROM THE DATABASE")
  return articles