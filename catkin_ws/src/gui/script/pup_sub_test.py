#!/usr/bin/env python
#-*- coding:utf-8 -*-
__author__="danenigma"

import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import rospy
from std_msgs.msg import String 
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
from design  import Ui_MainWindow
from PyQt4 import QtGui
from PyQt4 import QtGui, QtCore, Qt
import cv2
import numpy as np

      

class controlThread(QThread):
    NODE_NAME = 'image_thread'
    def __init__(self,app):
        QThread.__init__(self)
	rospy.init_node(self.NODE_NAME)
        self.app = app
	self.th_pub    = rospy.Publisher('/gui_topic1',String,queue_size = 1)
	self.dlib_sub = rospy.Subscriber('/dlib_image',Image,self.dlib_cb)
	self.bridge = CvBridge()
	self.marker_pos = []
    def dlib_cb(self,data):
	"""callback for the marker"""
	self.app.currentFrame = self.bridge.imgmsg_to_cv2(data, "rgb8")

    def convertFrame(self):
        """     converts frame to format suitable for QtGui            """
        try:
            height,width=self.app.currentFrame.shape[:2]
            img=QtGui.QImage(self.app.currentFrame,
                              width,
                              height,
                              QtGui.QImage.Format_RGB888)
            img=QtGui.QPixmap.fromImage(img)
            self.app.previousFrame = self.app.currentFrame
            return img
        except:
            return None            
    def __del__(self):
        self.wait()

    def run(self):
	while True: self.th_pub.publish(self.app.variable)
	
class controlApp(QtGui.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(controlApp, self).__init__(parent)
        
	self.ui = Ui_MainWindow()
	self.ui.setupUi(self)
        self._timer = QtCore.QTimer(self)
        self._timer.timeout.connect(self.play)
        self._timer.start(27)
        self.update()
	self.variable = "none"
	self.ui.pushButton.clicked.connect(lambda : self.change(self.ui.pushButton))
	self.ui.pushButton_2.clicked.connect(lambda : self.change(self.ui.pushButton_2))
	self.T = controlThread(self)
	self.T.start()
	self.currentFrame = np.array([])	

    def change(self,b):
	"""change the value of variable"""
	if b.text()=="Taking Sample":
		self.variable = "Take Sample"	
	else :
		self.variable = "Start Puppeteering"
	
    def play(self):
        try:
            self.ui.videoFrame.setPixmap(
                self.T.convertFrame())
            self.ui.videoFrame.setScaledContents(True)
        except TypeError:
            print "No frame"	
def main():
   app = QApplication(sys.argv)
   ex = controlApp()
   ex.show()
   sys.exit(app.exec_())
	
if __name__ == '__main__':
   main()
