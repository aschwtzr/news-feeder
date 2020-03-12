import datetime

def timestamp_string ():
    timestamp = datetime.datetime.now()
    return timestamp.strftime("%m/%d/%Y, %H:%M:%S")