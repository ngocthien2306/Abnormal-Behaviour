# -*- coding: utf-8 -*-
"""
Created on Wed May 18 19:02:22 2022

@author: ngomi
"""

import cv2
import pandas as pd
import time
from csv import writer
import mediapipe as mp
import requests

cap = cv2.VideoCapture(0)

faceDetection = mp.solutions.face_detection.FaceDetection()

data = []
studentId = '19110115'
def sendData():
    requests.post('http://127.0.0.1:5000/student/' + studentId, json={'data': data})
    print("sended")

frame_rate = 5
prev = 0
frame_count = 0

while(frame_count < 150):
    time_elapsed = time.time() - prev
    ret, frame = cap.read()

    if time_elapsed > 1./frame_rate:
        prev = time.time()
   
        # Capture frame-by-frame
        color = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = faceDetection.process(color)
        
        x =0 
        y = 0 
        w = 0
        h = 0
        if results.detections:
            for id, detection in enumerate(results.detections):
                bboxC = detection.location_data.relative_bounding_box
                ih, iw, ic = color.shape
                x = int(bboxC.xmin * iw)
                y = int(bboxC.ymin * ih)
                w = int(bboxC.width * iw)
                h = int(bboxC.height * ih)
                break
        
        data.append(x)
        data.append(y)
        data.append(w)
        data.append(h)
        """
        row_data.append(bboxC.xmin)
        row_data.append(bboxC.ymin)
        row_data.append(bboxC.width)
        row_data.append(bboxC.height)
        """

        frame_count += 1
            
        color = (255,0,0)
        stroke = 2
        end_cord_x = x + w
        end_cord_y = y + h
        cv2.rectangle(frame, (x,y), (end_cord_x, end_cord_y), color, stroke)
        # Display the resulting frame
        cv2.imshow('frame',frame)
        
            
    if cv2.waitKey(20) & 0xFF == ord('q'):
        break
# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
sendData()

