from bs4 import BeautifulSoup

def parse_google (description):
  print(description )
  soup = BeautifulSoup(description, "html.parser")
  print('GOOGLE')
  soup.get_text()
  return soup.get_text()

def parse_default (description):
  print(description)
  soup = BeautifulSoup(description, "html.parser")
  print('DEFAULT')
  soup.get_text()
  return soup.get_text()

parsers = {
  'google': parse_google,
  'default': parse_default
}