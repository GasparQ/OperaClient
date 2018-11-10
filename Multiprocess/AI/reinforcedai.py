import random
import numpy as np
from collections import deque
from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import Adam
import copy
from Multiprocess.AI.ai import AI


class ReinforcedAI(AI):

    def __init__(self, index, is_ghost, train):
        super().__init__(index, is_ghost, train)
        self.memory = deque(maxlen=2000)
        self.gamma = 0.95

        self.epsilon = 1
        self.epsilon_decay = 0.995
        self.epsilon_min = 0.01

        self.learning_rate = 0.01
        self.model = self._build_model()
        self.prev_action = -1
        self.prev_state = -1

    def _build_model(self):

        model = Sequential()

        model.add(Dense(32, input_shape=(3, ), activation='relu'))
        model.add(Dense(32, activation='relu'))
        model.add(Dense(8, activation='linear'))

        model.compile(loss='mse', optimizer=Adam(lr=self.learning_rate))
        return model

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

    def pick_random_choice(self, choices, available):
        dice = random.randrange(0, available)
        j = 0
        for i in range(0, len(choices)):
            if choices[i] == 1:
                if dice == j:
                    return i
                j += 1
        return -1

    def choose_character(self):
        # print(line + " -> " + str(self.state))
        # Get available suspect to play
        available = self.state.available
        actions_turn_0 = [0, 0, 0, 0, 0, 0, 0, 0]
        available_len = range(0, len(available))
        # percent = float(len(available)) / float(len(actions_turn_0))
        for i in range(0, len(actions_turn_0)):
            for j in available_len:
                if int(available[j]) == i:
                    actions_turn_0[i] = 1
                j += 1
            i += 1
        if np.random.rand() <= self.epsilon:
            choice = self.pick_random_choice(actions_turn_0, len(available))
        else:
            actions = self.model.predict(self.state.to_numpy())
            choice = np.argmax(actions)
        for i in range(0, len(available)):
            if int(available[i]) == choice:
                return i
        return 0

    def choose_position(self, line):
        pass

    def memorize(self):
        raise NotImplemented("Method on_new_turn is not implemented")

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def replay(self, batch_size):

        minibatch = random.sample(self.memory, batch_size)

        for state, action, reward, next_state, done in minibatch:
            target = reward
            if not done:
                target = (reward + self.gamma * np.amax(self.model.predict(next_state)[0]))
            target_f = self.model.predict(state)
            target_f[0][action] = target

            self.model.fit(state, target_f, epochs=1, verbose=0)

        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

    def load(self, path):
        self.model.load_weights(path)

    def save(self, path):
        self.model.save_weights(path)

    def play(self, line):
        # print("ReinforcedAI.play()")
        return str(random. randrange(2))

