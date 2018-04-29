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
# import numpy
import time

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


def showBoxes(image, object_data, person_data):
    h, w, c = image.shape
    personZDistance = (focalLength * avgPersonHeight * h) / (abs(personData['y2'] - personData['y1']) * sensorHeight)

    humanLocation = None
    mmToPixelRatio = None

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
            humanLocation = (personData['midX'], personData['midY'], mmToPixelRatio * personZDistance)
        # print(mmToPixelRatio)
        # print("IMG HEIGHT: ", h)
        # print("SIDE LENGTH: ", sideLength)
        zDistance = (focalLength * actualQRHeight * h) / (sideLength * sensorHeight)
        # print("Z-DISTANCE: ", zDistance)
        mid3Point = (midPoint[0], midPoint[1], mmToPixelRatio * zDistance)

        cv2.rectangle(image, (personData['x1'], personData['y1']),
                     (personData['x2'], personData['y2']), (0, 255, 0), 2)

        cv2.circle(image, (int(personData['midX']), int(personData['midY'])), 10, personColor, -1)

        absDiff = distance(mid3Point, humanLocation)
        print("\nQR LOCATION: ", mid3Point)
        print("HUMAN LOCATION: ", humanLocation)
        print("DISTANCE BETWEEN: ", absDiff, "\n")
        if closestQR['data'] == '' or absDiff < closestQR['distance']:
            closestQR['distance'] = absDiff
            closestQR['data'] = object.data
            closestQR['location'] = midPoint

    cv2.circle(image, closestQR['location'], 10, closestColor, -1)
    cv2.imshow("QR To Human", image)
    # cv2.waitKey(0)


if __name__ == '__main__':
    # qr_source = cv2.imread("qr_test/horiz1.jpg")
    # qr_source = imutils.resize(qr_source, width=500)

    # kernel = numpy.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
    # qr_source = cv2.filter2D(qr_source, -1, kernel)

    # qr_source = cv2.cvtColor(qr_source, cv2.COLOR_BGR2HSV)
    # qr_source[:, :, 2] = [[max(pixel - 75, 0) if pixel < 100
    # else min(pixel + 75, 255) for pixel in row] for row in qr_source[:, :, 2]]
    # qr_source = cv2.cvtColor(qr_source, cv2.COLOR_HSV2BGR)
    # qr_source = cv2.cvtColor(qr_source, cv2.COLOR_BGR2GRAY)

    # qr_source = cv2.threshold(qr_source, 150, 255, cv2.THRESH_BINARY)[1]

    # gray = cv2.cvtColor(qr_source, cv2.COLOR_BGR2GRAY)

    # camera = cv2.VideoCapture(0)
    # time.sleep(0.25)
    photos = []
    photos.append(cv2.imread("qr_test/closeSwitch1.jpg"))
    photos.append(cv2.imread("qr_test/closeSwitch2.jpg"))
    photos.append(cv2.imread("qr_test/closeSwitch3.jpg"))
    photos.append(cv2.imread("qr_test/closeSwitch4.jpg"))
    photos.append(cv2.imread("qr_test/closeSwitch5.jpg"))
    # photos.append(cv2.imread("qr_test/mouse3.jpg"))

    prevFrame = None
    firstFrame = None
    first = True
    # while True:
    for i in range(0, len(photos)):
        # gotFrame, frame = camera.read()
        gotFrame, frame = True, photos[i]
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

        maxWidth, maxHeight = 0, 0
        personX, personY = 0, 0
        avgMidX = 0
        avgMidY = 0
        for contour in personContours:
            if cv2.contourArea(contour) < minContourSize:
                continue
            (person_x, person_y, p_width, p_height) = cv2.boundingRect(contour)
            # if p_width * p_height > maxWidth * maxHeight:
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
            cv2.waitKey(0)
            first = False
        # cv2.imshow("QR To Human", frame)
        objects = parseImage(frame)
        showBoxes(frame, objects, personData)
        prevFrame = person_gray
        cv2.waitKey(0)
    # camera.release()
    cv2.destroyAllWindows()
