import urllib
from topTalkers import topTalk
import json
import requests
import time
import datetime
import sys
f = open(sys.argv[3],"w")
def func(start,end):
  #print start
  #print end

  query = json.dumps({"size":1000,"filter":{"bool":{"must":[{"range":{"start":{"gte":start,"lte":end,"format":"epoch_millis"}}}],"must_not":[]}}})
  response = requests.get("http://140.182.49.116:9200/_search?pretty=1",data=query,stream=True)
  content = response.raw.read( decode_content=True)
  f.write(content)
 # results = response.text
  '''url = 'http://140.182.49.116:9200/_search?pretty=1'
  values = {"size":500,"filter":{"bool":{"must":[{"range":{"start":{"gte":start,"lte":end,"format":"epoch_millis"}}}],"must_not":[]}}}
  data = urllib.urlencode(values)
  f.write(urllib.urlopen("http://140.182.49.116:9200/_search?pretty=1%s" % data).read())'''
  f.close()


def getUnixTime(dt):
  splitDate = dt.split('-')
  mydat = datetime.datetime(int(splitDate[0]),int(splitDate[1]),int(splitDate[2]),int(splitDate[3]),int(splitDate[4]),int(splitDate[5]))
  epoch = datetime.datetime.utcfromtimestamp(0)
  td = mydat - epoch
  unixtime = (td.microseconds + (td.seconds + td.days * 86400) * 10 ** 6 )/ 10**6
  unixStr = str(unixtime)
  if len(unixStr) <13:
    for i in range (13 - len(unixStr)):
      unixStr = unixStr + "0"
  return int(unixStr)

if __name__ == '__main__':
  # Input format --> getRequest 
  if len(sys.argv) < 4 :
    print " usage --> 'python getRequest startDate(year-month-day-hour-min-sec) endDate fileName"
    exit(1)
  
  # get unix data type from the given time
  start = getUnixTime(sys.argv[1])
  end = getUnixTime(sys.argv[2])
  
  func(start,end)
  topTalk(sys.argv[3]) 
