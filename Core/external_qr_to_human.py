# qrToHuman.py
# Gets the distance/device info of the closest QR code and human
# Test Device: Google Pixel 1
#   Focal Length: 26mm
#   Sensor Height: 7.81mm

import cv2
import pyzbar.pyzbar as pyzbar
import imutils
import math


class SpatialQR:
    def __init__(self, image):
        self.previousImage = cv2.imread(image)
        self.currentImage = cv2.imread(image)
        self.closestQR = {'distance': 0, 'data': '', 'location': (0, 0)}
        self.lineColor = (255, 0, 0)
        self.closestColor = (0, 255, 0)
        self.personColor = (0, 0, 255)

        # 5 inches
        self.actualQRHeight = 203
        self.focalLength = 4.67
        self.sensorHeight = 7.81

        # 5 ft 10 inches
        # avgPersonHeight = 1778
        self.avgPersonHeight = 1500
        self.minContourSize = 500
        self.prevFrame = None

    def distance(self, obj1, obj2):
        absDistance = 0
        for dim in range(0, len(obj1)):
            absDistance += (obj1[dim] - obj2[dim]) ** 2
        return math.sqrt(absDistance)

    def parseImage(self, image):
        objects = pyzbar.decode(image)
        # for object in objects:
            # print("QR TYPE: ", object.type)
            # print("QR DATA: ", object.data)
        return objects

    def showBoxes(self, image, object_data, personData):
        h, w, c = image.shape
        try:
            personZDistance = (self.focalLength * self.avgPersonHeight * h) / (abs(personData['y2'] - personData['y1']) * self.sensorHeight)
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
                         % qrPoints], self.lineColor, 3)
            midPoint = (int(midPoint[0] / qrPoints), int(midPoint[1] / qrPoints))

            sideLength = 0
            for i in range(1, qrPoints):
                sideLength += self.distance(object.location[i-1], object.location[i])
            sideLength /= qrPoints

            if mmToPixelRatio is None:
                mmToPixelRatio = sideLength**2 / self.actualQRHeight**2
                personZDistance *= mmToPixelRatio
                humanLocation = (personData['midX'], personData['midY'], personZDistance)
            zDistance = (self.focalLength * self.actualQRHeight * h) / (sideLength * self.sensorHeight)
            zDistance *= mmToPixelRatio
            mid3Point = (midPoint[0], midPoint[1], zDistance)

            cv2.rectangle(image, (personData['x1'], personData['y1']),
                         (personData['x2'], personData['y2']), (0, 255, 0), 2)

            cv2.circle(image, (int(personData['midX']), int(personData['midY'])), 10, self.personColor, -1)

            absDiff = self.distance(mid3Point, humanLocation)
            volumeLevel += math.floor(absDiff / max(w, h) * 100)
            # print("\nQR LOCATION: ", mid3Point)
            # print("HUMAN LOCATION: ", humanLocation)
            # print("DISTANCE BETWEEN: ", absDiff, "\n")
            # print("VOLUME LEVEL: ", volumeLevel)
            if self.closestQR['data'] == '' or absDiff < self.closestQR['distance']:
                self.closestQR['distance'] = absDiff
                self.closestQR['data'] = object.data
                self.closestQR['location'] = midPoint
        # osascript.osascript("set volume output volume " + str(volumeLevel))
        cv2.circle(image, self.closestQR['location'], 10, self.closestColor, -1)
        cv2.imshow("QR To Human", image)
        volumeLevel /= len(object_data)
        return volumeLevel

    def getDistanceToVolume(self, image):
        frame = cv2.imread(image)
        self.closestQR = {'distance': 0, 'data': '', 'location': (0, 0)}

        frame = imutils.resize(frame, width=500)
        person_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        person_gray = cv2.GaussianBlur(person_gray, (21, 21), 0)

        if self.prevFrame is None:
            self.prevFrame = person_gray
            cv2.imshow("QR To Human", frame)
            return -1

        frameDiff = cv2.absdiff(self.prevFrame, person_gray)
        personThreshold = cv2.threshold(frameDiff, 30, 255, cv2.THRESH_BINARY)[1]
        personThreshold = cv2.dilate(personThreshold, None, iterations=2)

        _, personContours, _ = cv2.findContours(personThreshold.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        if len(personContours) == 0:
            self.prevFrame = person_gray
            return -1

        maxWidth, maxHeight = 0, 0
        personX, personY = 0, 0
        avgMidX = 0
        avgMidY = 0
        for contour in personContours:
            if cv2.contourArea(contour) < self.minContourSize:
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

        objects = self.parseImage(frame)
        volume = self.showBoxes(frame, objects, personData)
        self.prevFrame = person_gray
        key = cv2.waitKey(1) & 0xFF
        if key == ord('o'):
            exit()
        return volume


# if __name__ == '__main__':
#     sqr = SpatialQR("qr_test/closeSwitch1.jpg")
#     print(sqr.getDistanceToVolume("qr_test/closeSwitch2.jpg"))
#     print(sqr.getDistanceToVolume("qr_test/closeSwitch3.jpg"))
