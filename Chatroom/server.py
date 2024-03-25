import threading
import socket
import json
MAXBUF = 65535

class Thread(threading.Thread):

    users = {}

    def __init__(self, newsock, sockname):
        threading.Thread.__init__(self)
        self.sock = newsock
        self.sockname = sockname
        Thread.users[sockname] = ''

    def run(self):
        self.sock.settimeout(1.0)
        while True:
            try:
                data = self.sock.recv(MAXBUF)
                if data == b'':
                    break
                name, msg = json.loads(data.decode())
                if msg[0] == '/':
                    if msg[1:5] == 'QUIT':
                        print('QUIT')
                    elif msg[1:5] == 'USER':
                        Thread.users[self.sockname] = msg[5:].strip()
                    elif msg[1:4] == 'WHO':
                        print(Thread.users)
                print(f'{name}: {msg}')
            except socket.timeout:
                self.sock.send(b'AAA')
        self.sock.close()
        Thread.users.pop(self.sockname)

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