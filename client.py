class Client:
    def __init__(self, id):
        self.id = id
        self.score = -1

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
        infof.close()
        if len(lines) > 0 and "Score final" in lines[-1]:
            self.score = int(lines[-1].replace('Score final : ', ''))
            return True
        return False
