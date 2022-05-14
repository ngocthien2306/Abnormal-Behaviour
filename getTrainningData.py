# -*- coding: utf-8 -*-
"""
Created on Sat May 14 08:32:29 2022

@author: ngomi
"""
import cv2
import pandas as pd
import time

cap = cv2.VideoCapture(0)
face_cascade = cv2.CascadeClassifier('cascades/data/haarcascade_frontalface_alt2.xml')

label = "F" # T: binh thuong, F: bat thuong

columns = ["label"]
for i in range(0, 150):
    # X
    columns.append("X"+str(i))
    # Y
    columns.append("Y"+str(i))
    # Width
    columns.append("W"+str(i))
    # Lenght
    columns.append("L"+str(i))
    pass
df = pd.DataFrame(data=[], columns=columns)    

row_data = [label]

frame_rate = 5
prev = 0
frame_count = 0
while(frame_count < 150):
    time_elapsed = time.time() - prev
    ret, frame = cap.read()

    if time_elapsed > 1./frame_rate:
        prev = time.time()
   
        # Capture frame-by-frame
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors = 5)
        for (x,y,w,h) in faces:
            
            row_data.append(x)
            row_data.append(y)
            row_data.append(w)
            row_data.append(h)
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
df_length = len(df)
df.loc[df_length] = row_data
df.to_csv('trainning_data.csv')
