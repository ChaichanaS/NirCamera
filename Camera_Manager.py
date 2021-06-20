
#from pypylon import pylon
import cv2
import numpy as np
import threading 
from datetime import datetime
from PyQt5.QtCore import pyqtSignal, pyqtSlot,QThread
import time


#region pylon
""" off class for pylon in macos"""
"""
class Camera(QThread):
    status_pixmap_signal = pyqtSignal(bool)  
    def __init__(self,name,parent=None):
        super(Camera, self).__init__(parent)
        info = "Camera Basler"
        self._nameThread = name
        self.camera = ""
        
    def start(self):
      
        #Basler
        #conecting to the first available camera
        self.camera = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())

        # Grabing Continusely (video) with minimal delay
        self.camera.StartGrabbing(pylon.GrabStrategy_LatestImageOnly) 
        self.converter = pylon.ImageFormatConverter()

        # converting to opencv bgr format
        self.converter.OutputPixelFormat = pylon.PixelType_BGR8packed
        self.converter.OutputBitAlignment = pylon.OutputBitAlignment_MsbAligned
        self.mStop = "False"
        
        #create thread for capturing images
       
            

        self.t1 = threading.Thread(target=self._update_frame)
        self.t1.daemon = True
        self.t1.start()
        
  
    def _update_frame(self):
        self.status_pixmap_signal.emit(self.camera.IsGrabbing())
        while self.camera.IsGrabbing():
            self.mStop = "False"
            try:
                self.grabResult = self.camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)
            except:
                self.status_pixmap_signal.emit(False)
                
            
            if self.mStop == "True":
                self.camera.StopGrabbing()
                self.camera.Close()
                break           
            if self.grabResult.GrabSucceeded():
                # Access the image data
                self.image = self.converter.Convert(self.grabResult)
                self.current_frame = self.image.GetArray()
               
            self.grabResult.Release()
        
                
    def Stop(self):
        self.mStop = "True"
        
    def Status(self):
        if self.camera != "":
            Status = "ON"
           
        else:
            Status = "OFF"
        return Status              
    # get the current frame
    def get_current_frame(self):
        return cv2.cvtColor(self.current_frame,cv2.COLOR_BGR2RGB)
   
              

class Camera_Callibration:
    def __init__(self):
        self.cam = Camera()
        self.cam.start()
        self.mStop = False
        self.CHECKERBOARD = (6,9)
        # termination criteria
        self.criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)       
        # prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
        self.objp = np.zeros((6*7,3), np.float32)
        self.objp[:,:2] = np.mgrid[0:7,0:6].T.reshape(-1,2)
        # Arrays to store object points and image points from all the images.
        self.objpoints = [] # 3d point in real world space
        self.imgpoints = [] # 2d points in image plane.
    def start(self):
        threading.Thread(target=self._calibration).start()
    def _calibration(self,image):
        self.i = 0
        
        while True:
             # save image to file, if pattern found
          
            self.ret, self.corners = cv2.findChessboardCorners(cv2.cvtColor(image,cv2.COLOR_BGR2GRAY), (7,6), None)
            if self.ret == True:
                filename = datetime.now().strftime('%Y%m%d_%Hh%Mm%Ss%f') + '.jpg'
                cv2.imwrite("pose/sample_images/" + filename, self.image)
                self.i += 1
                self.objpoints.append(self.objp)
                corners2 = cv2.cornerSubPix(self.image,self.corners, (11,11), (-1,-1), self.criteria)
                self.imgpoints.append(self.corners)
                # Draw and display the corners
                cv2.drawChessboardCorners(image, (7,6), corners2, self.ret)
            if self.i == 20:
                break
            if self.mStop == True:
                break
    def Stop(self):
        self.mStop = True
    def _current_image(self):
        font = cv2.FONT_HERSHEY_SIMPLEX
        self.Image = cv2.putText(self.image,"Calibration Camera : Keep Image " +str(self.i)+'/20',(100,100), font, 3,(0,0,255),2)  
        return self.Image
class VideoThread(QThread):
    change_pixmap_signal = pyqtSignal(np.ndarray)
    Stop_pixmap_signal = pyqtSignal()        
    def run(self):
        
        #Basler
        #conecting to the first available camera
        camera = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())

        # Grabing Continusely (video) with minimal delay
        camera.StartGrabbing(pylon.GrabStrategy_LatestImageOnly) 
        converter = pylon.ImageFormatConverter()

        # converting to opencv bgr format
        converter.OutputPixelFormat = pylon.PixelType_BGR8packed
        converter.OutputBitAlignment = pylon.OutputBitAlignment_MsbAligned
        self.mStop = False
        
        while camera.IsGrabbing():
            
            grabResult = camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)
            if self.mStop == True:
                #camera.StopGrabbing()
                camera.Close()
                break           
            if grabResult.GrabSucceeded():
                # Access the image data
                image = converter.Convert(grabResult)
                self.img = image.GetArray()
                self.change_pixmap_signal.emit(self.img)
    @pyqtSlot()
    def snap(self):
         #Basler
        # conecting to the first available camera
       
        camera = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())
        camera.Open()
        countOfImagesToGrab = 100
         # The parameter MaxNumBuffer can be used to control the count of buffers
         # allocated for grabbing. The default value of this parameter is 10.
        camera.MaxNumBuffer = 5

        # Start the grabbing of c_countOfImagesToGrab images.
        # The camera device is parameterized with a default configuration which
        # sets up free-running continuous acquisition.
        camera.StartGrabbingMax(countOfImagesToGrab)
        converter = pylon.ImageFormatConverter()

        # converting to opencv bgr format
        converter.OutputPixelFormat = pylon.PixelType_BGR8packed
        converter.OutputBitAlignment = pylon.OutputBitAlignment_MsbAligned
        self.mStop = False
        while camera.IsGrabbing():
            
            grabResult = camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)
            if self.mStop == True:
                break           
            if grabResult.GrabSucceeded():
                # Access the image data
                image = converter.Convert(grabResult)
                img = image.GetArray()
                self.change_pixmap_signal.emit(img)
                camera.Close()
                break
            else:
                print("Error: ", grabResult.ErrorCode, grabResult.ErrorDescription)
            grabResult.Release()
        camera.Close()

    @pyqtSlot()
    def Stop(self):
        self.mStop = True
    def _current_image(self):
        return self.img
"""
#endregion
class webcam(QThread):
    change_pixmap_signal = pyqtSignal(np.ndarray)        
    def run(self):
        
        cap = cv2.VideoCapture(0)
        self.mStop = False
    
        
        while True:
            ret, cv_img = cap.read()
            if ret:
                self.change_pixmap_signal.emit(cv_img)
        

      
     
        
    def Stop(self):
        self.mStop = True