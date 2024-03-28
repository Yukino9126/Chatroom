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
        self._exc = None
        try:
            # Send username
            self.sock.send(bytes('/USER ' + self.name, 'UTF-8'))

            # Send msg
            while True:
                msg = input(f"{'':>10s} > ")
                if msg != '':
                    data = bytes(msg, 'UTF-8')
                    self.sock.send(data)
        except (KeyboardInterrupt, EOFError):
            print('\nClient Disconnect')
            return

class Recv_Thread(threading.Thread):

    def __init__(self, sock):
        threading.Thread.__init__(self)
        self.sock = sock

    def run(self):
        try:
            while True:
                # Recv
                data = self.sock.recv(MAXBUF)
                if data == b'':
                    print('\nServer Disconnect')
                    return
                # Display
                user, msg = json.loads(data.decode())
                print(f'\n{user:>10s} > {msg}')
        except (KeyboardInterrupt, EOFError):
            return

def client(host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.connect((host, port))

    try:
        send = Send_Thread(sock, input('Your name? '))
        recv = Recv_Thread(sock)
        send.start()
        recv.start()

    except (KeyboardInterrupt, EOFError):
        send.join()
        recv.join()
        print('Connetion interrupted.')
        sock.close()

if __name__ == '__main__':
    client('127.0.0.1', 20000)