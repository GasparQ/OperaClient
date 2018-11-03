import GAME_DATA
from tree import Tree


class Character:
    def __init__(self, color, position=0, innocent=False, alone=True):
        self.color = color
        self.position = position
        self.innocent = innocent
        self.alone = alone

    def SetInnocent(self):
        self.innocent = True

    def SetAlone(self, value):
        self.alone = value

    def GetPossibleMoves(self):
        return GAME_DATA.BASE_PATHES[self.position]

    def UsePower(self, game, choice):
        raise NotImplemented("Method UsePower is not implemented")

    def GetPowerTiming(self):
        raise NotImplemented("Method GetPowerTiming is not implemented")

    def GetPowerChoices(self, game):
        raise NotImplemented("Method GetPowerChoices is not implemented")

    def Clone(self):
        raise NotImplemented("Method Clone is not implemented")


class Red(Character):
    def __init__(self):
        Character.__init__(self, GAME_DATA.RED)

    def UsePower(self, game, choice):
        alibi = game.PickAlibi()

        if game.currentPlayer == GAME_DATA.PHANTOM_PLAYER:
            if alibi == GAME_DATA.PHANTOM:
                game.board.singer += 1
        else:
            if alibi == GAME_DATA.PHANTOM:
                game.board.singer -= 1
            else:
                game.board.GetCharacter(alibi).SetInnocent()

    def GetPowerTiming(self):
        return GAME_DATA.BEFORE & GAME_DATA.AFTER

    def GetPowerChoices(self, board):
        pass

    def Clone(self):
        return Red()


class Pink(Character):
    def __init__(self):
        Character.__init__(self, GAME_DATA.PINK)

    def GetPossibleMoves(self):
        return GAME_DATA.PINK_PATHES[self.position]

    def UsePower(self, board, data):
        pass

    def GetPowerTiming(self):
        return GAME_DATA.ALWAYS

    def GetPowerChoices(self, board):
        pass

    def Clone(self):
        return Pink()


class Blue(Character):
    def __init__(self):
        Character.__init__(self, GAME_DATA.BLUE)

    def UsePower(self, game, choice):
        game.board.lock = choice

    def GetPowerTiming(self):
        return GAME_DATA.BEFORE & GAME_DATA.AFTER

    def GetPowerChoices(self, game):
        choices = []
        for room in range(10):
            for path in GAME_DATA.BASE_PATHES[room]:
                choices.append((room, path))
        return choices

    def Clone(self):
        return Blue()


class Gray(Character):
    def __init__(self):
        Character.__init__(self, GAME_DATA.GRAY)

    def UsePower(self, game, choice):
        game.board.shadow = choice

    def GetPowerTiming(self):
        return GAME_DATA.BEFORE & GAME_DATA.AFTER

    def GetPowerChoices(self, game):
        choices = [i for i in range(10)]
        choices.remove(game.board.shadow)
        return choices

    def Clone(self):
        return Gray()


class Black(Character):
    def __init__(self):
        Character.__init__(self, GAME_DATA.BLACK)

    def UsePower(self, game, choice):
        if choice:
            for adjacent in GAME_DATA.BASE_PATHES[self.position]:
                for char in game.board.rooms[adjacent]:
                    game.board.MovePlayer(char.color, self.position)

    def GetPowerTiming(self):
        return GAME_DATA.AFTER

    def GetPowerChoices(self, game):
        return [False, True]

    def Clone(self):
        return Black()


class White(Character):
    def __init__(self):
        Character.__init__(self, GAME_DATA.WHITE)

    def UsePower(self, game, choice):
        for char in choice:
            game.board.MovePlayer(char[0], char[1])

    def GetPowerTiming(self):
        return GAME_DATA.AFTER

    def GetPowerChoices(self, game):
        root = Tree()
        choices = [root]

        for character in game.board.rooms[self.position]:
            if character.color != self.color:
                nextchoices = []
                for choice in choices:
                    for room in GAME_DATA.BASE_PATHES[self.position]:
                        child = Tree((self.color, room), choice)
                        nextchoices.append(child)
                        choice.children.append(child)
                choices = nextchoices
        finalChoices = []
        for choice in choices:
            choiceLvl = []
            currChoice = choice
            while currChoice != root:
                choiceLvl.append(currChoice.data)
                currChoice = currChoice.parent
            finalChoices.append(choiceLvl)
        return finalChoices

    def Clone(self):
        return White()


class Purple(Character):
    def __init__(self):
        Character.__init__(self, GAME_DATA.PURPLE)

    def UsePower(self, game, choice):
        currPos = self.position
        selected = game.board.GetCharacter(choice)
        game.board.MovePlayer(self.color, selected.position)
        game.board.MovePlayer(selected.color, currPos)

    def GetPowerTiming(self):
        return GAME_DATA.BEFORE

    def GetPowerChoices(self, game):
        return [GAME_DATA.RED, GAME_DATA.PINK, GAME_DATA.BLUE,
                GAME_DATA.GRAY, GAME_DATA.BLACK, GAME_DATA.WHITE,
                GAME_DATA.BROWN]

    def Clone(self):
        return Purple()


class Brown(Character):
    def __init__(self):
        Character.__init__(self, GAME_DATA.BROWN)

    def UsePower(self, game, choice):
        if choice:
            game.board.MovePlayer(choice, self.position)

    def GetPowerTiming(self):
        return GAME_DATA.BEFORE

    def GetPowerChoices(self, game):
        return [False] + [char.color for char in game.board.rooms[self.position] if char.color != self.color]

    def Clone(self):
        return Brown()
