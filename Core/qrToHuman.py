# qrToHuman.py
# Gets the distance/device info of the closest QR code and human
# Test Device: Google Pixel 1
#   Focal Length: 26mm
#   Sensor Height: 7.81mm

import cv2
import pyzbar.pyzbar as pyzbar
# import argparse
import imutils
import math
import time

# WARNING: Mac Dependent library for volume control
import osascript

closestQR = {'distance': 0, 'data': '', 'location': (0, 0)}
lineColor = (255, 0, 0)
closestColor = (0, 255, 0)
personColor = (0, 0, 255)

# 5 inches
actualQRHeight = 127

focalLength = 4.67
sensorHeight = 7.81

# 5 ft 10 inches
# avgPersonHeight = 1778
avgPersonHeight = 10

minContourSize = 500


def distance(obj1, obj2):
    absDistance = 0
    for dim in range(0, len(obj1)):
        absDistance += (obj1[dim] - obj2[dim]) ** 2
    return math.sqrt(absDistance)


def parseImage(image):
    objects = pyzbar.decode(image)
    for object in objects:
        print("QR TYPE: ", object.type)
        print("QR DATA: ", object.data)
    return objects


def showBoxes(image, object_data, personData):
    h, w, c = image.shape
    try:
        personZDistance = (focalLength * avgPersonHeight * h) / (abs(personData['y2'] - personData['y1']) * sensorHeight)
    except ZeroDivisionError:
        print("PERSON-QR PAIR NOT DETECTED")
        return
    humanLocation = None
    mmToPixelRatio = None
    volumeLevel = 0
    for object in object_data:
        qrPoints = len(object.location)
        midPoint = (0, 0)
        for i in range(0, qrPoints):
            midPoint = (midPoint[0] + object.location[i][0], midPoint[1]
                      + object.location[i][1])
            cv2.line(image, object.location[i], object.location[(i + 1)
                     % qrPoints], lineColor, 3)
        midPoint = (int(midPoint[0] / qrPoints), int(midPoint[1] / qrPoints))

        sideLength = 0
        for i in range(1, qrPoints):
            sideLength += distance(object.location[i-1], object.location[i])
        sideLength /= qrPoints

        if mmToPixelRatio is None:
            mmToPixelRatio = sideLength**2 / actualQRHeight**2
            personZDistance *= mmToPixelRatio
            humanLocation = (personData['midX'], personData['midY'], personZDistance)
        zDistance = (focalLength * actualQRHeight * h) / (sideLength * sensorHeight)
        zDistance *= mmToPixelRatio
        mid3Point = (midPoint[0], midPoint[1], zDistance)

        cv2.rectangle(image, (personData['x1'], personData['y1']),
                     (personData['x2'], personData['y2']), (0, 255, 0), 2)

        cv2.circle(image, (int(personData['midX']), int(personData['midY'])), 10, personColor, -1)

        absDiff = distance(mid3Point, humanLocation)
        volumeLevel = math.floor(absDiff / max(w, h) * 100)
        print("\nQR LOCATION: ", mid3Point)
        print("HUMAN LOCATION: ", humanLocation)
        print("DISTANCE BETWEEN: ", absDiff, "\n")
        print("VOLUME LEVEL: ", volumeLevel)
        if closestQR['data'] == '' or absDiff < closestQR['distance']:
            closestQR['distance'] = absDiff
            closestQR['data'] = object.data
            closestQR['location'] = midPoint
    osascript.osascript("set volume output volume " + str(volumeLevel))
    cv2.circle(image, closestQR['location'], 10, closestColor, -1)
    cv2.imshow("QR To Human", image)


if __name__ == '__main__':
    camera = cv2.VideoCapture(0)
    time.sleep(0.25)
    photos = []
    # photos.append(cv2.imread("qr_test/closeSwitch1.jpg"))
    # photos.append(cv2.imread("qr_test/closeSwitch2.jpg"))
    # photos.append(cv2.imread("qr_test/closeSwitch3.jpg"))
    # photos.append(cv2.imread("qr_test/closeSwitch4.jpg"))
    # photos.append(cv2.imread("qr_test/closeSwitch5.jpg"))
    # photos.append(cv2.imread("qr_test/mouse3.jpg"))

    exitKey = False
    # while True:
    # if exitKey:
    #     break
    prevFrame = None
    firstFrame = None
    first = True
    closestQR = {'distance': 0, 'data': '', 'location': (0, 0)}
    while True:
    # for i in range(0, len(photos)):
        time.sleep(0.25)
        gotFrame, frame = camera.read()
        # gotFrame, frame = True, photos[i]
        if not gotFrame:
            break

        frame = imutils.resize(frame, width=500)
        person_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        person_gray = cv2.GaussianBlur(person_gray, (21, 21), 0)

        if prevFrame is None:
            firstFrame = frame
            prevFrame = person_gray
            cv2.imshow("QR To Human", frame)
            continue

        frameDiff = cv2.absdiff(prevFrame, person_gray)
        personThreshold = cv2.threshold(frameDiff, 60, 255, cv2.THRESH_BINARY)[1]
        personThreshold = cv2.dilate(personThreshold, None, iterations=2)

        _, personContours, _ = cv2.findContours(personThreshold.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        if len(personContours) == 0:
            continue

        maxWidth, maxHeight = 0, 0
        personX, personY = 0, 0
        avgMidX = 0
        avgMidY = 0
        for contour in personContours:
            if cv2.contourArea(contour) < minContourSize:
                continue
            (person_x, person_y, p_width, p_height) = cv2.boundingRect(contour)
            maxWidth, maxHeight = p_width, p_height
            personX, personY = person_x, person_y
            avgMidX += personX + maxWidth/2
            avgMidY += personY + maxHeight/2
            cv2.rectangle(frame, (personX, personY), (personX + maxWidth, personY + maxHeight), (0, 255, 0), 2)
        avgMidX /= len(personContours)
        avgMidY /= len(personContours)

        personData = {
                        'x1': personX, 'y1': personY,
                        'x2': personX + maxWidth, 'y2': personY + maxHeight,
                        'midX': avgMidX,
                        'midY': avgMidY
                     }

        if first:
            cv2.imshow("QR To Human", firstFrame)
            first = False
        objects = parseImage(frame)
        showBoxes(frame, objects, personData)
        prevFrame = person_gray
        key = cv2.waitKey(1) & 0xFF
        if key == ord('o'):
            exitKey = True
            break
    camera.release()
    cv2.waitKey(0)
    cv2.destroyAllWindows()
