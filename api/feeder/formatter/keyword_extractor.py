import logging
from feeder.models.article import Article
import yake
import re
from datetime import date
from functools import reduce
from nltk.corpus import stopwords
import nltk

language = "en"
max_ngram_size = 2
deduplication_thresold = 0.9
deduplication_algo = 'seqm' # leve|jaro|seqm
windowSize = 1
large_kw_count = 6
small_kw_count = 6

big_custom_kw = yake.KeywordExtractor(lan=language, n=max_ngram_size, dedupLim=deduplication_thresold, dedupFunc=deduplication_algo, windowsSize=windowSize, top=6, features=None)
small_custom_kw = yake.KeywordExtractor(lan=language, n=max_ngram_size, dedupLim=deduplication_thresold, dedupFunc=deduplication_algo, windowsSize=windowSize, top=4, features=None)

def keywords_from_paragraphs_title (paragraphs, title):
  # chop content to the top third 
  end = len(paragraphs) / 2 if len(paragraphs) >= 10 else len(paragraphs) / 3
  print(f"PARAGRAPHS: {len(paragraphs)}")
  print(f"END P INDEX: {int(end)}")

  top_third = paragraphs[0:int(end)]
  text = '. '.join(paragraphs)
  print(text)
  kw, events = keywords_from_text_title(text, title)
  events.append({
    'operation': 'keywords_from_text_title',
    'input': f"TITLE: {title}\n\n TEXT: {text}",
    'output': kw
  })
  return kw, events

def keywords_from_text_title (text, title, debug=False):
  events = []
  # strategy: 
  # 1. attempt to extract keywords from raw_text
  # 2. attempt to extract keywords from raw_text and title
  # 3. split a headline with split(' ')
  output, events = keywords_from_string(text, events)
  if len(output) < 2 and text is not None:
    output, events = keywords_from_string(f"{title} {text}", events)
  if len(output) < 2:
    output, events = word_ranker(f"{title} {text}", events)
  if debug == True:
    print(output)
  keywords = list(map(lambda kw: kw[0], output))
  return keywords, events

# get keywords from list of titles when body is not enough
# TODO: remove and use single underlying keywords extractor
# 
def keywords_from_title_list (string_list):
  reduced = " ".join(list(map(lambda headline: remove_publication_after_pipe(headline), string_list)))
  kw, events = keywords_from_string(reduced, [])
  return list(map(lambda kw: kw[0], kw)), events

def keywords_from_string (input, events = []):
  keywords_from_text = []
  # sanitized = sanitize_string(input)
  try:
    # print('first try')
    keywords_from_text = big_custom_kw.extract_keywords(input)
    events.append({'input': input, 'output': keywords_from_text, 'operation': 'big_custom_kw'})
    if len(keywords_from_text) >= 5:
      return keywords_from_text, events
  except IndexError as e:
    logging.warning(f"ERROR: {repr(e)} STRING: {input}")
    events.append({'input': input, 'output': repr(e), 'operation': 'big_custom_kw'})
  except RuntimeError as e:
    logging.warning(f"ERROR: {repr(e)} STRING: {input}")
    events.append({'input': input, 'output': repr(e), 'operation': 'big_custom_kw'})
  try:
    # print('second try')
    keywords_from_text, events = small_custom_kw.extract_keywords(input)
    events.append({'input': input, 'output': keywords_from_text, 'operation': 'small_custom_kw'})
    if len(keywords_from_text) >= 4:
      return keywords_from_text, events
  except:
    logging.warning("All keyword extractions failed.")
  return [], events

  if len(keywords_from_text) < 1:
    return [], events                       
  # return keywords_from_text

def word_ranker (incoming, events=[]):
  if type(incoming) is list:
    tmp = incoming
    incoming = clean_and_reduce_string_list(incoming)
    events.append({'input': tmp, 'output': incoming, 'operation': 'clean_and_reduce_string_list'})
  mapped = {}
  sanitized = sanitize_string(incoming)
  # print(events)
  events.append({'input':incoming, 'output': sanitized, 'operation': 'sanitize_string'})

  parsed = sanitized.lower().split(' ')
  for key in parsed:
    if key in mapped.keys():
      mapped[key] += 1
    else:
      mapped[key] = 1
  sorted_keywords = {k: v for k, v in sorted(mapped.items(), key=lambda item: item[1], reverse=True)}
  filtered = filter(lambda pair: pair[1] >= 2 and len(pair[0]) >= 3, sorted_keywords.items())
  events.append({'input': sorted_keywords.items(), 'output': filtered, 'operation': 'filter_and_sort_kw'})
  return list(map(lambda pair: pair, list(filtered))), events

# KEYWORD UTILS FOR CLEANING STRINGS

# remove junk content from article body text
def remove_known_junk(string, keep_keywords=False):
  # print("BEFORE\n")
  # print(string)
  string = re.sub("Take a look at the beta version of dw.com. We're not done yet! Your opinion can help us make it better.", '', string)
  string = re.sub("We use cookies to improve our service for you. You can find more information in our data protection declaration.", '', string)
  string = re.sub("Got a confidential news tip? We want to hear from you.", '', string)
  string = re.sub("By subscribing I accept the terms of use and privacy policy", '', string)
  string = re.sub("Advertisement", '', string)
  string = re.sub(r"(© 2021 Deutsche Welle.*)", '', string)
  string = re.sub(r"1998-2022 Nexstar Media", '', string)
  string = re.sub(r"(Sign up for.*).", '', string)
  string = re.sub(r"(© 2021 CNBC.*)", '', string)
  string = re.sub(r"(\d+ hours ago \(\d+:\d+ \w+\))", '', string)
  string = re.sub(r"(These were the updates on \w+, \w* \d*:*.)", '', string)
  string = re.sub(r"(\\n\\n.*\\n\\n)", '', string)
  string = re.sub(r'© 2022 Deutsche Welle(.*)\n', '', string)
  string = re.sub(r'Privacy Policy(.*)\n', '', string)
  string = re.sub(r'Accessibility Statement(.*)\n', '', string)
  string = re.sub(r'Legal notice(.*)\n', '', string)
  string = re.sub(r'Contact(.*)\n(.*)Mobile version\n', '', string)
  string = re.sub(r'^ADVERTISEMENT ', '', string)
  string = re.sub(r'sdi/wmr (\w*)', '', string)
  string = re.sub(r'\xa0 ', '', string)
  string = re.sub(r'ADVERTISEMENT$', '', string)
  string = re.sub(r'Please enable JS and disable any ad blocker', '', string)
  string = re.sub(r'Edited by: ((\w* )*)\n', '', string)
  string = re.sub(r'View the discussion thread,', '', string)
  string = re.sub(r'Last modified on (\w*) (\d*) (\w*) (\d*) (\d*).(\d*) (\w*)', '', string)
  string = re.sub(r'By (.*), CNN  Updated (.*) (\d*), (\d*)  ', '', string)
  string = re.sub(r'© (.*) BBC. The BBC is not responsible for the content of external sites. Read about our approach to external linking.', '', string)
  string = re.sub(r'Edited by: (.*)\n© 2022 Deutsche Welle |\nPrivacy Policy |\nAccessibility Statement |\nLegal notice |\nContact\n| Mobile version\n', '', string)
  string = re.sub(r'The Hill 1625 K Street, NW Suite 900 Washington DC 20006 | 202-628-8500 tel | 202-628-8503 fax The contents of this site are © 1998 - 2022  Nexstar Media Inc. | All Rights Reserved', '', string)
  string = re.sub(r'\n(.*)contributed to this report. The most important news stories of the day, curated by Post editors and delivered every morning. By signing up you agree to our Terms of Use and Privacy Policy', '', string)
  # string = re.sub(r'(.*)Mobile version\n', '', string)
  string = re.sub(r'(( \| )|( \- )).*', '', string)

  if keep_keywords:
    # headline headline Location: date, year city, country --
    string = re.sub(r'^(.*): (\w* \d+, \d+) (.*)', '', string)
  else:
    string = re.sub(r'^(.*): (\w* \d+, \d+) (.*), (.*) -- ', '', string)
  string = re.sub(r'^By (.*) BBC News website', '', string)
  string = re.sub("This video can not be played", '', string)

  # print("CLEAN\n")
  # print(string)
  return string

def split_extend (input_list, input_string):
  split = input_string.split(' ')
  input_list.extend(split)
  return input_list

def remove_publication_after_pipe (string):
  formatted = re.sub(r'(( \| )|( \- )).*', '', string)
  return formatted

def sanitize_string (string):
  parsed = re.sub(r'(:)|(\'s)', '', string)
  filtered = filter_stopwords_from_string(parsed)
  return filtered

def filter_stopwords_from_string (string):
  # https://gist.github.com/sebleier/554280
  # https://python.gotrained.com/text-classification-with-pandas-scikit/
  review = string.lower() #Convert to lower-case words
  raw_word_tokens = re.findall(r'(?:\w+)', review,flags = re.UNICODE) #remove pontuaction
  filtered_tokens = [w for w in raw_word_tokens if not w in stopwords.words('english')] # do not add stop words
  return ' '.join(filtered_tokens) #return all tokens

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

def clean_and_reduce_string_list (string_list):
  reduced = " ".join(list(map(lambda headline: remove_publication_after_pipe(headline), string_list)))
  filtered = filter_stopwords_from_string(reduced)
  return filtered