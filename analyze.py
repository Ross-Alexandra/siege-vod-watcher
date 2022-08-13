import cv2
import datetime
import pytesseract
import sys

from lib.dataManagement.game import Game
from lib.dataRetrival.keyData import getTime
from lib.dataRetrival.killFeed import read_killfeed
from lib.dataRetrival.operatorSelection import getPlayerOperators, findPlayerOperatorSet
from lib.dataRetrival.keyData import isTimestamp
from lib.imageProcessing.frameType import getFrameType
from lib.imageProcessing.constants import IN_MENU, IN_ROUND

def process_menu_data(frame, gameData):
    time = getTime(frame, False)
    if isTimestamp(time) and time == "0:00":
        if gameData.isRoundFinalized():
            if len(gameData.roundData) > 0:
                gameData.finalizeKillFeed()

            print(gameData)

            gameData.newRound()

        # If the time is 0:00 then attempt to read all
        # the operators and player names selected by the team.
        frameData = getPlayerOperators(frame)
        gameData.voteRoundPlayerOperators(frameData)
        print(f"Processed {frameData}")

def process_round_data(frame, gameData):
    if not gameData.isRoundFinalized():
        gameData.finalizeVotes()

        print(gameData)
    
    kill_feed = read_killfeed(frame, gameData)
    for killer, killee in kill_feed:
        feedString = f"{killer} -> {killee}"
        if gameData.killFeed.get(feedString, None) is None:
            gameData.killFeed[feedString] = 1
        else:
            gameData.killFeed[feedString] += 1

    if kill_feed:
        print(f"Killfeed detected: {kill_feed}")
    else:
        print("No killfeed detected on frame.")

if __name__ == "__main__":

    pytesseract.pytesseract.tesseract_cmd = r'C:\Users\Ross Alexandra\AppData\Local\Tesseract-OCR\tesseract.exe'
    start = datetime.datetime.now() # Get start time to display elapsed time.

    file = sys.argv[1] if len(sys.argv) == 2 else r'.\resources\example_round.mp4'

    gameData = Game()
    vidcap = cv2.VideoCapture(file)
    frameCount = 0 
    frameType = IN_MENU # By default, assume a VOD will start on a menu.

    while True:
        success, frame = vidcap.read()

        if not success:
            break
        else:
            frameTypeString = "IN_ROUND" if frameType == IN_ROUND else "IN_MENU"
            print(f"Processing Frame #{frameCount}; FrameType={frameTypeString} elapsed time: {datetime.datetime.now() - start}")

            cv2.imshow('frame', frame)

        # Read in the frame type to later process
        # the round.
        frameType = getFrameType(frame, frameType)

        if frameType != IN_ROUND:
            process_menu_data(frame, gameData)
        else:
            process_round_data(frame, gameData)

        frameCount += 1

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    vidcap.release()
    cv2.destroyAllWindows()

    gameData.newRound()
    gameData.finalizeKillFeed()
    print(f"{gameData}")

