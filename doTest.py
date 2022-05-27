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
import os
import sys
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

#%%


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle("Exam")
        self.setGeometry(100, 100, 500, 650)
        self.init = ()
        self.fullName = ""
        self.mssv = ""
        self.input_mssv = QTextEdit("", self)
        self.input_fname = QTextEdit("", self)
        self.input_phone = QTextEdit("", self)
        self.select_model = QComboBox(self)
        
    def start_program(self):
        self.hide()
        self.draw_ui_exam()
        self.show()
    
    def reset(self):
        print("A")
    
    def beginTest(self):
        cap = cv2.VideoCapture(0)
        faceDetection = mp.solutions.face_detection.FaceDetection()
        data = []
        
        studentId = self.input_mssv.toPlainText()
        fullname = self.input_fname.toPlainText();
        phone = self.input_phone.toPlainText();
        model = self.select_model.currentText();
        
        if studentId == None or studentId == '':
            return
        if fullname == None or fullname == '':
            return
        if phone == None or phone == '':
            return
        
        print(studentId)
        #append(self.input_fname.toPlainText()
        def sendData():
            requests.post('http://127.0.0.1:5000/student/' + studentId, json={'data': data, 
                                                                              'fullname': fullname, 
                                                                              'phone': phone,
                                                                              'model': model})
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
                
                x = 0 
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
        
                    
                color = (255,0,0)
                stroke = 2
                end_cord_x = x + w
                end_cord_y = y + h
                cv2.rectangle(frame, (x,y), (end_cord_x, end_cord_y), color, stroke)
                # Display the resulting frame
                cv2.imshow('frame',frame)
                frame_count += 1
                
            if frame_count == 150:
                sendData()
                frame_count = 0
                data = []
            if cv2.waitKey(20) & 0xFF == ord('q'):
                break
        # When everything done, release the capture
        cap.release()
        cv2.destroyAllWindows()
    
    
    def draw_ui_exam(self):
        label_title = QLabel("Wellcome Student to the test of HCMUTE", self)
        label_title.setGeometry(20, 20, 400, 50)
        label_title.setFont(QFont('Roboto', 12))

        label_fname = QLabel("Fullname: ", self)
        label_fname.setGeometry(20, 90, 100, 30)
        label_fname.setFont(QFont('Roboto', 12))
        
        label_mssv = QLabel("Student ID: ", self)
        label_mssv.setGeometry(20, 130, 100, 30)
        label_mssv.setFont(QFont('Roboto', 12))
           
        label_phone = QLabel("Phone: ", self)
        label_phone.setGeometry(20, 170, 100, 30)
        label_phone.setFont(QFont('Roboto', 12))
                     
        label_model = QLabel("Model: ", self)
        label_model.setGeometry(20, 210, 100, 30)
        label_model.setFont(QFont('Roboto', 12))
           
        
        
        self.input_fname.setGeometry(130, 90, 350, 30)
        self.input_fname.setFont(QFont('Roboto', 10))
        
        self.input_mssv.setGeometry(130, 130, 350, 30)
        self.input_mssv.setFont(QFont('Roboto', 10))
        
        self.input_phone.setGeometry(130, 170, 350, 30)
        self.input_phone.setFont(QFont('Roboto', 12))
        
        self.select_model.addItem("Suport Vector Machine")
        self.select_model.addItem("Logistic Regression")
        self.select_model.addItem("KNeighbors Classifier")
        self.select_model.addItem("Random Model")
        self.select_model.setGeometry(130, 210, 350, 30)
        
        btn_start = QPushButton("Do exam", self)
        btn_start.setGeometry(20, 300, 150, 50)
        btn_start.clicked.connect(self.beginTest)
        
        label = QLabel(self)
        pixmap = QPixmap('image/machine_learning.jpg')
        label.setPixmap(pixmap)
        label.setScaledContents(True)
        label.setGeometry(20, 370, 460, 250)
                
        
        
        

#%%

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.start_program()
    sys.exit(app.exec())

# In[1] UI
import tkinter as tk

# def handleBegin():
#     studentId = E1.get()
#     if(studentId == ""):
#         return
#     beginTest(studentId)

# window = tk.Tk()

# # Student ID label:
# frame = tk.Frame(
#     master=window,
#     relief=tk.RAISED,
#     borderwidth=1
#     )
# frame.grid(row=0, column=0)
# L1 = tk.Label(master=frame, text="Student ID:")
# L1.pack()

# # Id input
# frame = tk.Frame(
#     master=window,
#     relief=tk.RAISED,
#     borderwidth=1
#     )
# frame.grid(row=0, column=1)
# E1 = tk.Entry(master=frame, bd=5)
# E1.pack()

# # Begin Button
# frame = tk.Frame(
#     master=window,
#     relief=tk.RAISED,
#     borderwidth=1
#     )
# frame.grid(row=1, column=0)
# B1 = tk.Button(master=frame, text="Begin Exam", command=handleBegin)
# B1.pack()

# window.mainloop()