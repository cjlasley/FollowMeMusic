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

closestQR = {'distance': 0, 'data': ''}
lineColor = (255, 0, 0)
closestColor = (0, 255, 0)

# 5 inches
actualQRHeight = 127

focalLength = 4.67
sensorHeight = 7.81

# 5 ft 10 inches
avgPersonHeight = 1778

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


def showBoxes(image, object_data, person_contours):
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

        h, w, c = image.shape

        mmToPixelRatio = sideLength**2 / actualQRHeight**2
        print(mmToPixelRatio)
        # print("IMG HEIGHT: ", h)
        # print("SIDE LENGTH: ", sideLength)
        zDistance = (focalLength * actualQRHeight * h) / (sideLength * sensorHeight)
        # print("Z-DISTANCE: ", zDistance)
        # TODO: INTEGRATE MOTION DETECT
        mid3Point = (midPoint[0], midPoint[1], mmToPixelRatio * zDistance)

        maxPersonHeight = 0
        avgPersonX = 0
        avgPersonY = 0
        for contour in personContours:
            if cv2.contourArea(contour) < minContourSize:
                continue
            (person_x, person_y, p_width, p_height) = cv2.boundingRect(contour)
            avgPersonX += person_x
            avgPersonY += person_y
            if p_height > maxPersonHeight:
                maxPersonHeight = p_height
            cv2.rectangle(image, (person_x, person_y), (person_x + p_width, person_y + p_height), (0, 255, 0), 2)
        avgPersonX /= len(personContours)
        avgPersonY /= len(personContours)
        personZDistance = (focalLength * avgPersonHeight * h) / (maxPersonHeight * sensorHeight)
        humanLocation = (avgPersonX, avgPersonY, mmToPixelRatio * personZDistance)
        absDiff = distance(mid3Point, humanLocation)
        print("DIST: ", absDiff)
        if closestQR['data'] == '' or absDiff < closestQR['distance']:
            closestQR['distance'] = absDiff
            closestQR['data'] = object.data
            cv2.circle(image, midPoint, 10, closestColor, -1)
    cv2.imshow("QR: ", image)
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
    photos.append(cv2.imread("qr_test/mouse1.jpg"))
    photos.append(cv2.imread("qr_test/mouse2.jpg"))
    photos.append(cv2.imread("qr_test/mouse3.jpg"))

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
            cv2.imshow("MOTION DETECT", frame)
            continue

        frameDiff = cv2.absdiff(prevFrame, person_gray)
        personThreshold = cv2.threshold(frameDiff, 60, 255, cv2.THRESH_BINARY)[1]
        personThreshold = cv2.dilate(personThreshold, None, iterations=2)

        _, personContours, _ = cv2.findContours(personThreshold.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        maxPersonHeight = 0
        avgPersonX = 0
        avgPersonY = 0
        maxWidth, maxHeight = 0, 0
        maxX, maxY = 0, 0
        for contour in personContours:
            if cv2.contourArea(contour) < minContourSize:
                continue
            (person_x, person_y, p_width, p_height) = cv2.boundingRect(contour)
            avgPersonX += person_x
            avgPersonY += person_y
            if p_height > maxPersonHeight:
                maxPersonHeight = p_height
            if p_width * p_height > maxWidth * maxHeight:
                maxWidth, maxHeight = p_width, p_height
                maxX, maxY = person_x, person_y

        cv2.rectangle(frame, (maxX, maxY), (maxX + maxWidth, maxY + maxHeight), (0, 255, 0), 2)

        if first:
            cv2.imshow("MOTION DETECT", firstFrame)
            cv2.waitKey(0)
            first = False
        cv2.imshow("MOTION DETECT", frame)
        objects = parseImage(frame)
        # showBoxes(frame, objects, personContours)
        cv2.waitKey(0)
    # camera.release()
    cv2.destroyAllWindows()
