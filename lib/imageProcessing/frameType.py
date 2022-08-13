from lib.imageProcessing._constants import HEALTH
from lib.imageProcessing.constants import IN_ROUND, IN_MENU
from lib.dataRetrival._constants import ROUND_TIME, MENU_TIME
from lib.dataRetrival.keyData import isTimestamp

import cv2
import pytesseract
from PIL import Image
import numpy as np

def getFrameType(image, previousFrameType):

    # Attempt to read in both the round and menu times.
    roundTime = image[ROUND_TIME['top'] : ROUND_TIME['bottom'], ROUND_TIME['left'] : ROUND_TIME['right']]
    roundTime = pytesseract.image_to_string(roundTime, lang='eng').strip()

    menuTime = image[MENU_TIME['top'] : MENU_TIME['bottom'], MENU_TIME['left'] : MENU_TIME['right']]
    menuTime = pytesseract.image_to_string(menuTime, lang='eng').strip()

    # If both of them have nonsense data, then we're
    # in neither a round nor a menu. Check empty
    # strings for a transition, otherwise
    # assume a bad read.
    if roundTime == "" and menuTime == "":
        return previousFrameType
    elif len(roundTime) != 4 and len(menuTime) != 4:
        return previousFrameType

    inRound = isTimestamp(roundTime)
    inMenu = isTimestamp(menuTime)

    # If neither flag or both flags are set
    # then we cannot read what type of frame
    # this is.
    if not inRound and not inMenu:
        return previousFrameType
    elif inRound and inMenu:
        return previousFrameType

    return IN_ROUND if inRound else IN_MENU
