from client import Client
from game import Board, Game
from dumb_ai import DumbAI
import GAME_DATA

#phantom = Client(0)
#inspector = Client(1)

# get the question in q variable
# q = phantom.GetQuestion()

# send response OK from the lambda
# phantom.SendResponse(lambda: 'Ok')

# print finish if the game is over
# if phantom.IsGameOver():
#     print('finish')

game = Game(Board(), [DumbAI(), DumbAI()])

print(game.board)

while not game.IsOver():
    tiles = game.PickTiles()

    for p in game.players:
        game.players.OnTurnBegins()

    game.PlayTurn(GAME_DATA.INSPECTOR_PLAYER, tiles)
    game.PlayTurn(GAME_DATA.PHANTOM_PLAYER, tiles)
    game.PlayTurn(GAME_DATA.PHANTOM_PLAYER, tiles)
    game.PlayTurn(GAME_DATA.INSPECTOR_PLAYER, tiles)

    game.board.MoveSinger()

    game.InnocentCharacters()

    print(game.board)

print('Game Over: ', game.board.singer, '/22')

print('Phantom: ', GAME_DATA.TILE_NAMES[game.board.phantom])