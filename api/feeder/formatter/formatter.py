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
  word_count = 8 if len(string_list) >= 2 else len(string_list) * 3
  lemmatize = True if len(string_list) > 1 else False
  reduced = ". ".join(list(map(lambda headline: remove_publication_after_pipe(headline), string_list)))
  # print(reduced)
  # TODO: Fix filters
  filters = ['-SBJ', '-LOC']

  try:
    keywords_from_text = keywords(reduced, split=True, words=word_count, lemmatize=True, pos_filter=[], scores=False)
    # print(keywords_from_text)
    sentence = ''
    for pair in keywords_from_text:
      sentence += f'{pair} '
    return sentence
  except:
    # print(string_list)
    # print('error extracting keywords')
    return string_list[0] #.split(' ')

def remove_publication_after_pipe (string):
  # print(string)
  # print(formatted)
  formatted = re.sub('(( \| )|( \- )).*', '', string)
  return formatted
