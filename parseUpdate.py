import sys
from optparse import OptionParser
from datetime import *
from mrtparse import *
import commands
myASnumber = 0
indt = 0
target = open("outPut.txt","w")
ipset = set()
def prline(line):
    global indt
    print('    ' * indt + line)

def print_bgp4mp(m):
    global indt
    indt = 0
    prline('%s' % BGP4MP_ST[m.subtype])
    indt += 1
    if ( m.subtype == BGP4MP_ST['BGP4MP_MESSAGE']
        or m.subtype == BGP4MP_ST['BGP4MP_MESSAGE_AS4']
        or m.subtype == BGP4MP_ST['BGP4MP_MESSAGE_LOCAL']
        or m.subtype == BGP4MP_ST['BGP4MP_MESSAGE_AS4_LOCAL']):
        print_bgp_msg(m.bgp.msg, m.subtype, m)

def print_bgp_msg(msg, subtype, m):
    global indt
    global myASnumber
    global ipset
    indt = 0
    for withdrawn in msg.withdrawn:
        ip = str(withdrawn.prefix)+"/"+str(withdrawn.plen)
        print ip
        if ip in ipset:
            print "came here"
            target.write("withdrew route " + str(withdrawn.prefix)+"/"+str(withdrawn.plen)+ " at "+str(datetime.fromtimestamp(m.ts))+"\n")

    for attr in msg.attr:
        if attr.type == BGP_ATTR_T['AS_PATH']:
            asPathValue = []
            for path_seg in attr.as_path:
                asPathValue = path_seg['val']
                print asPathValue
                if myASnumber == str(asPathValue[-1]):
                    for nlri in msg.nlri:
                        target.write("added route " + str(nlri.prefix)+"/"+str(nlri.plen)+" at "+str(datetime.fromtimestamp(m.ts))+"\n")

def main():
    global myASnumber
    global ipset
    if len(sys.argv) != 3:
        print('Usage: %s FILE AS_NUMBER' % sys.argv[0])
        exit(1)

    d = Reader(sys.argv[1])
    myASnumber=sys.argv[2]
    cmd = "whois -h whois.radb.net -- '-i origin AS"+myASnumber+ "' | grep route:"
    print cmd
    ipInfo = commands.getoutput(cmd)
    for ip in ipInfo.split("\n"):
        ipset.add(ip[12:])

    #i =0
    #for i in range(0,1000):
    for m in d:
        m = m.mrt
        print('--------------------------------------------------------------')
        if ( m.type == MRT_T['BGP4MP'] or m.type == MRT_T['BGP4MP_ET']):
            print_bgp4mp(m)
    print ipset
    target.close()

if __name__ == '__main__':
    print "main entered"
    main()
