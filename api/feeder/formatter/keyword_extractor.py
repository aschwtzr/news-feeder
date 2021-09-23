import logging
from feeder.common.article import Article
from gensim.summarization import keywords
import re
from datetime import date
from functools import reduce
from nltk.corpus import stopwords
import nltk

def keywords_from_article (article):
  # strategy: 
  # 1. attempt to extract keywords from headline
  # 2. attempt to extract keywords from summary
  # 3. split a headline with split(' ')
  output = keywords_from_string(article.title)
  if len(output) < 2 and article.brief is not None:
    output = keywords_from_string(f"{article.title} {article.brief}")
  if len(output) < 2:
    output = word_ranker(f"{article.title} {article.brief}")
  return output
  

# get keywords from list of strings
def keywords_from_string_list (string_list):
  reduced = " ".join(list(map(lambda headline: remove_publication_after_pipe(headline), string_list)))
  gensim_keywords = []
  try:
    gensim_keywords = keywords_from_string(reduced)
  except:
    logging.warning("Failed to parse keywords from concatenated strings.")
  try:
    gensim_keywords = keywords_from_string(string_list[0])
  except:
    logging.warning("Failed to parse keywords from string list or headline.")
    logging.warning(string_list)
  return gensim_keywords

def keywords_from_string (input):
  keywords_from_text = []
  sanitized = sanitize_string(input)
  try:
    keywords_from_text = keywords(sanitized, split=True, words=4, lemmatize=True, scores=False)
    # keywords_from_text = keywords(sanitize_string(input), split=True, words=4, lemmatize=True, pos_filter=('NN', 'NNS', 'NNPS', 'VBN', 'VBD', 'VB', '-OBJ', '-SBJ'), scores=False)
  except IndexError as e:
    logging.warning(f"ERROR: {repr(e)} STRING: {sanitized}")
    # logging.exception('Error extracting keywords. Lowering lemmas and word count')
  except RuntimeError as e:
    logging.warning(f"ERROR: {repr(e)} STRING: {sanitized}")
    # logging.exception('Error extracting keywords. Lowering lemmas and word count')
  try:
    keywords_from_text = keywords(sanitized, split=True, words=3, lemmatize=False, scores=False)
  except:
    logging.warning(f"Final attempt. STRING: {sanitized}")
  try:
    keywords_from_text = keywords(sanitized, split=True, words=2, lemmatize=False, scores=False)
  except:
    logging.warning("All keyword extractions failed.")
  # gensim doesn't always split cleanly
  if len(keywords_from_text) < 1:
    return []                       

  properly_split = reduce((lambda split_list, keyword: split_extend(split_list, keyword)), keywords_from_text, [])
  return properly_split

def split_extend (input_list, input_string):
  split = input_string.split(' ')
  input_list.extend(split)
  return input_list

def remove_publication_after_pipe (string):
  formatted = re.sub(r'(( \| )|( \- )).*', '', string)
  return formatted

def sanitize_string (string):
  depubbed = remove_publication_after_pipe(string)
  parsed = re.sub(r'(:)|(\'s)', '', depubbed)
  filtered = filter_stopwords_from_title(parsed)
  return filtered

def clean_and_reduce_string_list (string_list):
  reduced = " ".join(list(map(lambda headline: remove_publication_after_pipe(headline), string_list)))
  filtered = filter_stopwords_from_title(reduced)
  return filtered

def filter_stopwords_from_title (string):
  # https://gist.github.com/sebleier/554280
  # https://python.gotrained.com/text-classification-with-pandas-scikit/
  filtered_keywords = []
  # for review in string:
  review = string.lower() #Convert to lower-case words
  raw_word_tokens = re.findall(r'(?:\w+)', review,flags = re.UNICODE) #remove pontuaction
  filtered_keywords = [w for w in raw_word_tokens if not w in stopwords.words('english')] # do not add stop words
  return ' '.join(filtered_keywords) #return all tokens

def process_and_tokenize_string (string):
    # https://stackabuse.com/implementing-word2vec-with-gensim-library-in-python/
    processed = string.lower()
    processed = re.sub('[^a-zA-Z]', ' ', processed)
    processed = re.sub(r'\s+', ' ', processed)
    all_sentences = nltk.sent_tokenize(processed)
    all_words = [nltk.word_tokenize(sent) for sent in all_sentences]
    for i in range(len(all_words)):
        all_words[i] = [w for w in all_words[i] if w not in stopwords.words('english')]
    return all_words

def filter_stopwords_from_keywords (kw_list):
  output_keywords = []
  for word in kw_list:
    review = word.lower()
    if review not in stopwords.words('english'):
      output_keywords.append(review)
  return output_keywords

def word_ranker (incoming):
  if type(incoming) is list:
    incoming = clean_and_reduce_string_list(incoming)
  mapped = {}
  sanitized = sanitize_string(incoming)
  minus_pub = remove_publication_after_pipe(sanitized)
  parsed = minus_pub.lower().split(' ')
  for key in parsed:
    if key in mapped.keys():
      mapped[key] += 1
    else:
      mapped[key] = 1
  sorted_keywords = {k: v for k, v in sorted(mapped.items(), key=lambda item: item[1], reverse=True)}
  filtered = filter(lambda pair: pair[1] >= 2 and len(pair[0]) >= 3, sorted_keywords.items())
  return list(map(lambda pair: pair[0], list(filtered)))