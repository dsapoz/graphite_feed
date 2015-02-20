#feeding data to graphite directly
import socket
from json_read import to_graphite #takes json result file / outputs graphite message list
import urllib2
from time import sleep, asctime


CARBON_SERVER = '127.0.0.1'
CARBON_PORT = 2003


jfile = 'result_2015-02-20.json' #Should have a way to check current date and change jfile accordingly?

while True:
    for line in to_graphite(urllib2.urlopen('http://10.228.141.113:9011/results/PR/'+jfile).readlines()):
        sock = socket.socket()
        sock.connect((CARBON_SERVER, CARBON_PORT))
        sock.send(line)
        sock.close()
    print jfile[:-5] + ' messages sent at ' + asctime()

    
    #When I don't open a new socket connection for each line (as above), I think some data is lost, and I have to
    #repeat the read/send process. The above takes about 10 minutes per result file however, whereas sending all
    #the lines over one socket takes about 2 seconds per result file.