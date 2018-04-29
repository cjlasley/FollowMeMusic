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

closestQR = {'distance': 0, 'data': ''}
lineColor = (255, 0, 0)
closestColor = (0, 255, 0)

# 5 inches
actualQRHeight = 127

focalLength = 4.67
sensorHeight = 7.81


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


def showBoxes(image, object_data):
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
        print("IMG HEIGHT: ", h)
        print("SIDE LENGTH: ", sideLength)
        zDistance = (focalLength * actualQRHeight * h) / (sideLength * sensorHeight)
        print("Z-DISTANCE: ", zDistance)
        # midPoint += zDistance
        # TODO: INTEGRATE MOTION DETECT
        humanLocation = (0, 0, 0)
        absDiff = distance(midPoint, humanLocation)
        if closestQR['data'] == '' or absDiff < closestQR['distance']:
            closestQR['distance'] = absDiff
            closestQR['data'] = object.data
            cv2.circle(image, midPoint, 10, closestColor, -1)
    cv2.imshow("QR: ", image)
    cv2.waitKey(0)


if __name__ == '__main__':
    qr_source = cv2.imread("qr_test/above1.jpg")
    qr_source = imutils.resize(qr_source, width=500)
    # gray = cv2.cvtColor(qr_source, cv2.COLOR_BGR2GRAY)
    objects = parseImage(qr_source)
    showBoxes(qr_source, objects)
