#test feeding data to graphite directly

#import statsd
import socket
from random import randint
import time
import pickle
import struct


delay = 60


CARBON_SERVER = '127.0.0.1'
CARBON_PORT = 2003

metrics = list()
for i in range(10):
    metrics.append('test.gauges.test_raw ' + str(i**2) + ' ' + str(time.time() - 90+10*i) + '\n')
    
message = metrics

#message = 'test.gauges.test_raw 30 %d\n' % int(time.time())
#payload = pickle.dumps(metrics, protocol = -1)
#header = struct.pack("!L", len(payload))
#message = header + payload

sock = socket.socket()
sock.connect((CARBON_SERVER, CARBON_PORT))

for i in range(len(message)):
    print 'sending message:\n%s' % message[i]
    #sock = socket.socket()
    #sock.connect((CARBON_SERVER, CARBON_PORT))
    sock.send(message[i])
    #time.sleep(15)
    #sock.close()
    
sock.close()



#def main():
    

#if __name__ == "__main__":
    #main()