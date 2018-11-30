import random
import copy
import codecs
from Multiprocess.AI.reinforcedai import ReinforcedAI


class Ghost(ReinforcedAI):

    def __init__(self, index, is_ghost):
        super().__init__(index, is_ghost)
        self.prev_suspect = 8

    def on_turn_begins(self):
        pass

    def pick_tile(self, game, tiles):
        return random.choice(tiles)

    def get_power_choice(self, game, tile):
        character = game.board.GetCharacter(tile)
        choices = character.GetPowerChoices(game)
        return random.choice(choices)

    def get_move(self, game, tile):
        return random.choice(game.board.GetPossibleMoves(tile))

    def memorize(self):
        f = codecs.open('./memories/memories_{}_{}.txt'.format(self.id, self.is_ghost), "a", "utf-8")
        txt = ""
        for state, action, reward, next_state, done in self.memory:
            txt += str(state) + '|'
            txt += str(action) + '|'
            txt += str(reward) + '|'
            txt += str(next_state) + '|'
            txt += str(done) + '\n'
        txt += "====\n"
        f.write(txt)
        f.close()

    def play(self, line):
        # print("Ghost.play()")
        print(line)
        if line.startswith("Tuiles disponibles :"):
            if self.prev_action != -1:
                reward = self.state.count_suspect() - self.prev_state.count_suspect()
                reward = 1 if reward == 0 else reward
                self.remember(self.prev_state, self.prev_action, reward, copy.deepcopy(self.state), False)
            character = self.choose_character()
            self.prev_state = copy.deepcopy(self.state)
            self.prev_action = character
            for i in range(0, len(self.state.available)):
                if int(self.state.available[i]) == character:
                    character = i
            print(character)
            return str(character)
        if line.startswith("positions disponibles :"):
            if self.prev_action != -1:
                reward = self.state.count_suspect() - self.prev_state.count_suspect()
                reward = 1 if reward == 0 else reward
                self.remember(self.prev_state, self.prev_action, reward, copy.deepcopy(self.state), False)
            pos = self.choose_position(line)
            self.prev_state = copy.deepcopy(self.state)
            self.prev_action = pos
            pos -= 8
            print(pos)
            return str(pos)
        return super().play(line)

    def end(self):
        print(self.state.score)
        if int(self.state.score) <= 0:
            print("WIN")
            reward = 10
        else:
            reward = self.state.count_suspect() - self.prev_state.count_suspect()
            reward = 1 if reward == 0 else reward
        self.remember(self.prev_state, self.prev_action, reward, copy.deepcopy(self.state), True)
        self.memorize()
