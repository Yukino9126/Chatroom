import threading
import socket
import json
import time
MAXBUF = 65535

class Send_Thread(threading.Thread):

    def __init__(self, sock, name):
        threading.Thread.__init__(self)
        self.sock = sock
        self.name = name

    def run(self):
        while True:
            try:
                msg = input("> ")
            except EOFError:
                break
            if msg != '':
                data = bytes(json.dumps((self.name, msg)), 'UTF-8')
                self.sock.send(data)
        self.sock.close()


class Recv_Thread(threading.Thread):

    def __init__(self, sock):
        threading.Thread.__init__(self)
        self.sock = sock

    def run(self):
        while True:
            try:
                data = self.sock.recv(MAXBUF)
                if data == b'':
                    break
                print(data.decode('UTF-8'))
            except EOFError:
                pass

def client(host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.connect((host, port))

    send = Send_Thread(sock, input('Your name? '))
    recv = Recv_Thread(sock)
    send.start()
    recv.start()

if __name__ == '__main__':
    client('127.0.0.1', 20000)