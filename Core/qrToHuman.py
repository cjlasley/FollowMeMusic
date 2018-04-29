import cv2
import pyzbar.pyzbar as pyzbar
# import argparse
import imutils
import math

closestQR = {'distance': 0, 'data': ''}
lineColor = (255, 0, 0)
closestColor = (0, 255, 0)


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
            cv2.line(image, object.location[i], object.location[(i+1)
                     % qrPoints], lineColor, 3)
        midPoint = (int(midPoint[0] / qrPoints), int(midPoint[1] / qrPoints))
        # TODO: INTEGRATE MOTION DETECT
        humanLocation = (0, 0, 0)
        absDiff = math.sqrt(abs((midPoint[0] - humanLocation[0])
                            + (midPoint[1] - humanLocation[1])))
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
