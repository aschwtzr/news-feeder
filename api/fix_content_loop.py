from feeder.formatter.content_fixer import extract_nlp_summ_kw, fix_most_recent, extract_missing_features, fetch_articles_missing
from feeder.models.article import Article
from feeder.util.time_tools import print_timestamp, date_time_string
import time

def end(startTime, message):
  executionTime = (time.time() - startTime)
  print_timestamp(f"{message}\n\nEXECUTION TIME {executionTime}")
  time.sleep(5)

while True:
  startTime = time.time()
  hours_ago_date_time = date_time_string(48)
  article = (Article
            .select()
            .where((Article.date > hours_ago_date_time) & (Article.skip_extract == None) & ((Article.keywords.is_null(True)) | (Article.paragraphs.is_null(True))))
            .order_by(Article.date.desc())
            .first())
  
  
  if article is not None:
    print_timestamp(f"1ST FETCHED ARTICLE {article.id}")
    try:
      print("TRYING EXTRACT 1")
      extract_missing_features([article],keywords=True, paragraphs=True, nlp_kw=True, summary=True, debug=True)
      # extract_missing_features([article],keywords=True, nlp_kw=True, summary=True, debug=True)
    except:
      end(startTime, f"Oh shit, an err! Article ID: {article.id}")
  else:
    article = (Article
          .select()
          .where((Article.date > hours_ago_date_time) & (Article.skip_extract == None) & ((Article.nlp_kw.is_null(True)) | (Article.summary.is_null(True))))
          .order_by(Article.date.desc())
          .first())
    if article is not None:
      print_timestamp(f"2ND FETCHED ARTICLE {article.id}")
      try:
        print("TRYING EXTRACT 2")
        extract_missing_features([article],summary=True, debug=True)
      except:
        article.skip_extract = True
        print(article.title)
        article.save()
        print(f"Oh shit, an err! Skipping Extract for Article ID: {article.id}")
    else:
      end(startTime, "All caught up, congrats!")
      continue
  end(startTime, "FINISHED THE LOOP DEE LOOP")