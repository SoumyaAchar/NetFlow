import sys
import pandas as pd
import json

def getMax(dataDict):
  maxData = -1
  maxIp = ""
  for ip,values in dataDict.iteritems():
    if values > maxData:
      maxData = values
      maxIp = ip
  return [maxIp, maxData]


def topTalk(filename):
  with open(filename) as data_file:
    data = json.load(data_file)

  ids = set()
  output = {}
  i=0
  for entry in data["hits"]["hits"]:
    if entry["_index"] == ".kibana":
      continue
    inner = {}
    uniqueId = entry["_id"]
    src_ipAddress = entry["_source"]["meta"]["src_ip"] 
    dst_ipAddress = entry["_source"]["meta"]["dst_ip"]
    mb_sent = (entry["_source"]["values"]["num_bits"])/(8*1024*1024)

    if uniqueId in ids:
      print "Duplicate flow ID found "
    else:
      ids.add(uniqueId)

    i+=1
    if(output.has_key(src_ipAddress)):
      if(output.get(src_ipAddress).has_key(dst_ipAddress)):
        inner[dst_ipAddress] = mb_sent + output.get(src_ipAddress).get(dst_ipAddress)
        output[src_ipAddress][dst_ipAddress] = inner[dst_ipAddress]
      else:
        inner[dst_ipAddress] = mb_sent
        output[src_ipAddress][dst_ipAddress] = inner[dst_ipAddress]
    else:
        inner[dst_ipAddress] = mb_sent
        output[src_ipAddress] = inner

# To find the src dst pair with max bits exchanged
  maxDataExchanged = -1
  finalSrc = ""
  finalDst = ""
  srcDict = {} 
  dstDict = {} #srcDict will hold scr + data sent and dstDict will hold dst + data recieved
  for src, values in output.iteritems():
    maxSrc=0
    for dst, dataInMb in values.iteritems():
      #print "-- src " + src + " dst " + dst + " value " + str(dataInMb) + "\n"
      maxSrc = maxSrc + dataInMb
      if(dst in dstDict):
        dstDict[dst] = dstDict[dst]+dataInMb
      else:
        dstDict[dst] = dataInMb
      if dataInMb > maxDataExchanged:
        finalSrc = src
        finalDst = dst
        maxDataExchanged = dataInMb
    srcDict[src] = maxSrc

  
  print "Number of flows " + str(i) + "\n"
  print "-----TOP TALKERS-----"
  print "Pairwise Source "+finalSrc +" Destination "+finalDst+" Data transferred "+str(maxDataExchanged) + " MB"
  print "Max data was sent from " + getMax(srcDict)[0] + ", data= "+str(getMax(srcDict)[1]) + " MB"
  print "Max data was received by "+getMax(dstDict)[0] + ", data= "+str(getMax(dstDict)[1]) + " MB\n"

if __name__ == "__main__":
  topTalk(sys.argv[1])

