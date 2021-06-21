import multiprocessing as multi
from Motoplus import *
import tkinter as tk
import numpy as np
import Transfrom as Tran
import Cann as cn
import threading
import keyboard
import tkinter
import socket
import time
import sys
import cv2

from PIL.ImageTk import PhotoImage
from tkinter.constants import *
from imutils.video import FPS
from PIL import ImageTk
from PIL import Image

# setup parameter
panelA = None
panelB = None
delay = 15
speed = 10
pad = 3
font = cv2.FONT_HERSHEY_SIMPLEX
First_time = True


def init(root):
    # Setting windows name
    global l_h, l_s, l_v, u_h, u_s, u_v, Sp, St
    root.title('Project')
    p1 = PhotoImage(file=r'D:\testimg\vedio.png')
    # Setting icon of master window
    root.iconphoto(False, p1)
    # root.geometry("%dx%d" % (W,H))
    root.geometry("{0}x{1}+{2}+{3}".format(root.winfo_screenwidth() - pad, root.winfo_screenheight() - pad, -6, 0))
    # root.attributes('-fullscreen', True)
    load_condition()
    # default for upper and lower HSV
    tkvar0 = tk.DoubleVar()
    tkvar0.set(splitread[0])
    tkvar1 = tk.DoubleVar()
    tkvar1.set(splitread[1])
    tkvar2 = tk.DoubleVar()
    tkvar2.set(splitread[2])
    tkvar3 = tk.DoubleVar()
    tkvar3.set(splitread[3])
    tkvar4 = tk.DoubleVar()
    tkvar4.set(splitread[4])
    tkvar5 = tk.DoubleVar()
    tkvar5.set(splitread[5])
    # default robot speed
    tkvar6 = tk.DoubleVar()
    tkvar6.set(splitread[6])
    tkvar7 = tk.DoubleVar()
    tkvar7.set(splitread[7])

    button = tk.Button(root, text='บันทึก', font=80, command=save_condition).place(x=880, y=550)
    # for change color http://www.science.smith.edu/dftwiki/index.php/Color_Charts_for_TKinter

    l_h = tk.Scale(root, from_=0, to=180, variable=tkvar0, orient=HORIZONTAL, label="L-H", troughcolor="blue")
    l_h.place(x=0, y=500)
    l_s = tk.Scale(root, from_=0, to=255, variable=tkvar1, orient=HORIZONTAL, label="L-S", troughcolor="red")
    l_s.place(x=200, y=500)
    l_v = tk.Scale(root, from_=0, to=255, variable=tkvar2, orient=HORIZONTAL, label="L-V", troughcolor="green")
    l_v.place(x=400, y=500)
    u_h = tk.Scale(root, from_=0, to=180, variable=tkvar3, orient=HORIZONTAL, label="U-H", troughcolor="blue")
    u_h.place(x=0, y=550)
    u_s = tk.Scale(root, from_=0, to=255, variable=tkvar4, orient=HORIZONTAL, label="U-S", troughcolor="red")
    u_s.place(x=200, y=550)
    u_v = tk.Scale(root, from_=0, to=255, variable=tkvar5, orient=HORIZONTAL, label="U-V", troughcolor="green")
    u_v.place(x=400, y=550)
    Sp = tk.Spinbox(root, from_=10, to=1500, width=4, textvariable=tkvar6, state='readonly', increment=speed)
    Sp.place(x=600, y=540)
    St = tk.Spinbox(root, from_=10, to=100, width=4, textvariable=tkvar7, state='readonly', increment=speed)
    St.place(x=600, y=550)

    var = tk.StringVar()
    var.set("Test Label")
    label = tk.Label(root, textvariable=var, relief=RAISED)
    label.place(x=150, y=0)
    # Creating Menubar
    menubar = tk.Menu(root)

    # Adding File Menu and commands
    file = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label='File', menu=file)
    file.add_command(label='New File', command=None)
    file.add_command(label='Open...', command=None)
    file.add_command(label='Save', command=None)
    file.add_separator()
    file.add_command(label='Exit', command=root.destroy)

    # Adding Edit Menu and commands
    edit = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label='Edit', menu=edit)
    edit.add_command(label='Cut', command=None)
    edit.add_command(label='Copy', command=None)
    edit.add_command(label='Paste', command=None)
    edit.add_command(label='Select All', command=None)
    edit.add_separator()
    edit.add_command(label='Find...', command=None)
    edit.add_command(label='Find again', command=None)

    # Adding Help Menu
    help_ = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label='Help', menu=help_)
    help_.add_command(label='Tk Help', command=None)
    help_.add_command(label='Demo', command=None)
    help_.add_separator()
    help_.add_command(label='About Tk', command=None)

    # display Menu
    root.config(menu=menubar)


def close(event):
    cap.release()
    root.withdraw()  # if you want to bring it back
    sys.exit()  # if you want to exit the entire thing


def update():
    global panelA, panelB
    if cap.isOpened():
        ret, image = cap.read()
        if ret:
            mask = find_position(image)
            mask = cv2.cvtColor(mask, cv2.COLOR_BGR2RGB)
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            edged = cv2.Canny(gray, 50, 100)
            image = ImageTk.PhotoImage(image=Image.fromarray(image))
            edged = ImageTk.PhotoImage(image=Image.fromarray(edged))
            mask = ImageTk.PhotoImage(image=Image.fromarray(mask))
            if panelA is None or panelB is None:
                panelA = tk.Label(image=image)
                panelA.image = image
                panelA.place(x=5, y=20)
                panelB = tk.Label(image=mask)
                panelB.image = mask
                panelB.place(x=670, y=20)
                print("Again2649")
            else:
                # update the panels
                panelA.configure(image=image)
                panelB.configure(image=mask)
                panelA.image = image
                panelB.image = mask
                print("Again0000")
    root.bind('<Escape>', close)
    root.bind('<Up>', close)
    print("Again1")
    root.after(delay, update)


def find_position(image):
    # global l_h, l_s, l_v, u_h, u_s, u_v
    fps = FPS().start()
    lower = np.array([l_h.get(), l_s.get(), l_v.get()])
    upper = np.array([u_h.get(), u_s.get(), u_v.get()])
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
    cv2.imshow('Marked object to be extracted', dilation)
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
                cv2.putText(bdg_rect, "size : {:.2f} mm".format(sizex) , (box[1][0]-50, box[1][1]), font, 0.5, (255, 125, 125), 2)
                print(cX, cY)  # 09072020
            # cv2.imshow('Marked object to be extracted', bdg_rect)
            temp_img = bdg_rect
    else:
        cv2.putText(temp_img, "No detect", (320, 240), font, 0.5, (255, 125, 125), 2)

    fps.update()
    fps.stop()
    print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
    print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))
    return temp_img


def load_condition():
    global splitread
    file1 = open("MyFile2.txt", "r")
    read = file1.read()
    print(file1.read())
    splitread = read.split(",")
    file1.close()


def save_condition():
    file1 = open("MyFile2.txt", "w")
    lh = int(l_h.get())
    ls = int(l_s.get())
    lv = int(l_v.get())
    uh = int(u_h.get())
    us = int(u_s.get())
    uv = int(u_v.get())
    sp = int(Sp.get())
    st = int(St.get())
    file1.write("{0},{1},{2},{3},{4},{5},{6},{7}".format(lh, ls, lv, uh, us, uv, sp, st))
    file1.close()

    file1 = open("MyFile2.txt", "r")
    print(file1.read())
    file1.close()


# Run
if First_time:
    root = tk.Tk()
    init(root)
    First_time = False
    cap = cv2.VideoCapture(0)
update()
root.mainloop()

# point1 = [1, 1, 0]
# point2 = [5, 4, 0]
# rotation = [0, 0, 0]
# translation = [5, 4, 0]
# mat = Tran.matrix(rotation, translation)
# print(mat)
# start = Tran.transform(point1, mat)
# print(start)


# ใต้นี้ไม่ทำ
# canvas = tk.Canvas(root, height=H, width=W)
# canvas.pack()

# p = multi.Process(target=show_values2())
# p.start()

# def on_click_callback(on):
#     if on:
#         print('led is on')
#     else:
#         print('led is off')
# led0 = cn.Led(root, size=50, on_click_callback=on_click_callback)
# led0.pack()

# tk.Button(root,text='red on',command=lambda: led0.to_red(True)).pack(fill=tk.X)
# #tk.Button(root, text='green', command=led0.to_green).pack(fill=tk.X)
# tk.Button(root,text='green on',command=lambda: led0.to_green(True)).pack(fill=tk.X)
# #tk.Button(root, text='yellow', command=led0.to_yellow).pack(fill=tk.X)
# tk.Button(root,text='yellow on',command=lambda: led0.to_yellow(True)).pack(fill=tk.X)
# tk.Button(root, text='grey', command=led0.to_grey).pack(fill=tk.X)
# tk.Label(root, text='Clickable LED').pack(fill=tk.X)
