import cv2
import pytesseract
import numpy as np
import re

from lib.dataRetrival._constants import OPERATORS, PLAYERS
from lib.imageProcessing import remove_gray_image_text_background
from lib.dataManagement.player import Player

def extract_operator_name(image):

    safe_image = np.asarray(image).copy()
    safe_image = cv2.cvtColor(safe_image, COLOR_BGR2HSV)

    name_color_low = np.array([0, 0, 238])
    name_color_high = np.array([5, 5, 255])

    mask = cv2.inRange(safe_image, name_color_low, name_color_high)

    image[mask > 0] = [0, 0, 0]

    operator = pytesseract.image_to_string(image).replace(" ", "").strip()

    # Pytesseract has issues with Siege's I font and often calls it a 1.
    operator = operator.replace("1", "I")

    return operator

def extract_player_name(image):

    safe_image = np.asarray(image).copy()

    #playerCleaned = 255 - teamBGToBlack(player)
    playerEnlarged = cv2.resize(safe_image, (0, 0), fx=4.0, fy=4.0)
    playerImageBlurred = cv2.medianBlur(playerEnlarged, 3)
    playerImageCleaned = cv2.medianBlur(remove_gray_image_text_background(cv2.cvtColor(255 - playerImageBlurred, cv2.COLOR_BGR2GRAY)), 3)

    playerName = pytesseract.image_to_string(playerImageCleaned).replace(" ", "").strip()
    return playerName

def getPlayerOperators(image):

    playerOperators = [{}, {}, {}, {}, {}]
    for i in range(5):
        operatorImage = image[OPERATORS[i]["top"] : OPERATORS[i]["bottom"], OPERATORS[i]["left"]: OPERATORS[i]["right"]]
        operator = extract_operator_name(operatorImage)

        playerImage = image[PLAYERS[i]["top"] : PLAYERS[i]["bottom"], PLAYERS[i]["left"]: PLAYERS[i]["right"]]
        playerName = extract_player_name(playerImage)

        # If the operator or player name has strange characters then
        # we know this is a bad read.
        if not bool(re.match(r'[A-Za-z]+', operator)) or not Player.is_valid_name(playerName):
            operator = "UNKNOWN"
        elif len(operator) < 3 and operator != "IQ":
            operator = "UNKNOWN"

        playerOperators[i][playerName] = operator

    return playerOperators

def findPlayerOperatorSet(playerOperatorVotes):
    '''
        Tally all the dictionaries and return the most common
        key: value pairs (ie, the most likely candidates for
        correct player name and operator).
    '''

    print(f"Tallying Votes: {playerOperatorVotes}")
    votedPlayerOperator = []

    for operatorVotes in playerOperatorVotes:
        tally = {}

        for vote in operatorVotes:
            for playerName, operator in vote.items():

                if operator == "UNKNOWN":
                    continue

                voteString = playerName + "=" + operator
                if tally.get(voteString, None):
                    tally[voteString] += 1
                else:
                    tally[voteString] = 1

        tally = [(key, value) for key, value in tally.items()]
        tally = sorted(tally, key=lambda x: x[1], reverse=True)[0]
        votedPlayerOperator.append(tally)

    return votedPlayerOperator
