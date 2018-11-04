from multiprocessing import Pool, TimeoutError
import os
import sys
from Server.gameserver import Game


def run_game(index):
    game = Game(index)
    game.Run()

class Server:
    def __init__(self, max_game=4):
        self.max_game = max_game

    def start(self, num_game):
        pool = Pool(processes=self.max_game)
        pool.map(run_game, range(num_game))


def main(argv):
    server = Server()
    server.start(10)
    pass


if __name__ == "__main__":
    main(sys.argv)
