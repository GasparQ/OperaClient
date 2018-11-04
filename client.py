class Client:
    colorMap = {
        "rose": "pink",
        "rouge": "red",
        "gris": "gray",
        "bleu": "blue",
        "voilet": "purple",
        "marron": "brown"
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
            self.shadow = ""
            self.lock1 = ""
            self.lock2 = ""
            self.players = {
                "pink": Client.Player(),
                "red": Client.Player(),
                "gray": Client.Player(),
                "blue": Client.Player(),
                "purple": Client.Player(),
                "brown": Client.Player(),
            }

        def SerialiseState(self):
            value = self.turn + ","
            value += self.shadow + ","
            value += self.lock1 + ","
            value += self.lock2 + ","
            for _, player in self.players:
                value += player.Serialise() + ","
            return value

    def __init__(self, id):
        self.id = id
        self.score = -1
        self.line = 0
        self.state = Client.State()

    """
        Read the question asked by the game
        
        @return string that contains the question
    """
    def GetQuestion(self):
        qf = open('./{}/questions.txt'.format(self.id), 'r')
        question = qf.read()
        qf.close()
        return question

    """
        Send a response to the game
        
        @param response Lambda that returns the string to send
    """
    def SendResponse(self, response):
        rf = open('./{}/reponses.txt'.format(self.id), 'w')
        rf.write(response())
        rf.close()

    """
        Check in info file if the game is over
        
        @return True if the game is over, false either
    """
    def IsGameOver(self):
        infof = open('./{}/infos.txt'.format(self.id), 'r')
        lines = infof.readlines()
        if (len(lines) != self.line):
            self.ParseNewLines(self.line, lines)
            self.line = len(lines)

        infof.close()
        if len(lines) > 0 and "Score final" in lines[-1]:
            self.score = int(lines[-1].replace('Score final : ', ''))
            return True
        return False

    def ParseNewLines(self, start, lines):
        for i in range(start, len(lines)):
            line = lines[i]
            if line == "****" and lines[i - 3] == "**************************":
                line = lines[i - 1]
                infos = line.replace(" ", "").split(",")
                self.state.turn = self.ParseSecond(infos[0])
                self.state.shadow = self.ParseSecond(infos[1])
                lock = self.ParseSecond(infos[2])
                self.state.lock1 = lock[0]
                self.state.lock2 = lock[1]
                line = lines[i - 2]
                infos = line.strip().split(" ")
                self.ParsePlayers(infos)
                print(self.state.SerialiseState())

    def ParsePlayers(self, infos):
        for info in infos:
            playerData = info.split("-")
            self.state.players[playerData[0]].pos = playerData[1]
            self.state.players[playerData[0]].suspect = "0" if playerData[2] == "suspect" else "1"

    def ParseSecond(self, txt):
        return  txt.split(":")[1]