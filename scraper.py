#!/usr/bin/env python
# coding: utf-8

# In[10]:


# python -m pip install -r requirements.txt
# to python-script:
#  - via jupyterlab-gui
#  - via jupyter nbconvert --to script [YOUR_NOTEBOOK].ipynb
pass


# In[11]:


import requests
from datetime import datetime, timezone, timedelta
import json


# ## Berta Block Boulderhalle Berlin Scraper

# In[12]:


"""
acronyms:

cod: status_code
ela: elapsed in microseconds (not milliseconds)
url: url
dat: date
enc: encoding
ctt: content-type
d: data

dli: datalist: [{event start (string utc nach iso 8601), end: event end (string utc nach iso 8601)}, ...]
min: minCourseParticipantCount
max: maxCourseParticipantCount
cur: currentCourseParticipantCount
state: state

"""

pass


# In[13]:


def toIsoString(dateTime):
    return dateTime.isoformat()

def getUtc():
    return datetime.now(timezone.utc).replace(microsecond=0)

def getUtcIsoString():
    return toIsoString(getUtc())

def unixTimestampToUTCIsoString(unixTimestamp):
    # cast to int (should be int already but just in case)
    # /1000 to get milliseconds from microseconds
    ts = int(unixTimestamp) / 1000
    dt = datetime.utcfromtimestamp(ts)
    return toIsoString(dt)

def getUnixTimestamp(dt):
    return int(dt.timestamp()) * 1000

def getDatetimeTodayWithSpecificHour(hour):
    return getUtc().replace(hour=hour, minute=0, second=0)

def parse_payload(response_payload):
    data = []
    for a in response_payload:
        record = {
        "dli": [{"sta": unixTimestampToUTCIsoString(b["start"]), "end": unixTimestampToUTCIsoString(b["end"])} for b in a["dateList"]],
        "min": a["minCourseParticipantCount"],
        "max": a["maxCourseParticipantCount"],
        "cur": a["currentCourseParticipantCount"],
        "state": a["state"]
        }
        data.append(record)
    return data


# In[14]:


# url = "https://jsonplaceholder.typicode.com/todos/1"

# start: e.g. 1650265200000
# end: e.g. 1650319200000
url = (
        "https://backend.dr-plano.com/courses_dates?" +
        "id=114569964" +
        "&start=" + str(getUnixTimestamp(getDatetimeTodayWithSpecificHour(7))) +
        "&end=" + str(getUnixTimestamp(getDatetimeTodayWithSpecificHour(22))))
url


# In[15]:


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36",
    "accept": "application/json"
}
response = requests.get(url, headers=headers)


# In[16]:


parsed_result = {
    "cod": response.status_code,
    "ela": response.elapsed.microseconds,
    "url": response.url, 
    "dat": getUtcIsoString(),
    "enc": response.encoding,
    "ctt": response.headers["Content-Type"],
    "d": parse_payload(response.json())
}


# In[19]:


# # get length of file
# data = []
# with open('stats/parsed.data') as f:
#     for line in f:
#         data.append(json.loads(line))
# len(data)


# In[18]:


def write_parsed_result_to_file(parsed_result):
    filename = "stats/parsed.data"
    json_string = json.dumps(parsed_result)
    print(json_string)
    with open(filename, "a") as f:
        f.write(json_string + "\n")
    
    # if first data record is older than 1 year, delete this record
    # so the data does not grow indefinitly
    date_current = getUtc()
    date_year_ago = date_current - timedelta(days=1*365/365)
    with open(filename, 'r+') as f:
        line = f.readline() # read the first line and throw it out
        json_line = json.loads(line)
        date_file_string = json_line["dat"]
        date_file_datetime = datetime.fromisoformat(date_file_string)
        if(date_file_datetime < date_year_ago):
            data = f.read() # read the rest
            f.seek(0) # set the cursor to the top of the file
            f.write(data) # write the data back
            f.truncate() # set the file size to the current size
    return

write_parsed_result_to_file(parsed_result)


# In[ ]:




