import sys
from interface import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtMultimedia import *
from PyQt5.QtMultimediaWidgets import *
from PyQt5.QtCore import QThread, QTimer
import pandas as pd


class MainWindow(QMainWindow):
  def __init__(self, parent=None):
    QMainWindow.__init__(self)
    self.ui = Ui_MainWindow()
    self.u = Ui_MainWindow()
    self.ui.setupUi(self)
    self.setWindowTitle("Abnormal Detection Group 3 SPKT")
    self.show()
    self.ui.loadDataStudent()
    
    # def loadDataStudent(self):

    #   raw_data = pd.read_csv('exam_data.csv')
    #   students = raw_data[["label", "phone", "student name", "id", "date", "ip", "model"]]

    #   row = 0
    #   self.tableStudentInfo.setRowCount(len(students))
    #   for student in students:
    #           self.tableStudentInfo.setItem(row, 0, QtWidgets.QTableWidgetItem(student["label"]))
    #           self.tableStudentInfo.setItem(row, 1, QtWidgets.QTableWidgetItem(student["id"]))
    #           self.tableStudentInfo.setItem(row, 2, QtWidgets.QTableWidgetItem(student["student name"]))
    #           self.tableStudentInfo.setItem(row, 3, QtWidgets.QTableWidgetItem(student["ip"]))
    #           self.tableStudentInfo.setItem(row, 4, QtWidgets.QTableWidgetItem(student["phone"]))
    #           self.tableStudentInfo.setItem(row, 5, QtWidgets.QTableWidgetItem(student["time"]))
    #           self.tableStudentInfo.setItem(row, 6, QtWidgets.QTableWidgetItem(student["model"]))
    #           row += 1
      

    
if __name__ == '__main__':
  app = QApplication(sys.argv)
  window = MainWindow()
  window.show()
  sys.exit(app.exec_())