#!/usr/bin/env python
# coding: utf-8

# In[13]:


# python -m pip install -r requirements.txt
# to python-script:
#  - via jupyterlab-gui
#  - via jupyter nbconvert --to script [YOUR_NOTEBOOK].ipynb


# In[12]:


import requests
from datetime import datetime, timezone
import json


# ## Berta Block Boulderhalle Berlin Scraper

# In[4]:


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


# In[5]:


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


# In[6]:


# url = "https://jsonplaceholder.typicode.com/todos/1"

# start: e.g. 1650265200000
# end: e.g. 1650319200000
url = (
        "https://backend.dr-plano.com/courses_dates?" +
        "id=114569964" +
        "&start=" + str(getUnixTimestamp(getDatetimeTodayWithSpecificHour(7))) +
        "&end=" + str(getUnixTimestamp(getDatetimeTodayWithSpecificHour(22))))
url


# In[7]:


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36",
    "accept": "application/json"
}
response = requests.get(url, headers=headers)


# In[8]:


parsed_result = {
    "cod": response.status_code,
    "ela": response.elapsed.microseconds,
    "url": response.url, 
    "dat": getUtcIsoString(),
    "enc": response.encoding,
    "ctt": response.headers["Content-Type"],
    "d": parse_payload(response.json())
}


# In[9]:


json_string = json.dumps(parsed_result)
json_string


# In[10]:


with open("stats/parsed.data", "a") as data_file:
    data_file.write(json_string + "\n")

