import logging
from feeder.common.article import Article
from gensim.summarization import keywords
import re
from datetime import date

# get keywords from list of strings
def keywords_from_string_list (string_list):
  reduced = " ".join(list(map(lambda headline: remove_publication_after_pipe(headline), string_list)))
  try:
    gensim_keywords = keywords_from_string(reduced)
    return gensim_keywords
  except:
    try:
      gensim_keywords = keywords_from_string(string_list[0])
      return gensim_keywords
    except:
      logging.warning("Failed to parse keywords from string list or headline.")
      return string_list[0].split(' ')

def keywords_from_string (input):
  try:
    keywords_from_text = keywords(sanitize_string(input), split=True, words=3 , lemmatize=True, scores=False)
    # keywords_from_text = keywords(sanitize_string(input), split=True, words=4, lemmatize=True, pos_filter=('NN', 'NNS', 'NNPS', 'VBN', 'VBD', 'VB', '-OBJ', '-SBJ'), scores=False)
    return keywords_from_text
  except Exception as e:
    logging.warning('error extracting keywords')
    logging.warning(f"string: {sanitize_string(input)}")
    logging.warning(repr(e))
    return input.split(' ')

def remove_publication_after_pipe (string):
  formatted = re.sub(r'(( \| )|( \- )).*', '', string)
  return formatted

def sanitize_string (string):
  formatted = re.sub(r'(:)', '', string)
  return formatted