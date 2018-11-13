import sys
from Multiprocess.game import Game
from threading import Thread
import getopt

class Server:
    def __init__(self, index):
        self.index = index
        self.game = None

    def start(self, batches):
        game = Game(self.index)
        port = game.start_game()
        thread = Thread(target=game.run, args=(batches,))
        thread.start()
        print("PORT:" + str(port))
        thread.join()
        print("END SERVER")


def parse_args(argv):
    my_opts, args = getopt.getopt(argv[1:], "b:i:")

    batches = 1
    index = 0
    for o, a in my_opts:
        if o == '-b':
            batches = int(a)
        elif o == '-i':
            index = int(a)
        else:
            print("Usage: %s -b batches" % sys.argv[0])
    # print("IA file : %s " % file)
    return batches, index


def main(argv):
    batches, index = parse_args(argv)
    server = Server(index)
    server.start(batches)


if __name__ == "__main__":
    main(sys.argv)
