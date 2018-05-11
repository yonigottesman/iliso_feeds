#!/usr/bin/python

import picamera
import picamera.array
import time
import cv2
from picamera import PiCamera
from picamera.array import PiRGBArray
import imutils
import numpy as np
from math import log
import requests

ILISO_HOST = "http://10.164.149.141:12345/update"

camera = cv2.VideoCapture(0)

frame_0 = None
t0 = time.time()
count = 0

while True:

    #take picture
    (grabbed, frame_1) = camera.read()
    
    # resize the frame, convert it to grayscale, and blur it
    frame_1 = imutils.resize(frame_1, width=500)
    gray = cv2.cvtColor(frame_1, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)

    if frame_0 is None:
        frame_0 = gray
        continue
    
    frameDelta = cv2.absdiff(frame_0, gray)
    thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]
    changed_pixels = np.count_nonzero(thresh)
    count = count + changed_pixels
    t1 = time.time()
    if (t1 - t0) % 60 >= 58:
        if count != 0:
            count = log(count,1.2)
        payload = {"all_feeds":[{"feed_name":"motion","samples":[{"value":count,"time":t1}]}]}
        r = requests.post(ILISO_HOST, json=payload)
        count = 0
        t0 = time.time()
        
    frame_0 = gray
