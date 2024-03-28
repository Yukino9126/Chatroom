import argparse
from server import server
from client import client

if __name__ == '__main__':
    choices = {'client': client, 'server': server}
    parser = argparse.ArgumentParser(description='Internet Relay Chat')
    parser.add_argument('role', choices=choices, help='which role to play')
    parser.add_argument('host', help='interface the server listens at;'
                        ' host the client sends to')
    parser.add_argument('-p', metavar='PORT', type=int, default=6667,
                        help='IRC port (default 6667)')
    args = parser.parse_args()
    function = choices[args.role]
    function(args.host, args.p)