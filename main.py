#!/usr/bin/python

import sys

import serial
from cv2 import cv2

# Initialize connection to arduino
ser = serial.Serial("/dev/ttyACM0", baudrate=9600)

# Initialize face cascade
cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

# Get Camera capture
cap = cv2.VideoCapture(0)
cap_center = (cap.get(cv2.CAP_PROP_FRAME_WIDTH) / 2, cap.get(cv2.CAP_PROP_FRAME_HEIGHT) / 2)

while True:
    # Get Video
    _, img = cap.read()

    # Gray scale video for better detection
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Get all detected faces
    faces = cascade.detectMultiScale(gray, 1.1, 4)

    # Tell arduino where to move
    for x, y, w, h in faces:
        face_center = (x + w / 2, y + h / 2)
        mov = (face_center[0] - cap_center[0], face_center[1] - cap_center[1])

        if mov[0] > 0:
            ser.write(abs(mov[0]))
            ser.write("l".encode())
        else:
            ser.write(abs(mov[0]))
            ser.write("r".encode())
        if mov[1] > 0:
            ser.write(abs(mov[1]))
            ser.write("u".encode())
        else:
            ser.write(abs(mov[1]))
            ser.write("d".encode())

    # if escape is pressed release camera and exit
    if cv2.waitKey(30) == 27:
        cap.release()
        sys.exit()
