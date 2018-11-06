import sys
from Multiprocess.game import Game
from threading import Thread


class Server:
    def __init__(self, index):
        self.index = index
        self.game = None

    def start(self):
        game = Game(self.index)
        port = game.start_game()
        thread = Thread(target=game.run, args=())
        thread.start()
        print("PORT:" + str(port))
        thread.join()
        print("END SERVER")


def main(argv):
    server = Server(argv[1])
    server.start()


if __name__ == "__main__":
    main(sys.argv)
