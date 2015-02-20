#test feeding data to graphite directly
import socket
from json_read import to_graphite #takes json result file / outputs graphite message list
import urllib2
from time import sleep, asctime


CARBON_SERVER = '127.0.0.1'
CARBON_PORT = 2003

#Needs a way to pull/read directly from http://http://10.228.141.113:9011/results/*
#jlist only works after saving files into the working directory

jlist = ['result_2015-02-01.json', 'result_2015-02-02.json', 'result_2015-02-03.json', 'result_2015-02-04.json',
         'result_2015-02-05.json', 'result_2015-02-06.json', 'result_2015-02-07.json', 'result_2015-02-08.json',
         'result_2015-02-09.json', 'result_2015-02-10.json', 'result_2015-02-11.json', 'result_2015-02-12.json',
         'result_2015-02-13.json', 'result_2015-02-14.json', 'result_2015-02-15.json', 'result_2015-02-16.json',
         'result_2015-02-17.json', 'result_2015-02-18.json', 'result_2015-02-19.json', 'result_2015-02-20.json',]

while True:
    for jfile in jlist: 
        with open(jfile, 'r') as message:
        #message = to_graphite(urllib2.urlopen('http://http://10.228.141.113:9011/results/PR/'+json_file).readlines())
        #the above method of pulling from the network gives me an error
            for line in to_graphite(message.readlines()):
                sock = socket.socket()
                sock.connect((CARBON_SERVER, CARBON_PORT))
                sock.send(line)
                sock.close()
        print jfile[:-5] + ' messages sent at ' + asctime()
    sleep(60)
    
    #When I don't open a new socket connection for each line (as above), I think some data is lost, and I have to
    #repeat the read/send process. The above takes about 10 minutes per result file however, whereas sending all
    #the lines over one socket takes about 2 seconds per result file.