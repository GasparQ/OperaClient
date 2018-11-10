import random

import GAME_DATA
from ai import AI
import action


class MonsterPiece(AI):
    def __init__(self):
        self.possibleActions = None
        self.values = {}
        for i in range(0, 9):
            for j in range(0, 9):
                for k in range(0, 9):
                    for l in range(0, 9):
                        self.values['{}-{}-{}-{}'.format(i / 8.0, j / 8.0, k / 8.0, l / 8.0)] = 0.0
        self.transitions = []
        self.epsilon = 0.9
        self.choosenAction = None
        self.moved = False
        self.turns = 0

    """
        Train the model
        Updates values for each states from a given reward
    """
    def OnTurnEnds(self, game):
        reward = self.GetReward(game)
        self.UpdateValues(reward)
        self.UpdateEpsilon()

    """
        Generates the possible actions for a turn and pick one in function of values
    """
    def OnMiniTurnBegins(self, game, tilesLeft):
        self.GeneratePossibleActions(game, tilesLeft)
        self.ChooseAction()
        self.moved = False

    def SaveTo(self, filename):
        file = open(filename, 'w')
        print(self.epsilon, file=file)
        for key, value in self.values.items():
            print("{} {}", key, value, file=file)
        file.close()

    def LoadFrom(self, filename):
        file = open(filename, 'r')
        self.epsilon = float(file.readline())
        lines = file.readline()
        for line in lines:
            key, value = line.split(' ')
            self.values[key] = float(value)
        file.close()

    @staticmethod
    def GetPowerStates(actions, character, which):
        newActions = []
        for curract in actions:
            choices = character.GetPowerChoices(curract.state)
            for choice in choices:
                currAction = curract.Clone()
                currAction.next_state = currAction.state.Clone()
                currAction.actions[which] = choice
                character.UsePower(curract.next_state, choice)
                newActions.append(currAction)
        return newActions

    @staticmethod
    def GetMovesStates(actions, character):
        newActions = []
        for curract in actions:
            moves = curract.board.GetPossibleMoves(character.color)
            for move in moves:
                currAction = curract.Clone()
                currAction.actions[action.MOVE] = move
                currAction.next_state = currAction.state.Clone()
                currAction.next_state.board.MovePlayer(character.color, move)
                newActions.append(currAction)
        return newActions

    def GeneratePossibleActions(self, game, tilesLeft):
        self.possibleActions = []

        for tile in tilesLeft:
            actions = [action.Action(game, [tile, None, None, None], game)]
            character = game.board.GetCharacter(tile)

            if character.GetPowerTiming() & GAME_DATA.BEFORE:
                actions = MonsterPiece.GetPowerStates(actions, character, action.PRE_POWER)

            actions = MonsterPiece.GetMovesStates(actions, character)

            if character.GetPowerTiming() & GAME_DATA.AFTER:
                actions = MonsterPiece.GetPowerStates(actions, character, action.POST_POWER)

            self.possibleActions += actions

    def ChooseAction(self):
        if random.uniform(0, 1) < self.epsilon:
            self.choosenAction = random.choice(self.possibleActions)
        else:
            self.choosenAction = None
            maxValue = 0
            for currAct in self.possibleActions:
                val = self.values[currAct.next_state.board.GetStateHash()]
                if self.choosenAction is None or val > maxValue:
                    maxValue = val
                    self.choosenAction = currAct
        self.transitions.append(self.choosenAction)

    def GetReward(self, game):
        raise NotImplemented("Method GetReward is not implemented")

    def UpdateValues(self, reward):
        for transition in reversed(self.transitions):
            state_hash = transition.state.board.GetStateHash()
            next_state_hash = transition.next_state.board.GetStateHash()
            if reward == 0:
                self.values[state_hash] += 0.001 * (self.values[next_state_hash] - self.values[state_hash])
            else:
                self.values[state_hash] += 0.001 * (reward - self.values[state_hash])

        self.transitions = []

    def UpdateEpsilon(self):
        self.turns += 1
        if self.turns % 10 == 0:
            self.turns = 0
            self.epsilon = max(self.epsilon * 0.9, 0.05)

    def PickTile(self, game, tiles):
        return self.choosenAction.actions[action.PICK]

    def GetPowerChoice(self, game, tile):
        if self.moved:
            return self.choosenAction.actions[action.POST_POWER]
        return self.choosenAction.actions[action.PRE_POWER]

    def GetMove(self, game, tile):
        self.moved = True
        return self.choosenAction.actions[action.MOVE]
