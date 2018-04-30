#detect_person.py

import cv2
import numpy as np

body_cascade = cv2.CascadeClassifier('haarcascade_fullbody.xml')

cap = cv2.VideoCapture(0)

def detectBody(img):
    while 1:
        #ret, img = cap.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        body = body_cascade.detectMultiScale(gray, 1.1, 3)

        for (x,y,w,h) in body:
            cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
            roi_gray = gray[y:y+h, x:x+w]
            roi_color = img[y:y+h, x:x+w]
            rectangleCoordinates = (x, y, w, h)
            return rectangleCoordinates

        cv2.imshow('img',img)
        k = cv2.waitKey(30) & 0xff
        if k == 27:
            break

    cap.release()
    cv2.destroyAllWindows()
