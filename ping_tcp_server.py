'''
### ping_tcp_server.py
# Usage:
#     python ping_tcp_server.py -p <port> -r <regexp>
# This will start a TCP service on the specified port.
# "<regexp>" is a Python-compatible regular expression
# (https://docs.python.org/2/library/re.html).
# The server will expect to receive a request starting with "PING " and
# terminating with a new-line (\n):
#     PING arbitrary text
# "arbitrary text" can contain any byte except newlines.
# The server will reply with one of three responses, terminated with a newline:
#     PONG found
# if "arbitrary text" in the request matches the regular expression provided
# in the command line, or
#     PONG not-found
# if "arbitrary text" in the request does not match the regular expression
# provided in the command line, or
#     ERROR optional error message
# if the server could not understand the request and any other error occurred.
# If possible, the server should include an error message describing the cause
# of # the error.
#
# The server must be able to process multiple requests in the same connection,
# until the client closes the connection.
# The server must be able to handle concurrent requests from multiple clients.
'''


import SocketServer
import sys
import re
import argparse


#it will run this on the localhost unless you change this variable
HOST = 'localhost'

#setup the arguments
parser = argparse.ArgumentParser()
parser.add_argument("-p", help="port number")
parser.add_argument("-r", help="regex")
args, unknown = parser.parse_known_args()

#if the arguments exist assign them to a variable
#if they don't exist complain and quit
if args.p is not None:
    PORT = int(args.p)
else:  
    print "NEED PORT NUMBER"
    sys.exit()
    
if args.r is not None:
    TEXT = args.r
else:  
    print "NEED REGEX TO LOOK FOR"
    sys.exit()

class SingleTCPHandler(SocketServer.BaseRequestHandler):
    "One instance per connection.  Override handle(self) to customize action."
    def handle(self):
        # here is the data they sent
        data = self.request.recv(1024)  
        #setup varilables to try and match the PING, REGEX, and \n
        intro = re.compile(r'PING:')
        end = '\n'
        full = re.compile(r'PING:'+ r' ' + TEXT + r'\n')

        #If everything matches give the full OK
        if full.match(data):
            pongF = ("PONG found"+'\n')
            self.request.send(pongF)
        #if that doesn't work check to see if the PING and \n match
        elif (intro.match(data) and end.endswith('\n')):
            pongNF = ("PONG not found"+'\n')
            self.request.send(pongNF)
        #if that doesn't work just check to see if you get the PING: at the beginning
        elif intro.match(data):
            pongNF = ("ERROR I see PING but not the new line"+'\n')
            self.request.send(pongNF)
        #if you cannot match the PING at the beginning just error out
        else:
            error = ("UNKNWOWN ERROR - possibly missing PING at intro" +'\n')
            self.request.send(error)


class SimpleServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    #setup the multithreading
    # make sure the ctrl+c will kill all of the threads
    daemon_threads = True
    # much faster rebinding
    allow_reuse_address = True

    def __init__(self, server_address, RequestHandlerClass):
        SocketServer.TCPServer.__init__(self, server_address, RequestHandlerClass)

if __name__ == "__main__":
    server = SimpleServer((HOST, PORT), SingleTCPHandler)
    # terminate with Ctrl-C
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        sys.exit(0)