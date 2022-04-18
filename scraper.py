#!/usr/bin/env python
# coding: utf-8

# In[2]:


import requests
import pandas as pd
from datetime import datetime, timezone
import json


# In[3]:


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

# url = "https://jsonplaceholder.typicode.com/todos/1"

url = "https://backend.dr-plano.com/courses_dates?id=114569964&start=1650265200000&end=1650319200000"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36",
    "accept": "application/json"
}
response = requests.get(url, headers=headers)


# In[4]:


def toIsoString(dateTime):
    return dateTime.isoformat()

def getUtcIsoString():
    utcDt = datetime.now(timezone.utc).replace(microsecond=0)
    return toIsoString(utcDt)

def unixTimestampToUTCIsoString(unixTimestamp):
    # cast to int (should be int already but just in case)
    # /1000 to get milliseconds from microseconds
    ts = int(unixTimestamp) / 1000
    dt = datetime.utcfromtimestamp(ts)
    return toIsoString(dt)

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


# In[ ]:





# In[5]:


parsed_result = {
    "cod": response.status_code,
    "ela": response.elapsed.microseconds,
    "url": response.url, 
    "dat": getUtcIsoString(),
    "enc": response.encoding,
    "ctt": response.headers["Content-Type"],
    "d": parse_payload(response.json())
}


# In[6]:


json_string = json.dumps(parsed_result)

with open("stats/parsed.data", "a") as data_file:
    data_file.write(json_string + "\n")

