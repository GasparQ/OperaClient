from ai import AI
from tree import Tree


class MonsterPiece(AI):
    def __init__(self):
        self.decisionTree = Tree()

    def OnTurnBegins(self):
        # generate descision tree
        pass

    def PickTile(self, game, tiles):
        # update position on tree
        # take decision from it
        pass

    def GetPowerChoice(self, game, tile):
        # from decision tree choose power
        pass

    def GetMove(self, game, tile):
        # from decision tree choose move
        pass
