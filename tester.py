import cv2
import pytesseract

from lib.dataRetrival.killFeed import read_killfeed
from lib.dataRetrival.operatorSelection import getPlayerOperators

def killfeed_test():
    im = cv2.imread(r"resources/triple_kill_feed.jpg")
    read_killfeed(im, None)

    cv2.waitKey(0)

    im2 = cv2.imread(r"resources/white_bg.jpg")
    read_killfeed(im2, None)

    cv2.waitKey(0)

    im3 = cv2.imread(r"resources/missed_kill_hs.jpg")
    read_killfeed(im3, None)

    cv2.waitKey(0)

    im4 = cv2.imread(r"resources/final.jpg")
    read_killfeed(im4, None)

    cv2.waitKey(0)

    cv2.destroyAllWindows()

def loadscreen_test():
    im = cv2.imread(r"resources/example_Moment.jpg")
    player_operators = getPlayerOperators(im)

    print(player_operators)

    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    pytesseract.pytesseract.tesseract_cmd = r'C:\Users\Ross Alexandra\AppData\Local\Tesseract-OCR\tesseract.exe'

    killfeed_test()