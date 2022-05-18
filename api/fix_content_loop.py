from feeder.formatter.topic_mapper import map_articles
from feeder.formatter.content_fixer import extract_nlp_summ_kw, fix_most_recent, extract_missing_features, fetch_articles_missing
from feeder.models.article import Article
from feeder.util.time_tools import print_timestamp, date_time_string

while True:
  hours_ago_date_time = date_time_string(48)
  article = (Article
            .select()
            .where((Article.date > hours_ago_date_time) & ((Article.keywords.is_null(True)) | (Article.paragraphs.is_null(True))))
            .order_by(Article.date.desc())
            .get())
  if article is not None:
    print_timestamp(f"FETCHED ARTICLE {article.id}")
    extract_missing_features([article],keywords=True, paragraphs=True, nlp_kw=True, summary=True, debug=False)
  else:
    article = (Article
          .select()
          .where((Article.date > hours_ago_date_time) & ((Article.keywords.is_null(True)) | (Article.paragraphs.is_null(True))))
          .order_by(Article.date.desc())
          .get())
    if article is not None:
      print_timestamp(f"FETCHED ARTICLE {article.id}")
      extract_missing_features([article],keywords=True, nlp_kw=True, summary=True, debug=False)
    else:
      print_timestamp("All caught up, congrats!")
  print_timestamp("FINISHED THE LOOP DEE LOOP")
