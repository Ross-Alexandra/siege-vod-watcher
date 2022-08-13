import cv2
import numpy as np

def teamBGToBlack(image):
    safeImage = np.asarray(image).copy()
    hsv=cv2.cvtColor(safeImage, cv2.COLOR_BGR2HSV)

    orange_low = np.array([6, 120, 155])
    orange_high = np.array([16, 255, 245])
    blue_low = np.array([100, 112, 150])
    blue_high = np.array([105, 222, 230])
    
    mask = cv2.inRange(hsv, orange_low, orange_high)
    safeImage[mask > 0] = (0,0,0)

    mask = cv2.inRange(hsv, blue_low, blue_high)
    safeImage[mask > 0] = (0,0,0)

    return safeImage

def lightToWhite(image, invert=False):
    blockNumber = 0
    for block in image:
        pixelNumber = 0
        for b, g, r in block:
            if invert:
                b = 255 - b
                g = 255 - g
                r = 255 - r
            if r > 50 and g > 50 and b > 50:
                image[blockNumber][pixelNumber] = [255, 255, 255]
            else:
                image[blockNumber][pixelNumber] = [b, g, r]
            pixelNumber += 1
        blockNumber += 1

    return image

def darkToBlack(image, invert=False):
    blockNumber = 0
    for block in image:
        pixelNumber = 0
        for b, g, r in block:
            if invert:
                b = 255 - b
                g = 255 - g
                r = 255 - r
            if r < 50 and g < 50 and b < 50:
                image[blockNumber][pixelNumber] = [0, 0, 0]
            else:
                image[blockNumber][pixelNumber] = [b, g, r]
            pixelNumber += 1
        blockNumber += 1

    return image

def find_edges(mask):
    try:
        mask = np.asarray(mask)

        pts = np.argwhere(mask>0)
        _,x1 = pts.min(axis=0)
        _,x2 = pts.max(axis=0)

        # All that's left in the image is
        # 2 lines, return the x-pos of those,
        # and the kill portion is everything left of
        # x1, and the death portion is everything right
        # of x2.
        return x1, x2, False
    except:
        return 0, 0, True

def icon_bg_to_black(image):
    image = np.asarray(image)
    safeImage = image.copy()

    hsv=cv2.cvtColor(safeImage, cv2.COLOR_BGR2HSV)

    bg_bright_low = np.array([4, 40, 40])
    bg_bright_high = np.array([17, 138, 107])

    bg_dark_low = np.array([100, 11, 62])
    bg_dark_high = np.array([140, 125, 125])

    bright_mask = cv2.inRange(hsv, bg_bright_low, bg_bright_high)
    dark_mask = cv2.inRange(hsv, bg_dark_low, bg_dark_high)

    safeImage[bright_mask > 0] = (255,255,255)
    safeImage[dark_mask > 0] = (255, 255, 255)

    return safeImage

def remove_gray_image_text_background(image, min_activation=0, thresh=87):
    image = np.asarray(image)
    safeImage = image.copy()

    text_low = np.array([min_activation])
    text_high = np.array([thresh])

    mask = cv2.inRange(safeImage, text_low, text_high)

    # Anything not recognized as text, convet to 
    # white pixel
    safeImage[mask == 0] = (255,)
    return safeImage