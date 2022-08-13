import cv2
import pytesseract
import numpy as np

from lib.dataRetrival._constants import KILLFEED
from lib.imageProcessing import find_edges, icon_bg_to_black, remove_gray_image_text_background, teamBGToBlack
from lib.dataManagement.player import Player

def cropToKillfeed(image, current_line):

    safeImage = np.asarray(image).copy()
    blurred = cv2.medianBlur(safeImage, 101)
    premask = teamBGToBlack(blurred)

    if current_line == 0:
        cv2.imshow("crop PreMask", premask)
    mask = cv2.Canny(premask, 0, 255)
    if current_line == 0:
        cv2.imshow("Crop Mask", mask)

    x1, _, _ = find_edges(mask)
    return image[:, x1:]

def read_killfeed(image, gameData):

    kill_death = []
    current_line = 4 # decremeted at start of loop.

    while True:

        # Only 4 lines of killfeed are possible, after 4 lines, stop trying to process.
        if current_line < 0:
            print("Done reading 4th line.")
            break
        else:
            current_line -= 1

        killfeed = image[KILLFEED[current_line]["top"] : KILLFEED[current_line]["bottom"], KILLFEED[current_line]["left"]: KILLFEED[current_line]["right"]]
        killfeed = cv2.resize(killfeed, (0, 0), fx=4.0, fy=4.0) 
        killfeed = cropToKillfeed(killfeed, current_line)

        if current_line == 0:
            cv2.imshow("feed", killfeed)

        # Create a strip of each color to isolate where the
        # words will be located. This allows us to crop
        # to an edge and guarentee that no portion of the
        # gun will show up.
        # Do this by washing the image out until the
        # gun icon disappears, bluring the text away into
        # color strips, then pulling out the location of the
        # start and end of each strip.

        try:
            # -215 Assertion Error is known to be thrown here.
            # Ignore this frame, as we will get plenty more.
            premask = cv2.medianBlur(killfeed, 65)
        except:
            print("Error blurring killfeed strip image. Checking next line.")
            continue

        premask = icon_bg_to_black(premask)
        mask = cv2.Canny(premask, 0, 255)

        if current_line == 0:
            cv2.imshow("premask", premask)
            cv2.imshow("Mask", mask)
        
        kill_right, death_left, no_edges = find_edges(mask)

        # If no edges are detected, then this is not actually
        # a killfeed.
        if no_edges:
            print("No gun icon detected, assuming no killfeed.")
            continue

        killImage = killfeed[:, :kill_right]
        deathImage = killfeed[:, death_left:]

        try:
            # -215 Assertion Error is known to be thrown here.
            # Ignore this frame, as we will get plenty more.
            killImageBlurred = cv2.medianBlur(killImage, 3)
        except:
            print("Error blurring kill image. Checking next line.")
            continue

        killImageCleaned = cv2.medianBlur(remove_gray_image_text_background(cv2.cvtColor(255 - killImageBlurred, cv2.COLOR_BGR2GRAY)), 3)
        killString = pytesseract.image_to_string(killImageCleaned).replace(" ", "").strip()

        if current_line == 0:
            cv2.imshow("Kill", killImageCleaned)

        if not Player.is_valid_name(killString):
            print(f"Read: invalid player name for kill: {killString}")
            continue

        try:
            # -215 Assertion Error is known to be thrown here.
            # Ignore this frame, as we will get plenty more.
            deathImageBlurred = cv2.medianBlur(deathImage, 3)
        except:
            print("Error blurring death image. Checking next line.")
            continue
        
        deathImageCleaned = cv2.medianBlur(remove_gray_image_text_background(cv2.cvtColor(255 - deathImageBlurred, cv2.COLOR_BGR2GRAY)), 3)
        deathString = pytesseract.image_to_string(deathImageCleaned).replace(" ", "").strip()

        if current_line == 0:
            cv2.imshow("Death", deathImageCleaned)

        if not Player.is_valid_name(deathString):
            print(f"Read: invalid player name for death: {deathString}")
            continue

        kill_death.append((killString, deathString))
        print(f"Read: {killString} killed {deathString}")

    return kill_death