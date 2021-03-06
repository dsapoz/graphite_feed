#feeding PR, UAT, SI, PT, NST data to graphite directly
import socket, urllib2, pytz
from json_read import result_to_graphite, trend_to_graphite, add_env #takes json result file / outputs graphite message list
from time import sleep, asctime
from datetime import datetime


CARBON_SERVER = '127.0.0.1'
CARBON_PORT = 2003
envs = ['PR', 'UAT', 'PT', 'SI', 'NST']


while True:
    for env in envs:
        jfile = 'result_'+str(datetime.now(pytz.utc))[:10]+'.json' #uses file for current date (in UTC)
        url = 'http://10.228.141.113:9011/results/' + env + '/' + jfile
        
        try:
            urllib2.urlopen(url)
        except urllib2.URLError:
            print url + ' does not exist'
            continue #if url does not exist yet, continue to next environment
        
        sock = socket.socket()
        sock.connect((CARBON_SERVER, CARBON_PORT))
        
        for line in add_env(env, result_to_graphite(urllib2.urlopen(url).readlines())):
            sock.send(line)
        sock.close()
        print env + ' ' + jfile[:-5] + ' messages sent at ' + asctime()
    sleep(300) #wait 5 minutes then collect logs again

"""env, jfile = 'PR', 'A0101_PR_trend.json'
url = 'http://10.228.141.113:9011/stat_trends/' + env + '/' + jfile
sock = socket.socket()
sock.connect((CARBON_SERVER, CARBON_PORT))
        
for line in add_env(env, trend_to_graphite(urllib2.urlopen(url).readlines())):
    sock.send(line)
sock.close()
print env + ' ' + jfile[:-5] + ' messages sent at ' + asctime()"""