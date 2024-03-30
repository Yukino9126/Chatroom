import threading
import socket
import json
import queue
MAXBUF = 65535

class Thread(threading.Thread):

    users = {}     # sockname : username
    msg_queue = {} # sockname : queue.Queue()

    def __init__(self, newsock, sockname):
        # init
        threading.Thread.__init__(self)
        # sock
        self.sock = newsock
        self.sock.settimeout(1.0)
        # user info
        self.username = ''
        self.sockname = str(sockname)
        Thread.users[self.sockname] = ''
        Thread.msg_queue[self.sockname] = queue.Queue()
        print(f'[SOCK] {self.sockname}: Connected!')

    def run(self):
        # Send / Recv
        while True:
            # Recv Data
            try:
                data = self.sock.recv(MAXBUF)
                if data == b'':
                    break
                msg = data.decode()

                # ----- Handle ----- #
                # slash command
                if msg[0] == '/':
                    if msg[1:5] == 'QUIT':   # Stop the connection and send the msg
                        self.new_msg(msg[5:].strip())
                        break
                    elif msg[1:5] == 'USER': # Modify the username and the list of online users
                        newname = msg[5:].strip()
                        print(f'[INFO] {self.sockname}: {self.username} -> {newname}')
                        self.username = newname
                        Thread.users[self.sockname] = self.username
                    elif msg[1:4] == 'WHO':  # Send the list of online users
                        print(f'[INFO] {self.sockname}: {self.username} requested the list of online users.')
                        self.sock.send(bytes(json.dumps(('*SERVER*', Thread.users)), 'UTF-8'))
                # General Msg
                else:
                    self.new_msg(msg)
                # ------------------ #
            # Send
            except socket.timeout:
                self.get_msg()

        # Delete
        print(f'[SOCK] {self.sockname}: {self.username} left.')
        self.sock.close()
        Thread.users.pop(self.sockname)
        Thread.msg_queue.pop(self.sockname)

    def new_msg(self, msg):
        print(f'{self.username:>10s} > {msg}')
        for i in Thread.msg_queue:
            if i != self.sockname:
                Thread.msg_queue[i].put(json.dumps((self.username, msg)))

    def get_msg(self):
        msgq = Thread.msg_queue[self.sockname]
        while not msgq.empty():
            self.sock.send(bytes(msgq.get(), 'UTF-8'))


def server(interface, port):
    # socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((interface, port))
    sock.listen(1)
    print('Listening at', sock.getsockname())

    try:
        while True:
            print('[SOCK] Waiting to accept a new connection')
            newsock, sockname = sock.accept()
            thread = Thread(newsock, sockname)
            thread.daemon = True
            thread.start()
    except KeyboardInterrupt:
        pass
    sock.close()
