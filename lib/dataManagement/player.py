import re

class Player:

    def __init__(self, playerName, playerOperator):
        self.playerName = playerName
        self.playerOperator = playerOperator
        self.kills = 0
        self.deaths = 0

    @staticmethod
    def is_valid_name(name):
        name_length = len(name)

        if not 3 <= name_length <= 15:
            return False

        
        if not bool(re.match(r'[A-Za-z\.-_]+', name)):
            return False

        return True