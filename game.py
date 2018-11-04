import random
import GAME_DATA
import characters


class Board:
    def __init__(self, singer=0):
        # list<Character> : available characters
        self.characters = [
            characters.Red(),
            characters.Pink(),
            characters.Blue(),
            characters.Gray(),
            characters.Black(),
            characters.White(),
            characters.Purple(),
            characters.Brown()
        ]

        # int : position of the singer
        self.singer = singer

        # int : max score that can be reached by the singer
        self.maxScore = 22

        # dict<int, list<Character>> : characters by room
        self.rooms = {i: [] for i in range(10)}
        chars = [GAME_DATA.RED, GAME_DATA.PINK, GAME_DATA.BLUE,
                 GAME_DATA.GRAY, GAME_DATA.BLACK, GAME_DATA.WHITE,
                 GAME_DATA.PURPLE, GAME_DATA.BROWN]
        random.shuffle(chars)
        for i in chars:
            self.rooms[i].append(self.characters[i])
            self.characters[i].position = i

        # tuple(int, int) : tuple of int that represents the path between rooms
        bluepos = self.characters[GAME_DATA.BLUE].position
        self.lock = (bluepos, GAME_DATA.BASE_PATHES[bluepos][0])

        # int : index of the room
        self.shadow = self.characters[GAME_DATA.GRAY].position

        # int : color of the phantom
        self.phantom = random.choice([GAME_DATA.RED, GAME_DATA.PINK, GAME_DATA.BLUE,
                                      GAME_DATA.GRAY, GAME_DATA.BLUE, GAME_DATA.WHITE,
                                      GAME_DATA.PURPLE, GAME_DATA.BROWN])

    def GetPossibleMoves(self, color):
        # Get possible moves of the player minus locked door
        character = self.GetCharacter(color)
        moves = character.GetPossibleMoves()
        if character.position in self.lock:
            moves = [move for move in moves if move not in self.lock]
        return moves

    def GetCharacter(self, color):
        return self.characters[color]

    def MovePlayer(self, color, newPos):
        character = self.GetCharacter(color)

        if character.position in self.lock and newPos in self.lock:
            return

        self.rooms[character.position].remove(character)

        if len(self.rooms[character.position]) == 1:
            self.rooms[character.position][0].alone = True

        self.rooms[newPos].append(character)
        character.position = newPos

        if len(self.rooms[newPos]) == 1 or newPos == self.shadow:
            character.alone = True
        else:
            for character in self.rooms[newPos]:
                character.alone = False

    def MoveShadow(self, newPos):
        if len(self.rooms[self.shadow]) > 1:
            for character in self.rooms[self.shadow]:
                character.alone = False
        self.shadow = newPos
        for character in self.rooms[newPos]:
            character.alone = True

    def MoveLock(self, newPos):
        self.lock = newPos

    def MoveSinger(self):
        for character in self.characters:
            if not character.innocent:
                self.singer += 1
        if self.GetCharacter(self.phantom).alone:
            self.singer += 1

    def Clone(self):
        board = Board(self.singer)

        for character in self.characters:
            board.MovePlayer(character.color, character.position)
            if character.innocent:
                board.GetCharacter(character.color).SetInnocent()

        board.MoveLock((self.lock[0], self.lock[1]))
        board.MoveShadow(self.shadow)

        board.phantom = self.phantom
        return board

    def __repr__(self):
        return ','.join([
            "{}-{}-{}".format(
                char.position,
                GAME_DATA.TILE_NAMES[char.color],
                'clean' if char.innocent else 'suspect'
            ) for char in self.characters
        ])


class Game:
    def __init__(self, board, players):
        self.board = board

        self.players = players

        self.phantomFound = False

        # int : represent the player who is currently playing
        self.currentPlayer = random.choice([GAME_DATA.PHANTOM_PLAYER, GAME_DATA.INSPECTOR_PLAYER])

        # set<int> : set of tiles used at each turn
        self.tiles = {}

        # set<int> : set of alibi cards used for red player
        self.alibis = [GAME_DATA.RED, GAME_DATA.PINK, GAME_DATA.BLUE,
                       GAME_DATA.GRAY, GAME_DATA.BLUE, GAME_DATA.WHITE,
                       GAME_DATA.PURPLE, GAME_DATA.BROWN, GAME_DATA.PHANTOM,
                       GAME_DATA.PHANTOM, GAME_DATA.PHANTOM]
        self.alibis.remove(board.phantom)
        random.shuffle(self.alibis)

    def PickTiles(self):
        if len(self.tiles) == 0:
            self.tiles = [GAME_DATA.RED, GAME_DATA.PINK, GAME_DATA.BLUE,
                          GAME_DATA.GRAY, GAME_DATA.BLUE, GAME_DATA.WHITE,
                          GAME_DATA.PURPLE, GAME_DATA.BROWN]
            random.shuffle(self.tiles)
        tiles = self.tiles[:4]
        self.tiles = self.tiles[4:]
        return tiles

    def PickAlibi(self):
        return self.alibis.pop(0)

    def IsOver(self):
        return self.board.singer >= self.board.maxScore or self.phantomFound

    def InnocentCharacters(self):
        phantomAlone = self.board.GetCharacter(self.board.phantom).alone
        nbSuspect = len(self.board.characters)

        for character in self.board.characters:
            if character.alone != phantomAlone:
                character.SetInnocent()
            if character.innocent:
                nbSuspect -= 1
        self.phantomFound = (nbSuspect == 1)

    def PlayTurn(self, player, tiles):
        p = self.players[player]
        tile = p.PickTile(tiles)
        tiles.remove(tile)
        char = self.board.GetCharacter(tile)

        print('Player', GAME_DATA.PLAYER_NAMES[player],
              'pick tile', GAME_DATA.TILE_NAMES[tile])

        self.currentPlayer = player

        # pre power AI
        if char.GetPowerTiming() & GAME_DATA.BEFORE:
            choice = p.GetPowerChoice(self, tile)
            char.UsePower(self, choice)

        # move AI
        move = p.GetMove(self, tile)
        self.board.MovePlayer(tile, move)

        # post power AI
        if char.GetPowerTiming() & GAME_DATA.AFTER:
            choice = p.GetPowerChoice(self, tile)
            char.UsePower(self, choice)

    def Clone(self):
        game = Game(self.board.Clone(), self.players)
        game.currentPlayer = self.currentPlayer
        game.tiles = self.tiles
        game.alibis = self.alibis
        game.phantomFound = self.phantomFound
        return game
