import threading
import socket
import json
import queue
from datetime import datetime
MAXBUF = 65535

class Thread(threading.Thread):

    username = ''
    users = {}
    threading_list = []
    msg_queue = queue.Queue()

    def __init__(self, newsock, sockname):
        threading.Thread.__init__(self)
        self.sock = newsock
        self.sockname = sockname
        Thread.users[sockname] = ''

    def run(self):
        # try:
            Thread.threading_list.append(threading.current_thread())
            self.sock.settimeout(1.0)
            while True:
                try:
                    data = self.sock.recv(MAXBUF)
                    if data == b'':
                        break
                    msg = data.decode()
                    if msg[0] == '/':
                        if msg[1:5] == 'QUIT':
                            print('QUIT')
                        elif msg[1:5] == 'USER':
                            self.username = msg[5:].strip()
                            Thread.users[self.sockname] = self.username
                            continue
                        elif msg[1:4] == 'WHO':
                            # self.sock.send(bytes(json.dumps(Thread.users), 'UTF-8'))
                            continue
                    for i in Thread.threading_list:
                        if i != threading.current_thread():
                            i.msg_queue.put(json.dumps((self.username, msg)))
                            print(json.dumps((self.username, msg)))
                except socket.timeout:
                    while not self.msg_queue.empty():
                        self.sock.send(bytes(self.msg_queue.get(), 'UTF-8'))
            self.sock.close()
            Thread.users.pop(self.sockname)
        # except:
        #     pass

def server(interface, port):
    # socket
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