# interface with external APIs
import time
import requests
import os

def get (uri):
  results = requests.get(uri)
  return results.text

def get_summary (uri):
  key = os.environ.get('SUMMRY_KEY')
  request_uri = f"https://api.smmry.com?SM_API_KEY={key}&SM_LENGTH=5&SM_URL={uri}"
  result = requests.get(request_uri)
  return result.text