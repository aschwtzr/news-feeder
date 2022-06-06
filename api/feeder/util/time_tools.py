from datetime import datetime, timedelta

def timestamp_string():
    timestamp = datetime.now()
    return timestamp.strftime("%m/%d/%Y, %H:%M:%S")

def print_timestamp(message):
  timestamp = timestamp_string()
  print(f"""
  *****************************************  
  *****************************************  
    {message} AT {timestamp}
  *****************************************  
  *****************************************  
  """)

def date_time_string(hours_ago=36):
  return datetime.now() - timedelta(hours = hours_ago)