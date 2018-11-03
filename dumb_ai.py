from ai import AI
import random


class DumbAI(AI):
    def PickTile(self, tiles):
        return random.choice(tiles)

    def GetPowerChoice(self, game, tile):
        character = game.board.GetCharacter(tile)
        choices = character.GetPowerChoices(game)
        return random.choice(choices)

    def GetMove(self, game, tile):
        return random.choice(game.board.GetPossibleMoves(tile))
