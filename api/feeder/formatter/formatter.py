from api.feeder.common.article import Article
from gensim.summarization import keywords
import re

def article_from_google_item (article, date):
  a = article.find('a')
  title = a.get_text()
  source = article.find('font').get_text()
  article = Article(source, a['href'], title, '', date)
  return article

# get keywords from list of strings
def keywords_from_strings (string_list):
  word_count = 6 if len(string_list) >= 3 else len(string_list) * 2
  lemmatize = True if len(string_list) > 1 else False
  # print(list(map(lambda headline: remove_publication_after_pipe(headline), string_list)))
  # print([remove_publication_after_pipe(headline) for headline in string_list])
  reduced = ". ".join(list(map(lambda headline: remove_publication_after_pipe(headline), string_list)))
  # print(reduced)
  # filters = ['-LOC', '-OBJ', 'SBJ', 'JJ']
  INCLUDING_FILTER = ['NN', 'NP']
  EXCLUDING_FILTER = []
  from gensim.summarization.textcleaner import HAS_PATTERN
  from gensim.utils import has_pattern

  assert HAS_PATTERN
  assert has_pattern()
  try:
    keywords_from_text = keywords(reduced, split=True, words=word_count, lemmatize=False, pos_filter=INCLUDING_FILTER)
    # print(keywords_from_text)
    sentence = ''
    for pair in keywords_from_text:
      sentence += f'{pair} '
    return sentence
  except:
    # print(string_list)
    # print('error extracting keywords')
    return string_list[0]

def remove_publication_after_pipe (string):
  # print(string)
  # print(re.sub('(( \| )|( \- )).*', '', string))
  return re.sub('(( \| )|( \– )).*', '', string)
