# -*- coding: utf-8 -*-
"""
Created on Fri May  6 21:03:29 2022

@author: ngomi
"""

import cv2

class detector:

    def beginDetec(seft):
        cap = cv2.VideoCapture(0)
        face_cascade = cv2.CascadeClassifier('cascades/data/haarcascade_frontalface_alt2.xml')

        while(True):
            # Capture frame-by-frame
            ret, frame = cap.read()
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors = 5)
            for (x,y,w,h) in faces:
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
    
        