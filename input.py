#test feeding data to graphite directly
import socket
from json_read import to_graphite #takes json result file / outputs graphite message list
import urllib2


CARBON_SERVER = '127.0.0.1'
CARBON_PORT = 2003
json_file = ''
message = to_graphite(json_file.readlines())
print message

sock = socket.socket()
sock.connect((CARBON_SERVER, CARBON_PORT))

for line in message:
    sock.send(message[i])
    print message[i] + ' ...sent'
    
sock.close()