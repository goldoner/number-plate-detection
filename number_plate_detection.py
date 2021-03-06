import PIL
import cv2
import imutils
import numpy as np
import pytesseract
from os import listdir
from os.path import isfile, join
import re



# print(glob.glob("/Users/dan0bar/Desktop/number-plate-detection/frames/*"))

# 2160 worked, 1030 partially worked,
path_to_picture = 'frames/Frame2160.jpg'

onlyfiles = [f for f in listdir('./frames') if isfile(join('./frames', f))]

onlyfiles.sort()
# print(type(onlyfiles))
# print(onlyfiles)


def detect_plate_on_frame(path_to_picture):

    img = cv2.imread(path_to_picture, cv2.IMREAD_COLOR)
    image = PIL.Image.open(path_to_picture)
    width, height = image.size
    # print(height)
    # print(width)


    img = cv2.resize(img, (width, height))

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.bilateralFilter(gray, 13, 15, 15)

    edged = cv2.Canny(gray, 30, 200)
    contours = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = imutils.grab_contours(contours)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]
    screenCnt = None

    for c in contours:

        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.018 * peri, True)

        if len(approx) == 4:
            screenCnt = approx
            break

    if screenCnt is None:
        detected = 0
        # print("No contour detected")
    else:
        detected = 1

    if detected == 1:
        cv2.drawContours(img, [screenCnt], -1, (0, 0, 255), 3)

    mask = np.zeros(gray.shape, np.uint8)
    new_image = cv2.drawContours(mask, [screenCnt], 0, 255, -1, )
    new_image = cv2.bitwise_and(img, img, mask=mask)

    (x, y) = np.where(mask == 255)
    (topx, topy) = (np.min(x), np.min(y))
    (bottomx, bottomy) = (np.max(x), np.max(y))
    Cropped = gray[topx:bottomx + 1, topy:bottomy + 1]

    text = pytesseract.image_to_string(Cropped, config='--psm 11')
    return text
    # print("Detected license plate Number is:", text)
    # img = cv2.resize(img, (500, 300))
    # Cropped = cv2.resize(Cropped, (400, 200))
    # cv2.imshow('car', img)
    # cv2.imshow('Cropped', Cropped)

    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

# print(detect_plate_on_frame(path_to_picture))

def num_there(s):
    return any(i.isdigit() for i in s)

def upperCase(s):
    return any(i.isupper() for i in s)


for i in onlyfiles:
    try:
        result = detect_plate_on_frame(f'frames/{i}')
        result = "".join(result.split())
        if (len(result) > 7 and len(result) <11 and num_there(result) and upperCase(result)):
            print(i)
            print(result)
    except:
        pass
