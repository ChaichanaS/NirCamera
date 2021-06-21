#from pypylon import pylon
import cv2
import numpy as np
import threading 
from datetime import datetime
from PyQt5.QtCore import pyqtSignal, pyqtSlot,QThread
import time
from imutils.video import FPS

class findPosition(QThread):
    send_Image_signal = pyqtSignal(np.ndarray)
    def __init__(self,parent=None):
        info = "Find position"
        self.font = cv2.FONT_HERSHEY_SIMPLEX
    def _findPosition(self,image,low,high):
        fps = FPS().start()
        lower = np.array([0, 0, low])
        upper = np.array([255, 255, high])
        temp_img = image.copy()
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, lower, upper)
        kernel = np.ones((1, 1), np.uint8)
        mask = cv2.erode(mask, kernel)
        # FILTER 20082020
        kernel = np.ones((5, 5), np.uint8)
        # Remove white noise
        opening = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        # Remove small black dots
        closing = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel)
        # Get back the fine boundary edges using dilation
        kernel1 = np.ones((2, 2), np.uint8)
        dilation = cv2.dilate(closing, kernel1, iterations=1)
        #cv2.imshow('Marked object to be extracted', dilation)
        # Contours detection
        if int(cv2.__version__[0]) > 3:
            # Opencv 4.x.x
            contours, _ = cv2.findContours(dilation, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        else:
            # Opencv 3.x.x
            _, contours, _ = cv2.findContours(dilation, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        # Get the outer contour (it has larger area than the inner contour)
        if (len(contours) > 1):
            c1 = max(contours, key=cv2.contourArea)
            # Define the bounding rectangle around the contour
            rect = cv2.minAreaRect(c1)
            # Get the 4 corner coordinates of the rectangle
            box = cv2.boxPoints(rect)
            box = np.int0(box)
            print("[INFO] box :")
            print(box)
            # Draw the bounding rectangle to show the marked object

            # Find area
            area = cv2.contourArea(c1)
            # epsilon = 0.08 * cv2.arcLength(c1, True)
            # approx = cv2.approxPolyDP(c1, epsilon, True)
            print("[INFO] Area : {:.2f}".format(area))
            if area > 10000:
                bdg_rect = cv2.drawContours(temp_img, [box], 0, (0, 0, 255), 2)
                Mo = cv2.moments(c1)
                # print(box[3][0])
                # print(box[2][0])
                # print(box[1][0])
                # print(box[0][0])
                xxx = box[3][0] - box[1][0]
                sizex = xxx*24/169
                print("[INFO] size : {} mm".format(sizex))
                yyy = box[3][1] - box[2][1]
                zeta = np.arctan(xxx / yyy) * 180 / np.pi
                print("[INFO] Zeta : {:.2f}".format(zeta))
                # print (Mo)
                if Mo["m00"] != 0:
                    # find centroid
                    cX = int(Mo["m10"] / Mo["m00"])
                    cY = int(Mo["m01"] / Mo["m00"])
                    # draw the contour and center of the shape on the image
                    # cv2.drawContours(bdg_rect, [c1], -1, (0, 255, 0), 2)

                    ###########  เขียนให้จำค่าก่อนหน้า และ ค่าสุดท้าย เอามาคำนวน หาความเร็ว
                    #cv2.circle(bdg_rect, (cX, cY), 7, (255, 125, 125), -1)
                    cv2.putText(bdg_rect, "size : {:.2f} mm".format(sizex) , (box[1][0]-50, box[1][1]), self.font, 2, (255, 125, 125), 5)
                    print(cX, cY)  # 09072020
                # cv2.imshow('Marked object to be extracted', bdg_rect)
                temp_img = bdg_rect
        else:
            cv2.putText(temp_img, "No detect", (320, 240), self.font, 2, (255, 125, 125), 5)
            sizex = 0

        fps.update()
        fps.stop()
        print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
        print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))
        return temp_img,sizex
