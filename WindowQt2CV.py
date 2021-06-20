import threading
import concurrent
import cv2
import numpy as np
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QVBoxLayout
from PyQt5.QtGui import QPixmap, QImage, QColor,QPen,QPainter,QBrush,QFont
from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt,QObject,QThread,QRect
#from Carlibration_Cameara import LinearRegression
class Display(QThread):
    
    def __init__(self,width,hight ,parent=None):
        super(Display, self).__init__(parent)
        self.disply_width =  width
        self.display_height = hight

       
    def start(self):
        print("Display Start")
    def run(self,Image):
        Main = threading.Thread(target=self.MainWindow_update_image,args=(Image,))
        Main.start()
        Main.join()
  

    def MainWindow_update_image(self, cv_img):
        """Updates the image_label with a new opencv image"""  
        with concurrent.futures.ThreadPoolExecutor() as _exe:   
            future = _exe.submit(self.convert_cv_qt,cv_img)
            self.qt_img = future.result()
        
           
    def convert_cv_qt(self, cv_img):
        """Convert from an opencv image to QPixmap"""
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QtGui.QImage(rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
        p = convert_to_Qt_format.scaled(self.disply_width, self.display_height, Qt.KeepAspectRatio)
        return QPixmap.fromImage(p)
    def get_img(self):
        return self.qt_img
class SmartWindow(QLabel):
    x0 = 0
    y0 = 0
    x1 = 0
    y1 = 0
    flag = False
    new_rectangle_signal = pyqtSignal()
    def __init__(self, parent=None):
        QWidget.__init__(self, parent=parent)
        self.Rectangle = "False"
        self.Point = "False"
        # self.modelX = LinearRegression()
        # self.modelX.LoadModel("./data/Master_Model/Model_X_Position.sav")
        # self.modelY = LinearRegression()
        # self.modelY.LoadModel("./data/Master_Model/Model_Y_Position.sav")
      
        
      # 
    def mousePressEvent(self,event):
        
        
        if self.Rectangle == "True":
            self.flag = True
            self.x0 = event.x()
            self.y0 = event.y()
        if self.Point == "True":
            self.flag = True
            self.x0 = event.x()
            self.y0 = event.y()
         # 
    def mouseReleaseEvent(self,event):
        
        if self.Rectangle == "True":
            self.flag = False
        if self.Point == "True":
            self.update()
         # 
    def mouseMoveEvent(self,event):
        
        if self.Rectangle == "True":
            if self.flag:
                self.x1 = event.x()
                self.y1 = event.y()
                self.update()
       
    def paintEvent(self, event):
        super().paintEvent(event)
        
        if self.Rectangle == "True":
            rect =QRect(self.x0, self.y0, abs(self.x1-self.x0), abs(self.y1-self.y0))
            painter = QPainter(self)
            painter.setPen(QPen(Qt.red,2,Qt.SolidLine))
            painter.drawRect(rect)
        if self.Point == "True":
            if self.x0 != 0:
                point = QPainter(self)
                point.setPen(QPen(Qt.red,20,Qt.SolidLine))
                point.setBrush(QBrush(Qt.red, Qt.SolidPattern))
                point.setFont(QFont('Helvetica', 20))
                point.drawEllipse(self.x0, self.y0,5,5)
                Xc = self.modelX.Predcit_Model(self.x0*3.2)
                Yc = self.modelY.Predcit_Model(self.y0*3.2)
                point.drawText(self.x0 +20, self.y0+20,"P1")
                point.drawText(500, 75,"P1({},{})".format(Xc,Yc))
            
            

    def _Off_Rectangle(self):
        self.Rectangle = "False"
    def _On_Rectangle(self):
        self.Rectangle = "True"
    def _Off_Point(self):
        self.Point = "False"
    def _On_Point(self,ModelX,ModelY):
        self.Point = "True"
        # self.modelX = LinearRegression()
        # self.modelX.LoadModel(ModelX)
        # self.modelY = LinearRegression()
        # self.modelY.LoadModel(ModelY)
  
   

 