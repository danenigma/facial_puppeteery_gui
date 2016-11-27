#!/usr/bin/env python

# import rospy
# from std_msgs.msg import String
# import Tkinter as tk
#
# hello_str = "none"
#
# def startPuppeteer():
#     global  hello_str
#     hello_str = "Starting Puppeteering"
#
# def takeSample():
#     global hello_str
#     hello_str = "Taking Sample"
#
# def imgViewer():
#     global hello_str
#     rospy.init_node('gui_node', anonymous=True)
#     rate = rospy.Rate(10) # .5tps
#     rospy.loginfo(hello_str)
#     pub.publish(hello_str)
#     rate.sleep()
#     window.after(10, imgViewer)
#
# if __name__ == '__main__':
#     try:
#         pub = rospy.Publisher('gui_topic1', String, queue_size=10)
#
#         window = tk.Tk()  # Makes main window
#         window.wm_title("GUI4 Facial-Puppeteery")
#         buttonsFrame = tk.Frame(window, width=400, height=200)
#         buttonsFrame.grid(row=10, column=20, padx=60, pady=80)
#
#         startPuppeteer = tk.Button(buttonsFrame, text="Start Puppeteer", font="Times|Serif|Bold", fg="Red", command=startPuppeteer)
#         startPuppeteer.pack(side=tk.LEFT)
#
#         takeSample = tk.Button(buttonsFrame, text="Take Sample", font="Times|Serif|Bold", fg="Red", command=takeSample)
#         takeSample.pack(side=tk.RIGHT)
#
#         window.geometry("%dx%d+%d+%d" % ((400, 200) + (800, 400)))
#
#         window.after(10, imgViewer)
#         window.mainloop()
#
#     except rospy.ROSInterruptException:
#         pass
import cv2
import rospy
from std_msgs.msg import String
import Tkinter as tk
import Image, ImageTk

hello_str = "none"

def startPuppeteer():
    global  hello_str
    hello_str = "Starting Puppeteering"

def takeSample():
    global hello_str
    hello_str = "Taking Sample"

def close():
    window.destroy()

def imgViewer():
    global hello_str
    rospy.init_node('gui_node', anonymous=True)
    # rate = rospy.Rate(1000) # .5tps
    rospy.loginfo(hello_str)
    pub.publish(hello_str)
    # rate.sleep()

    _, frame = cap.read()
    frame = cv2.flip(frame, 1)
    cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
    img = Image.fromarray(cv2image)
    imgtk = ImageTk.PhotoImage(image=img)

    display1.imgtk = imgtk #Shows frame for display 1
    display1.configure(image=imgtk)

    window.after(1, imgViewer)

if __name__ == '__main__':
    try:
        pub = rospy.Publisher('gui_topic1', String, queue_size=10)

        window = tk.Tk()
        window.wm_title("GUI4 Facial-Puppeteery")

        imageFrame = tk.Frame(window, width=600, height=500)
        imageFrame.grid(row=0, column=0, padx=10, pady=2)

        display1 = tk.Label(imageFrame)
        display1.grid(row=0, column=0, padx=10, pady=2)  # Display 1

        cap = cv2.VideoCapture(0)

        buttonsFrame = tk.Frame(window, width=100, height=20)
        buttonsFrame.grid(row=2, column=0, padx=10, pady=10)

        startPuppeteer = tk.Button(buttonsFrame, text="Start Puppeteer", font="Times|Serif|Bold", fg="Red", command=startPuppeteer)
        startPuppeteer.pack(side=tk.LEFT)

        takeSample = tk.Button(buttonsFrame, text="  Take Sample  ", font="Times|Serif|Bold", fg="Red", command=takeSample)
        takeSample.pack(side=tk.LEFT)

        takeSample = tk.Button(buttonsFrame, text="     Close     ", font="Times|Serif|Bold", fg="Red", command=close)
        takeSample.pack(side=tk.LEFT)

        window.geometry("%dx%d+%d+%d" % ((680, 560) + (500, 200)))

        window.after(1, imgViewer)
        window.mainloop()

    except rospy.ROSInterruptException:
        pass
