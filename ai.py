class AI:
    def OnTurnBegins(self):
        raise NotImplemented("Method OnNewTurn is not implemented")

    def PickTile(self, game, tiles):
        raise NotImplemented("Method PickTile is not implemented")

    def GetPowerChoice(self, game, tile):
        raise NotImplemented("Method UsePowerBeforeMove is not implemented")

    def GetMove(self, game, tile):
        raise NotImplemented("Method Move is not implemented")
