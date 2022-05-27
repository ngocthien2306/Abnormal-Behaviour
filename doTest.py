

import cv2
import pandas as pd
import time
from csv import writer
import mediapipe as mp
import requests
import os
import sys
import matplotlib.pyplot as plt
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtMultimedia import *
from PyQt5.QtMultimediaWidgets import *
from PyQt5.QtCore import QThread, QTimer
from camera import Camera
#%%

class MovieThread(QThread):
    def __init__(self, camera):
        super().__init__()
        self.camera = camera

    def run(self):
        self.camera.acquire_movie(200)
#%%

class MainWindow(QMainWindow):
    def __init__(self, camera = None):
        super(MainWindow, self).__init__()
        self.setWindowTitle("Exam")
        self.setGeometry(100, 100, 1200, 650)
        self.init = ()
        self.fullName = ""
        self.mssv = ""
        self.input_mssv = QTextEdit("", self)
        self.input_fname = QTextEdit("", self)
        self.input_phone = QTextEdit("", self)
        self.select_model = QComboBox(self)
        self.available_cameras = QCameraInfo.availableCameras()

        if not self.available_cameras:
            # exit the code
            sys.exit()
            
        self.status = QStatusBar()
        self.status.setStyleSheet("background : white;")
        self.setStatusBar(self.status)
        self.save_path = ""
        self.viewfinder = QCameraViewfinder(self)
        # showing this viewfinder
        
        toolbar = QToolBar("Camera Tool Bar")
        # adding tool bar to main window
        self.addToolBar(toolbar)
        
        click_action = QAction("Click photo", self)
        # adding status tip to the photo action
        click_action.setStatusTip("This will capture picture")
        # adding tool tip
        click_action.setToolTip("Capture picture")
        click_action.triggered.connect(self.click_photo)
  
        # adding this to the tool bar
        toolbar.addAction(click_action)
        # similarly creating action for changing save folder
        change_folder_action = QAction("Change save location",self)
  
        # adding status tip
        change_folder_action.setStatusTip("Change folder where picture will be saved saved.")
  
        # adding tool tip to it
        change_folder_action.setToolTip("Change save location")
  
        # setting calling method to the change folder action
        # when triggered signal is emitted
        change_folder_action.triggered.connect(self.change_folder)
  
        # adding this to the tool bar
        toolbar.addAction(change_folder_action)
  
        # creating a combo box for selecting camera
        camera_selector = QComboBox()
  
        # adding status tip to it
        camera_selector.setStatusTip("Choose camera to take pictures")
  
        # adding tool tip to it
        camera_selector.setToolTip("Select Camera")
        camera_selector.setToolTipDuration(2500)
  
        # adding items to the combo box
        camera_selector.addItems([camera.description() for camera in self.available_cameras])
  
        # adding action to the combo box
        # calling the select camera method
        camera_selector.currentIndexChanged.connect(self.select_camera)
  
        # adding this to tool bar
        toolbar.addWidget(camera_selector)
  
        # setting tool bar stylesheet
        toolbar.setStyleSheet("background : white;")

        self.camera = camera
        self.timer = QTimer()
        


  
    def change_folder(self):
        # open the dialog to select path
        path = QFileDialog.getExistingDirectory(self, "Picture Location", "")
        # if path is selected
        if path:
            # update the path
            self.save_path = path
  
            # update the sequence
            self.save_seq = 0
  
    # method for alerts
    def alert(self, msg):
  
        # error message
        error = QErrorMessage(self)
  
        # setting text to the error message
        error.showMessage(msg)
        
    def select_camera(self, i):

        # getting the selected camera
        self.camera = QCamera(self.available_cameras[i])
  
        # setting view finder to the camera
        self.camera.setViewfinder(self.viewfinder)
  
        # setting capture mode to the camera
        #self.camera.setCaptureMode(QCamera.CaptureStillImage)
  
        # if any error occur show the alert
        self.camera.error.connect(lambda: self.alert(self.camera.errorString()))
  
        # start the camera
        self.camera.start()
  
        # creating a QCameraImageCapture object
        self.capture = QCameraImageCapture(self.camera)
  
        # showing alert if error occur
        self.capture.error.connect(lambda error_msg, error, msg: self.alert(msg))
  
        # when image captured showing message
        self.capture.imageCaptured.connect(lambda d, i: self.status.showMessage("Image captured : "  + str(self.save_seq)))
        # getting current camera name
        self.current_camera_name = self.available_cameras[i].description()
  
        # initial save sequence
        self.save_seq = 0
        
    def click_photo(self):
        # time stamp
        timestamp = time.strftime("%d-%b-%Y-%H_%M_%S")
  
        # capture the image and save it on the save path
        self.capture.capture(os.path.join("C:/Users/hp/Downloads/HK2 21-22/Machine Learning/Final Project/ExamAntiCheat/image/", 
                                          "%s-%04d-%s.jpg" % (
            self.current_camera_name,
            self.save_seq,
            timestamp
        )))
        
      
  
        # increment the sequence
        self.save_seq += 1
      
    def start_program(self):
        self.hide()
        self.draw_ui_exam()
        #self.start()
        #self.nextFrameSlot()
        self.show_camera()
        self.show()
        
    def start(self):
        if not self.camera.open():
            print('failure')
            msgBox = QMessageBox()
            msgBox.setText("Failed to open camera.")
            msgBox.exec_()
            return


    def nextFrameSlot(self):
        frame = self.camera.read()
        #frame = self.camera.read_gray()
        image = QImage(frame, frame.shape[1], frame.shape[0], QImage.Format_RGB888)
        label = QLabel(self)
        pixmap = QPixmap(image)
        label.setPixmap(pixmap)
        label.setScaledContents(True)
        label.setGeometry(520, 50, 650, 300)
    
        self.show()

        
    def reset(self):
        print("A")
    
    def beginTest(self):
        cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        faceDetection = mp.solutions.face_detection.FaceDetection()
        data = []
        
        studentId = self.input_mssv.toPlainText()
        fullname = self.input_fname.toPlainText();
        phone = self.input_phone.toPlainText();
        model = self.select_model.currentText();
        
        if studentId == None or studentId == '':
            self.alert("Please enter student ID!")
            return
        if fullname == None or fullname == '':
            self.alert("Please enter your name!")
            return
        if phone == None or phone == '':
            self.alert("Please enter your phone!")
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
                cv2.imshow(fullname + " " + studentId,frame)
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
    
    def show_camera(self):
        self.viewfinder.show()
        # making it central widget of main window
        self.viewfinder.setGeometry(520, -110, 650, 600)
        #self.setCentralWidget(self.viewfinder)
        
        self.select_camera(0)
    
    def draw_ui_exam(self):
        label_title = QLabel("Wellcome Student to the test of HCMUTE", self)
        label_title.setGeometry(20, 30, 400, 50)
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
        self.input_phone.setFont(QFont('Roboto', 10))
        
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
    camera = Camera(0)
    app = QApplication(sys.argv)
    window = MainWindow(camera)
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