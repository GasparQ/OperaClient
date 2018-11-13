import os
import random
import sys
from collections import deque
import numpy as np
from Multiprocess.AI.ai import AI
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
stderr = sys.stderr
sys.stderr = open(os.devnull, 'w')
from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import Adam
import keras
sys.stderr = stderr


class ReinforcedAI(AI):

    def __init__(self, index, is_ghost, epsilon=1, gamma=0.95, epsilon_min=0.01, learning_rate=1):
        super().__init__(index, is_ghost)
        self.memory = deque()
        self.gamma = gamma

        self.epsilon = epsilon
        self.epsilon_decay = 0.995
        self.epsilon_min = epsilon_min

        self.learning_rate = learning_rate
        self.model = self._build_model()
        # self.model.summary()
        # self.load('./weights/weight_{}_{}_{}.hdf5'.format(self.id, self.is_ghost, 17627))
        self.prev_action = -1
        self.prev_state = -1

    def reset(self):
        super().reset()
        self.memory = deque()
        self.gamma = 0.95

        self.epsilon = 1
        self.epsilon_decay = 0.995
        self.epsilon_min = 0.01

        self.learning_rate = 1
        self.model = self._build_model()
        # self.model.summary()
        # self.load('./weights/weight_{}_{}_{}.hdf5'.format(self.id, self.is_ghost, 17627))
        self.prev_action = -1
        self.prev_state = -1

    def _build_model(self):

        model = Sequential()

        model.add(Dense(32, input_shape=(1,), activation='relu'))
        model.add(Dense(128, activation='relu'))
        model.add(Dense(18, activation='softmax'))

        model.compile(loss='categorical_crossentropy', optimizer=Adam(lr=self.learning_rate))

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
        actions_turn_0 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
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
            x = self.state.to_numpy()
            actions = self.model.predict(x)
            choice = np.argmax(actions[0])
        return choice

    def choose_position(self, line):
        available = line.replace(", choisir la valeur", "").split(":")[1].replace(" ", "").replace("{", "").replace("}", "").split(",")
        actions_turn_0 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        available_len = range(0, len(available))
        for i in range(8, len(actions_turn_0)):
            for j in available_len:
                if int(available[j]) == i - 8:
                    actions_turn_0[i] = 1
                j += 1
            i += 1
        if np.random.rand() <= self.epsilon:
            choice = self.pick_random_choice(actions_turn_0, len(available))
        else:
            actions = self.model.predict(self.state.to_numpy())[0]
            choice = np.argmax(actions)
        return choice

    def memorize(self):
        raise NotImplemented("Method on_new_turn is not implemented")

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    class LossHistory(keras.callbacks.Callback):
        def on_train_begin(self, logs={}):
            self.losses = []

        def on_batch_end(self, batch, logs={}):
            self.losses.append(logs.get('loss'))

    def replay_from_file(self):
        f = open('./memories/memories_{}_{}.txt'.format(self.id, self.is_ghost), "r")
        lines = f.readlines()
        total = 6631
        for line in lines:
            line = line[:-1]
            if line == "====":
                if total != 0 and total % 200 == 0:
                    self.save('./weights/weight_{}_{}_{}.hdf5'.format(self.id, self.is_ghost, total))
                history = self.replay(len(self.memory))
                print("bacth", total, "loss", history.losses)
                self.memory.clear()
                total += 1
            else:
                tmp = line.split("|")
                s0 = AI.State()
                s0.from_csv(tmp[0])
                a = int(tmp[1])
                r = int(tmp[2])
                s1 = AI.State()
                s1.from_csv(tmp[3])
                self.remember(s0.to_numpy(), a, r, s1.to_numpy(), True if tmp[4] == "True" else False)
        f.close()
        self.save('./weight_{}_{}_{}.hdf5'.format(self.id, self.is_ghost, total))
        self.close()
        self.end()
        print("END")

    def replay(self, batch_size):

        minibatch = random.sample(self.memory, batch_size)
        history = ReinforcedAI.LossHistory()
        for state, action, reward, next_state, done in minibatch:
            target = reward
            if not done:
                target = (reward + self.gamma * np.amax(self.model.predict(next_state)[0]))
            target_f = self.model.predict(state)
            target_f[0][action] = target

            self.model.fit(state, target_f, epochs=1, verbose=0, callbacks=[history])
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay
        return history

    def load(self, path):
        self.model.load_weights(path)

    def save(self, path):
        self.model.save_weights(path)

    def play(self, line):
        # print("ReinforcedAI.play()")
        return str(random. randrange(2))

