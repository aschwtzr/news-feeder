import logging
from feeder.common.article import Article
from gensim.summarization import keywords
import re
from datetime import date
from functools import reduce

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
    logging.warning(f"string: {sanitized}")
    logging.warning(repr(e))
    # logging.exception('Error extracting keywords. Lowering lemmas and word count')
  except RuntimeError as e:
    logging.warning(f"string: {sanitized}")
    logging.warning(repr(e))
    # logging.exception('Error extracting keywords. Lowering lemmas and word count')
  try:
    keywords_from_text = keywords(sanitized, split=True, words=3, lemmatize=False, scores=False)
  except:
    # logging.exception('Failed second attempt at extracting keywords.')
    # logging.warning(f"string: {sanitized}")
    logging.warning("Final attempt.")
  try:
    keywords_from_text = keywords(sanitized, split=True, words=3, lemmatize=False, scores=False)
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
  parsed = re.sub(r'(:)|(\'s)', '', string)
  formatted = parsed.lower()
  return formatted

def clean_and_reduce_string_list (string_list):
  reduced = " ".join(list(map(lambda headline: remove_publication_after_pipe(headline), string_list)))
  return reduced

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