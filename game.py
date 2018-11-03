import random
import GAME_DATA


class Board:
    def __init__(self, characters, lock, shadow, singer):
        # list<Character> : available characters
        self.characters = characters

        # tuple(int, int) : tuple of int that represents the path between rooms
        self.lock = lock

        # int : index of the room
        self.shadow = shadow

        # int : position of the singer
        self.singer = singer

        # dict<int, list<Character>> : characters by room
        self.rooms = {i: [] for i in range(8)}
        for i in characters:
            self.rooms[characters[i].position].append(characters[i])

        self.currentPlayer = random.choice(GAME_DATA.PHANTOM_PLAYER, GAME_DATA.INSPECTOR_PLAYER)

        self.phantom = random.choice(GAME_DATA.RED, GAME_DATA.PINK, GAME_DATA.BLUE,
                                     GAME_DATA.GRAY, GAME_DATA.BLUE, GAME_DATA.WHITE,
                                     GAME_DATA.PURPLE, GAME_DATA.BROWN)
        self.tiles = {}
        self.alibis = random.shuffle([GAME_DATA.RED, GAME_DATA.PINK,
                                      GAME_DATA.BLUE, GAME_DATA.GRAY,
                                      GAME_DATA.BLUE, GAME_DATA.WHITE,
                                      GAME_DATA.PURPLE, GAME_DATA.BROWN,
                                      GAME_DATA.PHANTOM, GAME_DATA.PHANTOM,
                                      GAME_DATA.PHANTOM])

    def PickTiles(self):
        if len(self.tiles) == 0:
            self.tiles = random.shuffle({GAME_DATA.RED, GAME_DATA.PINK,
                                         GAME_DATA.BLUE, GAME_DATA.GRAY,
                                         GAME_DATA.BLUE, GAME_DATA.WHITE,
                                         GAME_DATA.PURPLE, GAME_DATA.BROWN})
        tiles = self.tiles[:4]
        self.tiles = self.tiles[4:]
        return tiles

    def PickAlibi(self):
        return self.alibis.pop(0)

    def ReplaceAlibisCards(self, cards):
        self.alibis += cards
        self.alibis = random.shuffle(self.alibis)

    def GetPossibleMoves(self, color):
        # Get possible moves of the player minus locked door
        character = self.GetCharacter(color)
        moves = character.GetPossibleMoves()
        if character.position in self.lock:
            moves = {moves[i] for i in moves if moves[i] not in self.lock}
        return moves

    def GetCharacter(self, color):
        return self.characters[color]

    def MovePlayer(self, color, newPos):
        character = self.GetCharacter(color)
        self.rooms[character.position].remove(character)

        if len(self.rooms[character.position]) == 1:
            self.rooms[character.position][0].alone = True

        self.rooms[newPos].append(character)
        character.position = newPos

        if len(self.rooms[newPos]) == 1 or newPos == self.shadow:
            character.alone = True
        else:
            for i in self.rooms[newPos]:
                self.rooms[newPos][i].alone = False

    def MoveShadow(self, newPos):
        if len(self.rooms[self.shadow]) > 1:
            for i in self.rooms[self.shadow]:
                self.rooms[self.shadow][i].alone = False
        self.shadow = newPos
        for i in self.rooms[newPos]:
            self.rooms[newPos][i].alone = True

    def MoveLock(self, newPos):
        self.lock = newPos

    def MoveSinger(self):
        for i in self.characters:
            if not self.characters[i].innocent:
                self.singer += 1
        if self.GetCharacter(self.phantom).alone:
            self.singer += 1

    def Clone(self):
        return Board([self.GetCharacter(i).Clone() for i in self.characters], self.lock, self.shadow, self.singer)


class State:
    def __init__(self, board, children):
        self.board = board
        self.children = children

    def GenerateStates(self, color):
        pass

    def GenerateMoveStates(self):
        # need all possible moves for a given player
        pass

    def GenerateRedStates(self):
        pass

    def GeneratePinkStates(self):
        pass

    def GenerateBlueStates(self):
        pass

    def GenerateGrayStates(self):
        pass

    def GenerateBlackStates(self):
        pass

    def GenerateWhiteStates(self):
        pass

    def GeneratePurpleStates(self):
        pass

    def GenerateBrownStates(self):
        pass
