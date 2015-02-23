#feeding PR, UAT, SI, PT, NST data to graphite directly
import socket, urllib2, pytz
from json_read import to_graphite, add_env #takes json result file / outputs graphite message list
from time import sleep, asctime
from datetime import datetime


CARBON_SERVER = '127.0.0.1'
CARBON_PORT = 2003
envs = ['PR', 'UAT', 'SI', 'PT', 'NST'] 


while True:
    for env in envs:
        exist = False
        jfile = 'result_'+str(datetime.now(pytz.utc))[:10]+'.json' #uses file for current date (in UTC)
        url = 'http://10.228.141.113:9011/results/' + env + '/' + jfile
        
        while not exist:
            try:
                urllib2.urlopen(url)
                exist = True
            except urllib2.URLError:
                sleep(300) #if url doesn't exist yet, wait 5 minutes then try again
        
        sock = socket.socket()
        sock.connect((CARBON_SERVER, CARBON_PORT))
        for line in add_env(env, to_graphite(urllib2.urlopen(url).readlines())):
            sock.send(line)
        
        sock.close()
        print env + ' ' + jfile[:-5] + ' messages sent at ' + asctime()
    sleep(60) #wait 1 minute then collect logs again