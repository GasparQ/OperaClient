import collections
import codecs


class AI:
    colorMap = {
        "rose": "pink",
        "rouge": "red",
        "gris": "gray",
        "bleu": "blue",
        "violet": "purple",
        "marron": "brown",
        "noir": "black",
        "blanc": "white"
    }

    class Player:
        def __init__(self):
            self.pos = ""
            self.alone = ""
            self.suspect = ""

        def Serialise(self):
            value = self.pos + ","
            value += self.alone + ","
            value += self.suspect
            return value

    class State:
        def __init__(self):
            self.turn = ""
            self.score = ""
            self.shadow = ""
            self.lock1 = ""
            self.lock2 = ""
            self.players = collections.OrderedDict()
            self.players["black"] = AI.Player()
            self.players["blue"] = AI.Player()
            self.players["brown"] = AI.Player()
            self.players["gray"] = AI.Player()
            self.players["pink"] = AI.Player()
            self.players["purple"] = AI.Player()
            self.players["red"] = AI.Player()
            self.players["white"] = AI.Player()

        def serialise_state(self):
            value = self.turn + ","
            value += self.score + ","
            value += self.shadow + ","
            value += self.lock1 + ","
            value += self.lock2 + ","
            for player in self.players.values():
                value += player.Serialise() + ","
            return value[:-1]

    def __init__(self, index, is_ghost):
        self.id = index
        self.is_ghost = is_ghost
        self.score = -1
        self.line = 0
        self.state = AI.State()
        self.check_turn = False
        codecs.open('./states_{}_{}.txt'.format(self.id, self.is_ghost), "w", "utf-8").close()
        self.log = codecs.open('./states_{}_{}.txt'.format(self.id, self.is_ghost), "a", "utf-8")

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

    def parse_turn(self, data):
        info = data.replace(" ", "").split(",", 3)
        self.state.turn = self.parse_second(info[0])
        self.state.score = self.parse_second(info[1]).split("/")[0]
        self.state.shadow = self.parse_second(info[2])
        lock = self.parse_second(info[3]).replace("{", "").replace("}", "").split(",")
        self.state.lock1 = lock[0]
        self.state.lock2 = lock[1]

    def parse_suspect(self, data):
        info = data.split("  ")
        self.parse_players(info)
        self.update_alone_states()
        self.update_state_file()

    def parse_new_pos(self, data):
        suspect = data.replace(" ", "").split(":")[1]
        info = suspect.split("-")
        self.state.players[AI.colorMap[info[0]]].pos = info[1]
        self.update_state_file()

    def parse_new_line(self, start, lines):
        for i in range(start, len(lines)):
            line = lines[i].rstrip()
            if line == "**************************":
                self.check_turn = True
            elif line == "****":
                self.check_turn = False
            elif self.check_turn:
                if line.startswith("Tour"):
                    self.parse_turn(line)
                else:
                    self.parse_suspect(line)
            elif line.startswith("NOUVEAU PLACEMENT"):
                self.parse_new_pos(line)

    def parse_second(self, txt):
        return txt.split(":")[1]

    def parse_players(self, infos):
        for info in infos:
            player_data = info.split("-")
            self.state.players[AI.colorMap[player_data[0]]].pos = player_data[1]
            self.state.players[AI.colorMap[player_data[0]]].suspect = "0" if player_data[2] == "suspect" else "1"

    def update_alone_states(self):
        for player in self.state.players.values():
            pos = player.pos
            player.alone = "1"
            for others in self.state.players.values():
                if others != player and others.pos == pos:
                    player.alone = "0"
                    break

    def update_state_file(self):
        state = self.state.serialise_state()
        self.log.write(state + "\n")

    def update_state(self):
        infos = open('./log_game_{}.txt'.format(self.id), 'r')
        lines = infos.readlines()
        if len(lines) != self.line:
            self.parse_new_line(self.line, lines)
            self.line = len(lines)
        infos.close()

    def close(self):
        self.log.close()
