from feeder.formatter.content_fixer import extract_nlp_summ_kw, fix_most_recent, extract_missing_features, fetch_articles_missing
from feeder.models.article import Article
from feeder.util.time_tools import print_timestamp, date_time_string
import time
startTime = time.time()

while True:
  hours_ago_date_time = date_time_string(48)
  try:
    article = (Article
              .select()
              .where((Article.date > hours_ago_date_time) & ((Article.keywords.is_null(True)) | (Article.paragraphs.is_null(True))))
              .order_by(Article.date.desc())
              .get())
    print_timestamp(f"FETCHED ARTICLE {article.id}")
    extract_missing_features([article],keywords=True, paragraphs=True, nlp_kw=True, summary=True, debug=False)
    extract_missing_features([article],keywords=True, nlp_kw=True, summary=True, debug=False)
  except:
    try:
      article = (Article
            .select()
            .where((Article.date > hours_ago_date_time) & ((Article.nlp_kw.is_null(True)) | (Article.summary.is_null(True))))
            .order_by(Article.date.desc())
            .get())
      print_timestamp(f"FETCHED ARTICLE {article.id}")
      extract_missing_features([article],keywords=True, nlp_kw=True, summary=True, debug=False)
    except:
      print_timestamp("All caught up, congrats!")
      time.sleep(5)
  executionTime = (time.time() - startTime)
  print_timestamp(f"FINISHED THE LOOP DEE LOOP {executionTime}")
