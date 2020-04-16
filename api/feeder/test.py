from feeder.formatter.debug_parser import print_source_articles
from feeder.emailer.emailer import run_digest

# print_source_articles()

# user settings coming soon! 
albert = {
  'email': 'schweitzer.albert@gmail.com',
  'sources': ['guardian', 'bbc', 'reuters', 'dw', 'google'],
  'experimental': True,
  'keywords': False,
  'debug': True,
  'limit': 8
}

mansi = {
  'email': 'mansidhamija24@gmail.com',
  'sources': ['guardian', 'bbc', 'reuters', 'dw', 'google'],
  'keywords': True,
  'debug': False,
  'limit': 8,
  'experimental': True
}

marisel= {
  'email': 'marisel.schweitzer@gmail.com',
  'sources': ['guardian', 'bbc', 'reuters', 'dw', 'google'],
  'keywords': True,
  'debug': False,
  'limit': 8,
  'experimental': True
}

# users = [albert, mansi, marisel]
users = [albert]
def runrun():
  run_digest(users)