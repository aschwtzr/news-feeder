# interface with external APIs
import time
import requests
import os
import json

def get_data_from_uri (uri):
  try:
    results = requests.get(uri, timeout=60)
    return {
      'ok': True, 
      'data': results.text
      }
  except requests.exceptions.RequestException as error:
    print(error)
    return {
      'ok': False,
      'error': error
      }

def get_content_from_uri (uri):
  try:
    res = requests.get(uri, timeout=60)
    return {
      'ok': True, 
      'data': res.content
      }
  except requests.exceptions.RequestException as error:
    print(error)
    return {
      'ok': False,
      'error': error
      }


def get_timeline_for_user (screen_name):
  headers = {f"Authorization": "Bearer {auth_token}"}
  uri = f"https://api.twitter.com/1.1/statuses/user_timeline.json?screen_name={screen_name}"
  try: 
    res = requests.get(uri, headers=headers, timeout=90)
    # print(res.content)
    # print(res.text)
    parsed = json.loads(res.text)
    # print(parsed)
    return {
      'ok': True, 
      'data': parsed
      }
  except requests.exceptions.RequestException as error:
    print(error)
    return {
      'ok': False,
      'error': error
      }

def summarize_text (text, length):
  key = os.environ.get('SUMMRY_KEY')
  request_uri = f"https://api.smmry.com?SM_API_KEY={key}&SM_KEYWORD_COUNT=0&SM_LENGTH={length}"
  result = requests.post(
    request_uri,
    json={'sm_api_input': text }
    )
  parsed = json.loads(result.text)
  print(parsed)
  if "sm_api_error" in parsed:
    print(parsed['sm_api_message'])
    result_hash = {
      'ok': False,
      'error': parsed['sm_api_message']
    }
  else:
    result_hash = {
      'ok': True,
      'summary': parsed['sm_api_content'],
      'keywords': parsed['sm_api_keyword_array'], 
      'character_count': int(parsed['sm_api_character_count']),
      'credits_used': int(parsed['sm_api_credit_cost']),
      'credit_balance': int(parsed['sm_api_credit_balance'])
    }
  return result_hash

def get_summary (uri):
  key = os.environ.get('SUMMRY_KEY')
  request_uri = f"https://api.smmry.com?SM_API_KEY={key}&SM_KEYWORD_COUNT=5&SM_LENGTH=5&SM_URL={uri}"
  result = requests.get(request_uri)
  parsed = json.loads(result.text)
  print(parsed)
  if "sm_api_error" in parsed:
    print(parsed['sm_api_message'])
    result_hash = {
      'ok': False,
      'error': parsed['sm_api_message']
    }
  else:
    result_hash = {
      'ok': True,
      'summary': parsed['sm_api_content'],
      'keywords': parsed['sm_api_keyword_array'], 
      'character_count': int(parsed['sm_api_character_count']),
      'credits_used': int(parsed['sm_api_credit_cost']),
      'credit_balance': int(parsed['sm_api_credit_balance'])
    }
  return result_hash
