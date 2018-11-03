import GAME_DATA


class Character:
    def __init__(self, color, position, innocence=True, alone=True):
        self.color = color
        self.position = position
        self.innocence = innocence
        self.alone = alone

    def SetInnocent(self):
        self.innocence = True

    def SetLoneliness(self, value):
        self.alone = value

    def GetPossibleMoves(self):
        return GAME_DATA.BASE_PATHES[self.position]

    def UsePower(self, board, data):
        raise NotImplemented("Method UsePower is not implemented")

    def GetPowerTiming(self):
        raise NotImplemented("Method GetPowerTiming is not implemented")

    def GetPowerChoices(self, board):
        raise NotImplemented("Method GetPowerChoices is not implemented")

    def Clone(self):
        raise NotImplemented("Method Clone is not implemented")


class Red(Character):
    def __init__(self, position):
        Character.__init__(self, GAME_DATA.RED, position)

    def UsePower(self, board, choice):
        raise NotImplemented("Method UsePower is not implemented")

    def GetPowerTiming(self):
        return GAME_DATA.BEFORE & GAME_DATA.AFTER

    def GetPowerChoices(self, board):
        raise NotImplemented("Method UsePower is not implemented")

    def Clone(self):
        return Red(self.position)


class Pink(Character):
    def __init__(self, position):
        Character.__init__(self, GAME_DATA.PINK, position)

    def GetPossibleMoves(self):
        return GAME_DATA.PINK_PATHES[self.position]

    def UsePower(self, board, data):
        pass

    def GetPowerTiming(self):
        return GAME_DATA.ALWAYS

    def GetPowerChoices(self, board):
        pass

    def Clone(self):
        return Pink(self.position)


class Blue(Character):
    def __init__(self, position):
        Character.__init__(self, GAME_DATA.BLUE, position)

    def UsePower(self, board, data):
        raise NotImplemented("Method UsePower is not implemented")

    def GetPowerTiming(self):
        return GAME_DATA.BEFORE & GAME_DATA.AFTER

    def GetPowerChoices(self, board):
        raise NotImplemented("Method GetPowerChoices is not implemented")

    def Clone(self):
        return Blue(self.position)


class Gray(Character):
    def __init__(self, position):
        Character.__init__(self, GAME_DATA.GRAY, position)

    def UsePower(self, board, data):
        raise NotImplemented("Method UsePower is not implemented")

    def GetPowerTiming(self):
        return GAME_DATA.BEFORE & GAME_DATA.AFTER

    def GetPowerChoices(self, board):
        raise NotImplemented("Method GetPowerChoices is not implemented")

    def Clone(self):
        return Blue(self.position)


class Black(Character):
    def __init__(self, position):
        Character.__init__(self, GAME_DATA.BLACK, position)

    def UsePower(self, board, data):
        raise NotImplemented("Method UsePower is not implemented")

    def GetPowerTiming(self):
        return GAME_DATA.AFTER

    def GetPowerChoices(self, board):
        raise NotImplemented("Method GetPowerChoices is not implemented")

    def Clone(self):
        return Blue(self.position)



class White(Character):
    def __init__(self, position):
        Character.__init__(self, GAME_DATA.WHITE, position)

    def UsePower(self, board, data):
        raise NotImplemented("Method UsePower is not implemented")

    def GetPowerTiming(self):
        return GAME_DATA.AFTER

    def GetPowerChoices(self, board):
        raise NotImplemented("Method GetPowerChoices is not implemented")

    def Clone(self):
        return Blue(self.position)



class Purple(Character):
    def __init__(self, position):
        Character.__init__(self, GAME_DATA.PURPLE, position)

    def UsePower(self, board, data):
        raise NotImplemented("Method UsePower is not implemented")

    def GetPowerTiming(self):
        return GAME_DATA.BEFORE

    def GetPowerChoices(self, board):
        raise NotImplemented("Method GetPowerChoices is not implemented")

    def Clone(self):
        return Blue(self.position)



class Brown(Character):
    def __init__(self, position):
        Character.__init__(self, GAME_DATA.BROWN, position)

    def UsePower(self, board, data):
        raise NotImplemented("Method UsePower is not implemented")

    def GetPowerTiming(self):
        return GAME_DATA.BEFORE

    def GetPowerChoices(self, board):
        raise NotImplemented("Method GetPowerChoices is not implemented")

    def Clone(self):
        return Blue(self.position)

