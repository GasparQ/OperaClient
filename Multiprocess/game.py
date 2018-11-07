import socket
import codecs
from random import shuffle,randrange

permanents, deux, avant, apres = {'rose'}, {'rouge', 'gris', 'bleu'}, {'violet', 'marron'}, {'noir', 'blanc'}
couleurs = avant | permanents | apres | deux
passages = [{1, 4}, {0, 2}, {1, 3}, {2, 7}, {0, 5, 8}, {4, 6}, {5, 7}, {3, 6, 9}, {4, 9}, {7, 8}]
pass_ext = [{1, 4}, {0, 2, 5, 7}, {1, 3, 6}, {2, 7}, {0, 5, 8, 9}, {4, 6, 1, 8}, {5, 7, 2, 9}, {3, 6, 9, 1},
            {4, 9, 5}, {7, 8, 4, 6}]


class Character:
    def __init__(self, color):
        self.color, self.suspect, self.position, self.pouvoir = color, True, 0, True

    def __repr__(self):
        susp = "-suspect" if self.suspect else "-clean"
        return self.color + "-" + str(self.position) + susp


class Player:
    def __init__(self, n, game):
        self.numero = n
        self.game = game
        self.role = "l'inspecteur" if n == 0 else "le fantome"

    def play(self, party):
        self.game.informer("****\n  Tour de " + self.role)
        p = self.select(party.tuiles_actives)
        avec = self.use_power(p, party, avant | deux)
        self.move(p, avec, party.bloque)
        self.use_power(p, party, apres | deux)

    def select(self, t):
        w = self.game.demander("Tuiles disponibles : " + str(t) + " choisir entre 0 et " + str(len(t) - 1), self)
        i = int(w) if w.isnumeric() and int(w) in range(len(t)) else 0
        p = t[i]
        self.game.informer("REPONSE INTERPRETEE : " + str(p))
        self.game.informer(self.role + " joue " + p.color)
        del t[i]
        return p

    def use_power(self, p, party, activables):
        if p.pouvoir and p.color in activables:
            a = self.game.demander("Voulez-vous activer le pouvoir (0/1) ?", self) == "1"
            self.game.informer("REPONSE INTERPRETEE : " + str(a == 1))
            if a:
                self.game.informer("Pouvoir de " + p.color + " activé")
                p.pouvoir = False
                if p.color == "rouge":
                    draw = party.cartes[0]
                    self.game.informer(str(draw) + " a été tiré")
                    if draw == "fantome":
                        party.start += -1 if self.numero == 0 else 1
                    elif self.numero == 0:
                        draw.suspect = False
                    del party.cartes[0]
                if p.color == "noir":
                    for q in party.personnages:
                        if q.position in {x for x in passages[p.position] if
                                          x not in party.bloque or q.position not in party.bloque}:
                            q.position = p.position
                            self.game.informer("NOUVEAU PLACEMENT : " + str(q))
                if p.color == "blanc":
                    for q in party.personnages:
                        if q.position == p.position and p != q:
                            dispo = {x for x in passages[p.position] if
                                     x not in party.bloque or q.position not in party.bloque}
                            w = self.game.demander(str(q) + ", positions disponibles : " + str(dispo) + ", choisir la valeur",
                                         self)
                            x = int(w) if w.isnumeric() and int(w) in dispo else dispo.pop()
                            self.game.informer("REPONSE INTERPRETEE : " + str(x))
                            q.position = x
                            self.game.informer("NOUVEAU PLACEMENT : " + str(q))
                if p.color == "violet":
                    self.game.informer("Rappel des positions :\n" + str(party))
                    co = self.game.demander("Avec quelle couleur échanger (pas violet!) ?", self)
                    if co not in couleurs:
                        co = "rose"
                    self.game.informer("REPONSE INTERPRETEE : " + co)
                    q = [x for x in party.personnages if x.color == co][0]
                    p.position, q.position = q.position, p.position
                    self.game.informer("NOUVEAU PLACEMENT : " + str(p))
                    self.game.informer("NOUVEAU PLACEMENT : " + str(q))
                if p.color == "marron":
                    return [q for q in party.personnages if p.position == q.position]
                if p.color == "gris":
                    w = self.game.demander("Quelle salle obscurcir ? (0-9)", self)
                    party.shadow = int(w) if w.isnumeric() and int(w) in range(10) else 0
                    self.game.informer("REPONSE INTERPRETEE : " + str(party.shadow))
                if p.color == "bleu":
                    w = self.game.demander("Quelle salle bloquer ? (0-9)", self)
                    x = int(w) if w.isnumeric() and int(w) in range(10) else 0
                    w = self.game.demander("Quelle sortie ? Chosir parmi : " + str(passages[x]), self)
                    y = int(w) if w.isnumeric() and int(w) in passages[x] else passages[x].copy().pop()
                    self.game.informer("REPONSE INTERPRETEE : " + str({x, y}))
                    party.bloque = {x, y}
        return [p]

    def move(self, p, avec, bloque):
        pass_act = pass_ext if p.color == 'rose' else passages
        if p.color != 'violet' or p.pouvoir:
            disp = {x for x in pass_act[p.position] if p.position not in bloque or x not in bloque}
            w = self.game.demander("positions disponibles : " + str(disp) + ", choisir la valeur", self)
            x = int(w) if w.isnumeric() and int(w) in disp else disp.pop()
            self.game.informer("REPONSE INTERPRETEE : " + str(x))
            for q in avec:
                q.position = x
                self.game.informer("NOUVEAU PLACEMENT : " + str(q))


# Create a TCP/IP socket
class Game:
    def __init__(self, index):
        self.log = "./log_game_" + str(index) + ".txt"
        f = codecs.open(self.log, "w", "utf-8")
        f.close()
        # self.logfile = codecs.open(self.log, "a", "utf-8")
        self.finished = False
        self.index = index
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_address = ('localhost', 0)
        self.port = ""
        self.detective = None
        self.ghost = None
        self.joueurs = [Player(0, self), Player(1, self)]
        self.start, self.end, self.num_tour, self.shadow, x = 4, 22, 1, randrange(10), randrange(10)
        self.bloque = {x, passages[x].copy().pop()}
        self.personnages = {Character(c) for c in couleurs}
        self.tuiles = [p for p in self.personnages]
        self.cartes = self.tuiles[:]
        self.fantome = self.cartes[randrange(8)]
        self.message("!!! Le fantôme est : " + self.fantome.color)
        self.cartes.remove(self.fantome)
        self.cartes += ['fantome'] * 3

        shuffle(self.tuiles)
        shuffle(self.cartes)
        for i, p in enumerate(self.tuiles):
            p.position = i

    def start_game(self):
        self.socket.bind(self.server_address)
        self.socket.listen(1)
        self.port = self.socket.getsockname()[1]
        self.server_address = ('localhost', self.port)
        # print('starting up on %s port %s' % self.server_address)
        return self.port

    def run(self):
        running = True
        while running:
            if self.detective is None or self.ghost is None:
                # print("waiting connection")
                connection, client_address = self.socket.accept()
                print('connection from', client_address)
                data = connection.recv(128)
                str_data = data.decode("utf-8")[8:]
                if str_data == "1":
                    self.ghost = connection
                elif str_data == "0":
                    self.detective = connection
                else:
                    print(data)
            else:
                self.lancer()
                running = False
        print("CLOSE SERVER")
        self.socket.close()
        # self.logfile.close()

    def message(self, texte):
        logfile = codecs.open(self.log, "a", "utf-8")
        logfile.write(texte + "\n")
        logfile.close()

    def informer(self, texte):
        self.message(texte)

    def demander(self, q, j):
        self.informer("QUESTION : " + q)
        if j.numero == 0:
            self.ghost.sendall(q.encode())
            response = self.ghost.recv(128).decode("utf-8")
        else:
            self.detective.sendall(q.encode())
            response = self.detective.recv(128).decode("utf-8")
        self.informer("REPONSE DONNEE : " + response)
        return response

    def actions(self):
        joueur_actif = self.num_tour % 2
        if joueur_actif == 1:
            shuffle(self.tuiles)
            self.tuiles_actives = self.tuiles[:4]
        else:
            self.tuiles_actives = self.tuiles[4:]
        for i in [joueur_actif, 1 - joueur_actif, 1 - joueur_actif, joueur_actif]:
            self.joueurs[i].play(self)

    def lumiere(self):
        partition = [{p for p in self.personnages if p.position == i} for i in range(10)]
        if len(partition[self.fantome.position]) == 1 or self.fantome.position == self.shadow:
            self.informer("le fantome frappe")
            self.start += 1
            for piece, gens in enumerate(partition):
                if len(gens) > 1 and piece != self.shadow:
                    for p in gens:
                        p.suspect = False
        else:
            self.informer("pas de cri")
            for piece, gens in enumerate(partition):
                if len(gens) == 1 or piece == self.shadow:
                    for p in gens:
                        p.suspect = False
        self.start += len([p for p in self.personnages if p.suspect])

    def tour(self):
        self.informer("**************************\n" + str(self))
        self.actions()
        self.lumiere()
        for p in self.personnages:
            p.pouvoir = True
        self.num_tour += 1

    def lancer(self):
        while self.start < self.end and len([p for p in self.personnages if p.suspect]) > 1:
            self.tour()
        self.informer("L'enquêteur a trouvé - c'était " + str(
            self.fantome) if self.start < self.end else "Le fantôme a gagné")
        self.informer("Score final : " + str(self.end - self.start))

    def __repr__(self):
        return "Tour:" + str(self.num_tour) + ", Score:" + str(self.start) + "/" + str(self.end) + ", Ombre:" + str(
            self.shadow) + ", Bloque:" + str(self.bloque) + "\n" + "  ".join([str(p) for p in self.personnages])

