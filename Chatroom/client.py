import threading
import socket
import json
from sys import stdin
MAXBUF = 65535

class Send_Thread(threading.Thread):

    def __init__(self, sock, name):
        threading.Thread.__init__(self)
        self.sock = sock
        self.name = name

    def run(self):
        # Send username
        self.sock.send(bytes('/USER ' + self.name, 'UTF-8'))

        # Send msg
        while True:
            try:
                msg = input(f"{'':>10s} > ")
                if msg[0:6] == '/HELP': # Print the slash command
                    self.help_info()
                    continue
                if msg != '':           # Send the msg
                    data = bytes(msg, 'UTF-8')
                    self.sock.send(data)
                if msg[0:6] == '/QUIT': # Stop the thread
                    break

            except socket.timeout:
                if stop_flag == True:
                    break
                
        stop_flag = True
        return
    
    def help_info(self):
        print()
        print('/USER <username>  will specify a username of the connecting client')
        print('/WHO              will return a list of users logged into the server.')
        print('/QUIT [<msg>]     will end a client session. The server will close the socket to this client.')
        print()


class Recv_Thread(threading.Thread):

    def __init__(self, sock):
        threading.Thread.__init__(self)
        self.sock = sock

    def run(self):

        while True:
            try:
                # Recv
                data = self.sock.recv(MAXBUF)
                if data == b'':
                    break

                # Display
                user, msg = json.loads(data.decode())
                print(f'\n{user:>10s} > {msg}')

            except socket.timeout:
                if stop_flag == True:
                    break

        stop_flag = True
        return

def client(host, port):
    # socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.settimeout(1)
    sock.connect((host, port))
    # flag
    global stop_flag
    stop_flag = False

    try:
        send = Send_Thread(sock, input('Your name?   '))
        recv = Recv_Thread(sock)
        send.start()
        recv.start()
        send.join()
        recv.join()

    except (KeyboardInterrupt, EOFError):
        stop_flag = True
        
    send.join()
    recv.join()
    sock.close()