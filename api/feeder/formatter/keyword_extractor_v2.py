from feeder.formatter.keyword_extractor_v1 import keywords_from_text_title, remove_known_junk, keywords_from_string
from transformers import pipeline

# ner_pipe = pipeline("ner")
summarizer = pipeline("summarization")

def update_article_keywords(article, debug=False):
  cleaned = remove_known_junk(article.raw_text, True)
  article.raw_text = cleaned
  keywords = keywords_from_text_title(cleaned, article.title)
  article.keywords = keywords
  if article.nlp_kw is None: 
    update_article_summary(article, debug)
  if debug == True:
    # print("AFTER\n")
    # print(cleaned)
    print("\nKEYWORDS\n")
    print(keywords)
  return article

def update_article_summary(article, debug):
  try:
    summary = summarize_nlp(article.raw_text, debug)
  except IndexError as e:
    print(f"unable to transform ID: {article.id}, trying NLTK")
    summary = summarize(article.raw_text, 12)
  article.summary = summary
  article.nlp_kw = keywords_from_text_title(article.summary, article.title)

def clean_article_data(article, kw=False, summ=False, debug=False):
  print(f"ARTICLE_ID: {article.id}")
  if debug == True:
    print("BEFORE\n")
    print(article.raw_text)
  if kw is True:
    update_article_keywords(article, debug)
  if summ is True:
    update_article_summary(article, debug)
  article.save()
  return article

def summarize_nlp(text, debug=False):
  if debug is True:
    print("\n")
    print(f"SUMMARIZE NLP INPUT: {len(text)}")
    print(text[:300])
  long_text = len(text) > 5000
  sentences = 30
  while len(text) > 4500:
    text = summarize(text, sentences)
    sentences -= 5
    if debug is True:
      print(f"\nTRIMMED: {len(text)}")

  if debug is True:
    print(f"LEGGO: {len(text)}")
  if long_text is True:
    print(text[:300])
  
  if len(text) < 200:
    return text
  elif len(text) < 400:
    max_length = 100
    min_length = 20
  elif len(text) < 600:
    max_length = 130
    min_length = 30
  elif len(text) < 900:
    max_length = 150
    min_length = 50
  elif len(text) < 1400:
    max_length = 220
    min_length = 150
  elif len(text) < 2200:
    max_length = 180
    min_length = 80
  else:
    max_length = 220
    min_length = 100

  summary = summarizer(text, max_length=max_length, min_length=min_length, do_sample=False)
  if debug is True:
    print(f"\SUMMARY: {len(summary[0]['summary_text'])}")
    print(summary[0]['summary_text'])
  return summary[0]['summary_text']

def small_summarize_nlp(text, debug=False):
  # if debug is True:
  #   print("\n")
  #   print(f"SUMMARIZE NLP INPUT: {len(text)}")
  #   print(text[:300])
  # long_text = len(text) > 5000
  # sentences = 30
  # while len(text) > 4500:
  #   text = summarize(text, sentences)
  #   sentences -= 5
  #   if debug is True:
  #     print(f"\nTRIMMED: {len(text)}")

  if debug is True:
    print(f"LEGGO: {len(text)}")

  if len(text) < 100:
    max_length = 10
    min_length = 5  
  if len(text) < 130:
    max_length = 30
    min_length = 10
  elif len(text) < 200:
    max_length = 60
    min_length = 30
  elif len(text) < 400:
    max_length = 80
    min_length = 40
  elif len(text) < 600:
    max_length = 100
    min_length = 50
  elif len(text) < 900:
    max_length = 120
    min_length = 60
  else:
    max_length = 140
    min_length = 80
  
  summary = summarizer(text, max_length=max_length, min_length=min_length, do_sample=False)
  if debug is True:
    print(f"\SUMMARY: {len(summary[0]['summary_text'])}")
    print(summary[0]['summary_text'])
  return summary[0]['summary_text']