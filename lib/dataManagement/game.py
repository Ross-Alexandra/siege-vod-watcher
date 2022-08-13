from collections import OrderedDict
from difflib import SequenceMatcher

from lib.dataManagement.round import Round
from lib.dataRetrival.operatorSelection import findPlayerOperatorSet

class Game:

    def __init__(self):
        self.roundData = []
        self._operatorPlayerVotes = [[], [], [], [], []]
        self._roundFinalized = True
        self.currentRound = None
        self.knownPlayers = []

        self.killFeed = OrderedDict()

    def newKnownPlayer(self, playerName):
        """
            Utility function to determine if there are already
            10 known players or add a new player.
        """ 

        if len(self.knownPlayers) > 10:
            return False

        self.knownPlayers.append(playerName)
        return True

    def isRoundFinalized(self):
        return self._roundFinalized

    def newRound(self):

        # roundData contains all rounds, thus
        # its size +1 = the number of the next round.
        self.roundData.append(Round(len(self.roundData) + 1))
        self._roundFinalized = False

    def _addPlayerToRound(self, playerName, operatorName):
        self.roundData[-1].addPlayer(playerName, operatorName)

    def voteRoundPlayerOperators(self, votes):
        if not self._roundFinalized:
            for i in range(5):
                self._operatorPlayerVotes[i].append(votes[i])

    def finalizeVotes(self):

        errorState = False

        if len(self._operatorPlayerVotes) != 0:
            playerOperators = [PO[0] for PO in findPlayerOperatorSet(self._operatorPlayerVotes)]
            print(f"Most common player operator pairs: {playerOperators}")

            for playerOperator in playerOperators:
                player, operator = playerOperator.split('=')
                self._addPlayerToRound(player, operator)

                # If these players are unknown, then add them
                # to the list of known players.
                if player not in self.knownPlayers:
                    errorState = self.newKnownPlayer(player)

            self._operatorPlayerVotes = [[], [], [], [], []] 
            self.currentRound = self.roundData[-1]
        else:
            # This round was a data read error. Remove it.
            self.roundData = self.roundData[:-1]
        self._roundFinalized = True

        if errorState:
            print("WARNING: POTENTIAL ERROR; There have been more than 10 players registered with this game.")

    def finalizeKillFeed(self):

        kill_feed = sorted(list(self.killFeed.items()), key=lambda x: x[1], reverse=True)
        kill_feed = [feed_vote[0] for feed_vote in kill_feed if feed_vote[1] > 3]

        roundKills = []
        iteration = 0
        while len(kill_feed) > 0:
            print(f"{iteration}th iteration; killfeed: {kill_feed}")

            most_voted_string = kill_feed[0]
            roundKills.append(most_voted_string)

            # Filter down the killfeed to only include strings with a less that 70% match to
            # the most voted string.
            kill_feed = list(filter(lambda x: False if SequenceMatcher(None, most_voted_string, x).ratio() > .7 else True, kill_feed))

            iteration += 1


        self.roundData[-1].registerKillFeed([feed for feed in self.killFeed.keys() if feed in roundKills])
        self.killFeed = {}

    def __str__(self):
        stringBuilder = ""

        for rnd in self.roundData:
            stringBuilder += f"Round {rnd.roundNumber}:\n"
            for player in rnd.playerOperators:
                stringBuilder += f"{player.playerName} =  {player.playerOperator}\n"

            stringBuilder += f"Round Killfeed: {rnd.killFeed}"
            stringBuilder += "\n"

        return stringBuilder