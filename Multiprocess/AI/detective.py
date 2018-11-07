from Multiprocess.AI.ai import AI
import random


class Detective(AI):
    def on_turn_begins(self):
        pass

    def pick_tile(self, game, tiles):
        return random.choice(tiles)

    def get_power_choice(self, game, tile):
        character = game.board.GetCharacter(tile)
        choices = character.GetPowerChoices(game)
        return random.choice(choices)

    def get_move(self, game, tile):
        return random.choice(game.board.GetPossibleMoves(tile))

    def play(self, line):
        print("Detective : " + line)
        return str(random.randrange(6))
