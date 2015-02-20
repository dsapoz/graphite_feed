#feeding data to graphite directly
import socket, urllib2, pytz
from json_read import to_graphite #takes json result file / outputs graphite message list
from time import sleep, asctime
from datetime import datetime


CARBON_SERVER = '127.0.0.1'
CARBON_PORT = 2003


while True:
    exist = False
    jfile = 'result_'+str(datetime.now(pytz.utc))[:10]+'.json' #uses file for current date (in UTC)
    url = 'http://10.228.141.113:9011/results/PR/'+jfile
    
    while not exist:
        try:
            urllib2.urlopen(url)
            exist = True
        except urllib2.URLError:
            sleep(300) #if url doesn't exist yet, wait 5 minutes then try again
    
    for line in to_graphite(urllib2.urlopen(url).readlines()):
        sock = socket.socket()
        sock.connect((CARBON_SERVER, CARBON_PORT))
        sock.send(line)
        sock.close()
    print jfile[:-5] + ' messages sent at ' + asctime()

    
    #When I don't open a new socket connection for each line (as above), I think some data is lost, and I have to
    #repeat the read/send process. The above takes about 10 minutes per result file however, whereas sending all
    #the lines over one socket takes about 2 seconds per result file.