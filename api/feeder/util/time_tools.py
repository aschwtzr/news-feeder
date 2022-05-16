from datetime import datetime

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