import sys
import getopt
import socket
import time
from random import randrange


class Client:
    def __init__(self, port, ia_file, is_ghost):
        self.port = port
        self.ia_file = ia_file
        self.sock = None
        self.server_address = None
        self.is_ghost = is_ghost

    def connect(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Connect the socket to the port where the server is listening
        self.server_address = ('localhost', self.port)
        # print('connecting to %s port %s' % self.server_address)
        try:
            self.sock.connect(self.server_address)
        except Exception as e:
            print("something's wrong with %s:%d. Exception is %s" % ('localhost', self.port, e))
            self.sock.close()

        self.send("CONNECT:" + ("0" if self.is_ghost else "1"))

    def send(self, message):
        # print("Send from " + ("ghost" if self.is_ghost else "detective") + " : " + message)
        self.sock.sendall(str.encode(message))

    def run(self):
        running = True
        while running:
            data = self.sock.recv(128)
            str_data = data.decode("utf-8")
            if str_data != "":
                print(str_data)
                self.sock.sendall(str(randrange(2)).encode())
            else:
                self.sock.close()
                running = False
        print("END")



def parse_args(argv):
    my_opts, args = getopt.getopt(argv[1:], "p:f:g:")

    port = 0
    file = ""
    is_ghost = False
    for o, a in my_opts:
        if o == '-p':
            port = int(a)
        elif o == '-f':
            file = a
        elif o == "-g":
            is_ghost = a == "True"
        else:
            print("Usage: %s -p port -f ia.py" % sys.argv[0])
    # print("IA file : %s " % file)
    return port, file, is_ghost


def main(argv):
    port, file, is_ghost = parse_args(argv)
    client = Client(port, file, is_ghost)
    client.connect()
    client.run()
    pass


if __name__ == "__main__":
    main(sys.argv)
