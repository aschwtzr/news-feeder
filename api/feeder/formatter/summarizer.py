import re
import nltk
from feeder.formatter.keyword_extractor import keywords_from_text_title, remove_known_junk, keywords_from_string
from transformers import pipeline, AutoTokenizer, AutoModelForTokenClassification
import heapq

# ner_pipe = pipeline("ner")
summarizer = pipeline("summarization")
# featurizer = pipeline("feature-extraction")
# tokenizer = AutoTokenizer.from_pretrained("dslim/bert-base-NER")
# model = AutoModelForTokenClassification.from_pretrained("dslim/bert-base-NER")
# pipeline("ner", model=model, tokenizer=tokenizer, aggregation_strategy="max")
# text2textizer = pipeline("text2text-generation")

def summarize_nlp(text, debug=False):
  if debug is True:
    print("\n")
    print(f"SUMMARIZE NLP INPUT: {len(text)}")
    print(text[:300])
  long_text = len(text) > 5000
  text = trim_summarize(text, debug)

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
  text = trim_summarize(text, debug)

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

def trim_summarize(text, debug=False):
  sentences = 32
  while len(text) > 4500:
    text = summarize_nltk(text, sentences, debug)
    if debug is True:
      print(f"Sentences: {sentences}")
      print(f"\nTRIMMED: {len(text)}")
      sentences-=4
  return text

def summarize_nltk(article_text, sentences, debug=False):
  article_text = re.sub(r'\[[0-9]*\]', ' ', article_text)
  article_text = re.sub(r'\s+', ' ', article_text)
  formatted_article_text = re.sub('[^a-zA-Z]', ' ', article_text )
  formatted_article_text = re.sub(r'\s+', ' ', formatted_article_text)
  sentence_list = nltk.sent_tokenize(article_text)
  stopwords = nltk.corpus.stopwords.words('english')

  word_frequencies = {} 
  for word in nltk.word_tokenize(formatted_article_text):
    if word not in stopwords:
      if word not in word_frequencies.keys():
        word_frequencies[word] = 1
      else:
        word_frequencies[word] += 1
  maximum_frequncy = max(word_frequencies.values())

  for word in word_frequencies.keys(): 
    word_frequencies[word] = (word_frequencies[word]/maximum_frequncy)
  sentence_scores = {}
  for sent in sentence_list:
    for word in nltk.word_tokenize(sent.lower()):
      if word in word_frequencies.keys():
        if len(sent.split(' ')) < 30:
          if sent not in sentence_scores.keys():
            sentence_scores[sent] = word_frequencies[word]
          else:
            sentence_scores[sent] += word_frequencies[word]
  summary_sentences = heapq.nlargest(sentences, sentence_scores, key=sentence_scores.get)
  summary = ' '.join(summary_sentences)
  if debug is True:
    print(summary)
  return summary

