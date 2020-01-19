from bs4 import BeautifulSoup

def parse_description_for_source (description, source):
  parse_func = parsers[source]
  description = parse_func(description)
  return description

def parse_google (article):
  item_soup = BeautifulSoup(article.description.get_text(), "html.parser")

  article = {
    'title': article.title.string,
    'content': item_soup.get_text(),
    'link': article.link.string
  }
  return article

def parse_default (content):
  return content

def parse_guardian (content):
  soup = BeautifulSoup(content, "html.parser")
  content_p_tags = soup.find_all('p')
  text = ''
  for index, p in enumerate(content_p_tags):
    text += p.get_text()
    if index == 0:
      text += '. '

  return text

def parse_reuters (content):
  soup = BeautifulSoup(content, "html.parser")
  return soup.get_text()


def parse_yahoo (content):
  soup = BeautifulSoup(content, "html.parser")
  return soup.get_text()

parsers = {
  'world': parse_default,
  'google': parse_default,
  'default': parse_default,
  'reuters': parse_reuters,
  'bbc': parse_default,
  'guardian': parse_guardian,
  'reddit': parse_default,
  'custom': parse_default,
  'dw': parse_default,
  'yahoo': parse_yahoo,
}
