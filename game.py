class Character:
    def __init__(self, color, position, innocence, loneliness):
        self.color = color
        self.position = position
        self.innocence = innocence
        self.loneliness = loneliness

    def Clone(self):
        return Character(self.color, self.position, self.innocence, self.loneliness)


class Board:
    def __init__(self, characters, lock, shadow, singer):
        self.characters = characters
        self.lock = lock
        self.shadow = shadow
        self.singer = singer

    def InnocentPlayer(self, color):
        self.characters[color].innocence = True

    def GetPossibleMoves(self, color):
        pass

    def SetPlayerLoneliness(self, color, loneliness):
        self.characters[color].loneliness = loneliness

    def MovePlayer(self, color, newPos):
        self.characters[color].position = newPos

    def MoveShadow(self, newPos):
        self.shadow = newPos

    def MoveLock(self, newPos):
        self.lock = newPos

    def MoveSinger(self, count):
        self.singer += count

    def Clone(self):
        return Board([self.characters[i].Clone() for i in self.characters], self.lock, self.shadow, self.singer)


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
