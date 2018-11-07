class AI:
    def on_turn_begins(self):
        raise NotImplemented("Method on_new_turn is not implemented")

    def pick_tile(self, game, tiles):
        raise NotImplemented("Method pick_tile is not implemented")

    def get_power_choice(self, game, tile):
        raise NotImplemented("Method get_power_choice is not implemented")

    def get_move(self, game, tile):
        raise NotImplemented("Method get_move is not implemented")

    def play(self, line):
        raise NotImplemented("Method play is not implemented")
