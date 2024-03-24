import threading
import socket
import json
MAXBUF = 65535

class Thread(threading.Thread):

    def __init__(self, newsock, sockname):
        threading.Thread.__init__(self)
        self.sock = newsock
        self.sockname = sockname

    def run(self):
        while True:
            try:
                data = self.sock.recv(MAXBUF)
                if data == b'': break
                print(data.decode())
            except EOFError:
                break
        self.sock.close()

def server(interface, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((interface, port))
    sock.listen(1)
    print('Listening at', sock.getsockname())

    while True:
        try:
            newsock, sockname = sock.accept()
            thread = Thread(newsock, sockname)
            thread.start()
        except EOFError: # TODO
            break