import cv2
import pyzbar.pyzbar as pyzbar
# import argparse
import imutils


def parseImage(image):
    objects = pyzbar.decode(image)
    for object in objects:
        print("QR TYPE: ", object.type)
        print("QR DATA: ", object.data)
    return objects


def showQRBox(image, object_data):
    lineColor = (255, 0, 0)
    for object in object_data:
        qrPoints = len(object.location)
        midPoint = (0, 0)
        for i in range(0, qrPoints):
            print(object.location[i])
            midPoint += (midPoint[0] + object.location[i][0], midPoint[1] + object.location[i][1])
            print("MID: ", midPoint)
            # midPoint[1] += object.location[i][1]
            cv2.line(image, object.location[i], object.location[(i+1)
                     % qrPoints], lineColor, 3)
        midPoint = (int(midPoint[0] / qrPoints), int(midPoint[1] / qrPoints))
        # midPoint[1] /= qrPoints
        # print(midPoint)
        cv2.circle(image, midPoint, 3, lineColor)
    cv2.imshow("QR: ", image)
    cv2.waitKey(0)


if __name__ == '__main__':
    qr_source = cv2.imread("qr_test/above1.jpg")
    qr_source = imutils.resize(qr_source, width=500)
    gray = cv2.cvtColor(qr_source, cv2.COLOR_BGR2GRAY)
    objects = parseImage(gray)
    showQRBox(gray, objects)
