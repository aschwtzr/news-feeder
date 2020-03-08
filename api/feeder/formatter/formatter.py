import logging
from feeder.common.article import Article
from gensim.summarization import keywords
import re
from datetime import date


# get keywords from list of strings
def keywords_from_strings (string_list):
  word_count = 8 if len(string_list) >= 2 else len(string_list) * 3
  lemmatize = True if len(string_list) > 1 else False
  reduced = ". ".join(list(map(lambda headline: remove_publication_after_pipe(headline), string_list)))

  # TODO: Fix filters
  filters = ['-SBJ', '-LOC']
  print(string_list)
  try:
    keywords_from_text = keywords(reduced, split=True, words=word_count, lemmatize=True, pos_filter=[], scores=False)
    sentence = ''
    for pair in keywords_from_text:
      sentence += f'{pair} '
    print(keywords_from_text)
    return sentence
  except:
    logging.warning('error extracting keywords')
    print("couldn't get keywords")
    return string_list[0] #.split(' ')

def remove_publication_after_pipe (string):
  formatted = re.sub('(( \| )|( \- )).*', '', string)
  return formatted
