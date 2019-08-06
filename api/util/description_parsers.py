from bs4 import BeautifulSoup

def parse_description_for_source (description, source):
  parse_func = parsers[source]
  description = parse_func(description)
  return description

def parse_google (article):
  print("ITEM")
  print(article)
  print("SOUP")
  item_soup = BeautifulSoup(article.description.get_text(), "html.parser")
  
  print(item_soup)
  print("TEXT")
  print(item_soup.get_text())
  print("\n\n")

  article = {
    'title': article.title.string,
    'content': item_soup.get_text(),
    'link': article.link.string
  }
  return article

def parse_default (article):
  article = {
    'title': article.title.string,
    'content': article.description.get_text(),
    'link': article.link.string
  }
  return article

parsers = {
  'google': parse_google,
  'default': parse_default,
  'reuters': parse_default,
  'bbc': parse_default,
  'guardian': parse_default,
  'reddit': parse_default,
  'custom': parse_default,
  'dw': parse_default
}

