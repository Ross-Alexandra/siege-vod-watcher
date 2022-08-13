from lib.dataManagement.player import Player

class Round:

    def __init__(self, roundNumber):
        self.roundNumber = roundNumber
        self.playerOperators = []
        self.killFeed = None

    def addPlayer(self, playerName, operatorName):
        if len(self.playerOperators) >= 5:
            raise Exception(f"Attempt to add {len(self.playerOperators) + 1}th player to the round. Cannot add more than 5 players.")

        self.playerOperators.append(Player(playerName, operatorName))

    def registerKillFeed(self, killFeed):
        self.killFeed = killFeed