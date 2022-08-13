import cv2
import pytesseract
import re

from lib.dataRetrival._constants import ROUND_TIME, MENU_TIME

def getTime(image, is_round):
    if is_round: 
        timeCrop = image[ROUND_TIME['top'] : ROUND_TIME['bottom'], ROUND_TIME['left'] : ROUND_TIME['right']]
    else:
        timeCrop = image[MENU_TIME['top'] : MENU_TIME['bottom'], MENU_TIME['left'] : MENU_TIME['right']]
    greyScale = cv2.cvtColor(timeCrop, cv2.COLOR_BGR2GRAY)
    timestamp = pytesseract.image_to_string(greyScale, lang='eng').strip()
    print(f"Parsed timestamp: {timestamp}")

    return timestamp

def isTimestamp(timeStampString):

    # Regex checks whether the string matches
    # the following format:
    #    <number> <colon> <number> <number>
    # This will match to all realistic timers in game.
    # should a timer have 4 digits then it is not supported.
    return bool(re.match(r"^\d:\d\d$", timeStampString))


def getScoreData(image):
    pass