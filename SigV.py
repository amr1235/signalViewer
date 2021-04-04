# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'SigV.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.Qt import Qt
import pandas as pd
import numpy as np
import pyqtgraph 
from pyqtgraph import PlotWidget , GraphicsLayoutWidget
import time as t
from scipy import signal
import matplotlib.pyplot as plt
import random
from PyQt5.QtGui import QPixmap




class clickableLabel(QtWidgets.QLabel) : 
    def __init__(self) : 
        super().__init__()
        self.clickMethod = None
        
    
    def mousePressEvent(self, ev):
        if ev.buttons() == QtCore.Qt.LeftButton :
            self.clickMethod()

class mainWindow(QtWidgets.QMainWindow) : 
    def __init__(self,parent = None) : 
        super().__init__()
        self.KeyUpMethod = None
        self.KeyDownMethod = None
        self.KeyLeftMethod = None
        self.KeyRightMethod = None
        self.spaceMethod = None
        self.number_1_method = None
        self.number_2_method = None
        self.number_3_method = None
        self.windowResizeMethod = None
    
    def keyPressEvent(self, ev) :
        if ev.key() == Qt.Key_Up : 
            self.KeyUpMethod(ev)
        if ev.key() == Qt.Key_Down :
            self.KeyDownMethod(ev)
        if ev.key() == Qt.Key_Left :
            self.KeyLeftMethod(ev)
        if ev.key() == Qt.Key_Right : 
            self.KeyRightMethod(ev)
        if ev.key() == Qt.Key_Space : 
            self.spaceMethod(ev)
        if ev.key() == Qt.Key_1 : 
            self.number_1_method(ev) 
        if ev.key() == Qt.Key_2 :
            self.number_2_method(ev)
        if ev.key() == Qt.Key_3 : 
            self.number_3_method(ev)
    def resizeEvent(self, ev) : 
        self.windowResizeMethod(ev)





class Ui_SignalViewer(object):

    def __init__(self):
        self.selectedSignal = 0
        self.fileNames = None
        self.isPaused = False

        self.plotIndex1 = 200
        self.xPointer1  = 0
        self.plot1 = None
        self.scrollStep1 = None

        self.plotIndex2 = 200
        self.xPointer2  = 0
        self.plot2 = None
        self.scrollStep2 = None

        self.plotIndex3 = 200
        self.xPointer3  = 0
        self.plot3 = None
        self.scrollStep3 = None

        self.xRangeStack1 = []
        self.yRangeStack1 = []

        self.xRangeStack2 = []
        self.yRangeStack2 = []

        self.xRangeStack3 = []
        self.yRangeStack3 = []

        self.xRangeOfSignal1 = [] # from , to 
        self.yRangeOfSignal1 = []

        self.xRangeOfSignal2 = []
        self.yRangeOfSignal2 = []
        
        self.xRangeOfSignal3 = []
        self.yRangeOfSignal3 = []



    def setupUi(self, SignalViewer):
        SignalViewer.setObjectName("SignalViewer")
        SignalViewer.resize(1350, 690)
        # SignalViewer.setFixedWidth(1350)
        # SignalViewer.setFixedHeight(690)
        SignalViewer.setTabShape(QtWidgets.QTabWidget.Triangular)
        SignalViewer.KeyUpMethod = self.key_up
        SignalViewer.KeyDownMethod = self.key_down    
        SignalViewer.KeyLeftMethod = self.key_left
        SignalViewer.KeyRightMethod = self.key_right
        SignalViewer.spaceMethod = self.spaceClicked
        SignalViewer.number_1_method = self.number_1_clicked
        SignalViewer.number_2_method = self.number_2_clicked
        SignalViewer.number_3_method = self.number_3_clicked
        SignalViewer.windowResizeMethod = self.windowResize
        
        self.centralwidget = QtWidgets.QWidget(SignalViewer)
        self.centralwidget.setObjectName("centralwidget")
        SignalViewer.setCentralWidget(self.centralwidget)
        

        self.menubar = QtWidgets.QMenuBar(SignalViewer)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 802, 27))
        self.menubar.setCursor(QtGui.QCursor(QtCore.Qt.OpenHandCursor))
        self.menubar.setAutoFillBackground(True)
        self.menubar.setStyleSheet("")
        self.menubar.setDefaultUp(False)
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setToolTipsVisible(False)
        self.menuFile.setObjectName("menuFile")
        self.menuEdit = QtWidgets.QMenu(self.menubar)
        SignalViewer.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(SignalViewer)
        self.statusbar.setObjectName("statusbar")
        SignalViewer.setStatusBar(self.statusbar)
        self.toolBar = QtWidgets.QToolBar(SignalViewer)
        self.toolBar.setEnabled(True)
        self.toolBar.setMouseTracking(True)
        self.toolBar.setMovable(False)
        self.toolBar.setObjectName("toolBar")
        SignalViewer.addToolBar(QtCore.Qt.BottomToolBarArea, self.toolBar)
        self.toolBar_2 = QtWidgets.QToolBar(SignalViewer)
        self.toolBar_2.setObjectName("toolBar_2")
        SignalViewer.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar_2)
        # open file
        self.actionnew_file = QtWidgets.QAction(SignalViewer)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("icons/folder.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionnew_file.setIcon(icon)
        self.actionnew_file.setObjectName("actionnew_file")
        self.actionnew_file.triggered.connect(self.selectFolder)

        # zoom in H
        self.actionzoom_in_h = QtWidgets.QAction(SignalViewer)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("icons/ic_zoom_in_h_black_24dp.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionzoom_in_h.setIcon(icon1)
        self.actionzoom_in_h.setObjectName("actionzoom_in_h")
        self.actionzoom_in_h.triggered.connect(self.zoom_in_h)
        self.shortcutZoom_in_h = QtWidgets.QShortcut(QtGui.QKeySequence("Ctrl+H"),SignalViewer)
        self.shortcutZoom_in_h.activated.connect(self.zoom_in_h)
        self.actionzoom_in_h.setEnabled(False)
        # zoom out H 
        self.actionzoom_out_h = QtWidgets.QAction(SignalViewer)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("icons/ic_zoom_out_h_black_24dp.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionzoom_out_h.setIcon(icon1)
        self.actionzoom_out_h.setObjectName("actionzoom_out_h")
        self.actionzoom_out_h.triggered.connect(self.zoom_out_h)
        self.shortcutZoom_out_h = QtWidgets.QShortcut(QtGui.QKeySequence("Shift+H"),SignalViewer)
        self.shortcutZoom_out_h.activated.connect(self.zoom_out_h)
        self.actionzoom_out_h.setEnabled(False)
        # zoom in v 
        self.actionzoom_in_v = QtWidgets.QAction(SignalViewer)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("icons/ic_zoom_in_v_black_24dp.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionzoom_in_v.setIcon(icon1)
        self.actionzoom_in_v.setObjectName("actionzoom_in_v")
        self.actionzoom_in_v.triggered.connect(self.zoom_in_v)
        self.shortcutZoom_in_v = QtWidgets.QShortcut(QtGui.QKeySequence("Ctrl+V"),SignalViewer)
        self.shortcutZoom_in_v.activated.connect(self.zoom_in_v)
        self.actionzoom_in_v.setEnabled(False)
        # zoom out v 
        self.actionzoom_out_v = QtWidgets.QAction(SignalViewer)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("icons/ic_zoom_out_v_black_24dp.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionzoom_out_v.setIcon(icon1)
        self.actionzoom_out_v.setObjectName("actionzoom_out_v")
        self.actionzoom_out_v.triggered.connect(self.zoom_out_v)
        self.shortcutZoom_out_v = QtWidgets.QShortcut(QtGui.QKeySequence("Shift+V"),SignalViewer)
        self.shortcutZoom_out_v.activated.connect(self.zoom_out_v)
        self.actionzoom_out_v.setEnabled(False)

        #pause 
        self.actionPause = QtWidgets.QAction(SignalViewer)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("icons/pause.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionPause.setIcon(icon1)
        self.actionPause.setObjectName("actionPause")
        self.actionPause.triggered.connect(self.pause)
        self.actionPause.setEnabled(False)

        #resume
        self.actionResume = QtWidgets.QAction(SignalViewer)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("icons/start.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionResume.setIcon(icon1)
        self.actionResume.setObjectName("actionPause")
        self.actionResume.triggered.connect(self.resume)
        self.actionResume.setEnabled(False)
        #save file
        self.actionsave_file = QtWidgets.QAction(SignalViewer)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("icons/diskette.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionsave_file.setIcon(icon3)
        self.actionsave_file.setObjectName("actionsave_file")
        self.actionsave_file.triggered.connect(self.generateReport)
        self.actionsave_file.setEnabled(False)

        #background
        self.backGround = QtWidgets.QLabel("")
        self.backGround.setGeometry(0,60,SignalViewer.width(),SignalViewer.height())
        self.backGround.setParent(SignalViewer)
        pixmap = QPixmap('BackGround.PNG')
        self.backGround.setPixmap(pixmap)
        self.backGround.setScaledContents(True)
        self.backGround.show()
        # select Folder
        self.actionChoose_File = QtWidgets.QAction(SignalViewer)
        self.actionChoose_File.setObjectName("actionChoose_File")
        self.actionChoose_File.triggered.connect(self.selectFolder)

        self.menuFile.addAction(self.actionChoose_File)
        self.menubar.addAction(self.menuFile.menuAction())
        self.toolBar_2.addSeparator()
        self.toolBar_2.addAction(self.actionnew_file)
        self.toolBar_2.addAction(self.actionsave_file)
        self.toolBar_2.addAction(self.actionzoom_in_h)
        self.toolBar_2.addAction(self.actionzoom_out_h)
        self.toolBar_2.addAction(self.actionzoom_in_v)
        self.toolBar_2.addAction(self.actionzoom_out_v)
        self.toolBar_2.addAction(self.actionPause)  
        self.toolBar_2.addAction(self.actionResume)

        #signal 1 == channel 1
        self.channelLabel1 = QtWidgets.QLabel("Channel 1")
        self.channelLabel1.setGeometry(5, 5, 50, 20)
        self.channelLabel1.setParent(self.centralwidget)
        self.channelLabel1.show()
        self.channelLabel1.setObjectName("channelLabel1")

        self.signal1 = GraphicsLayoutWidget(self.centralwidget)
        self.signal1.setGeometry(QtCore.QRect(5, 30,int((SignalViewer.width() - 20) / 2 ),170))
        self.signal1.setObjectName("signal1")
            # label to cover channel 1 
        self.labelForSignal1 = clickableLabel()
        self.labelForSignal1.setParent(self.signal1)
        self.labelForSignal1.setGeometry(QtCore.QRect(0, 0,self.signal1.width(),self.signal1.height()))
        self.labelForSignal1.show()
        self.labelForSignal1.setObjectName("label1")
        self.labelForSignal1.clickMethod = self.signal1Clicked
            #label for spectogram of channel 1 
        self.spectoLabel1 = QtWidgets.QLabel("spectogram for channel 1")
        self.spectoLabel1.setGeometry(int(self.signal1.width()) + 10, 5, 150, 20)
        self.spectoLabel1.setParent(self.centralwidget)
        self.spectoLabel1.show()
        self.spectoLabel1.setObjectName("spectoLabel1")
            # spectogram of channel 1 we will name it signal 2 to be easly detect
        self.signal4 = GraphicsLayoutWidget(self.centralwidget)
        self.signal4.setGeometry(self.signal1.width() + 10, 30,self.signal1.width(),170)
        self.signal4.setObjectName("signal2")


        #signal 3 == channel 2
        self.channelLabel2 = QtWidgets.QLabel("Channel 2")
        self.channelLabel2.setGeometry(5, self.signal1.height() + 30, 50, 20)
        self.channelLabel2.setParent(self.centralwidget)
        self.channelLabel2.show()
        self.channelLabel2.setObjectName("channelLabel 2")

        self.signal2 = GraphicsLayoutWidget(self.centralwidget)
        self.signal2.setGeometry(QtCore.QRect(5, self.signal1.height() + 55,  self.signal1.width() ,170))
        self.signal2.setObjectName("signal3")
            # label to cover channel 1 
        self.labelForSignal3 = clickableLabel()
        self.labelForSignal3.setParent(self.signal2)
        self.labelForSignal3.setGeometry(QtCore.QRect(0, 0,self.signal2.width(),self.signal2.height()))
        self.labelForSignal3.show()
        self.labelForSignal3.setObjectName("label2")
        self.labelForSignal3.clickMethod = self.signal2Clicked
            #label for spectogram of channel 1 
        self.spectoLabel2 = QtWidgets.QLabel("spectogram for channel 2")
        self.spectoLabel2.setGeometry(int(self.signal1.width()) + 10, self.signal4.height() + 30, 150, 20)
        self.spectoLabel2.setParent(self.centralwidget)
        self.spectoLabel2.show()
        self.spectoLabel2.setObjectName("specto2")
            # spectogram of channel 2 we will name it signal 4 to be easly detect
        self.signal5 = GraphicsLayoutWidget(self.centralwidget)
        self.signal5.setGeometry( self.signal1.width() + 10, self.signal4.height() + 55,self.signal1.width(),170)
        self.signal5.setObjectName("signal2")

        #signal 5 channel 3 
        self.channelLabel3 = QtWidgets.QLabel("Channel 3")
        self.channelLabel3.setGeometry(5, self.signal1.height() + self.signal2.height() + 60, 50, 20)
        self.channelLabel3.setParent(self.centralwidget)
        self.channelLabel3.show()
        self.channelLabel3.setObjectName("channelLabel 3")

        self.signal3 = GraphicsLayoutWidget(self.centralwidget)
        self.signal3.setGeometry(QtCore.QRect(5, self.signal1.height() + self.signal2.height() + 85,  self.signal1.width() ,170))
        self.signal3.setObjectName("signal5")
            # label to cover channel 1 
        self.labelForSignal5 = clickableLabel()
        self.labelForSignal5.setParent(self.signal3)
        self.labelForSignal5.setGeometry(QtCore.QRect(0, 0,self.signal3.width(),self.signal3.height()))
        self.labelForSignal5.show()
        self.labelForSignal5.setObjectName("label2")
        self.labelForSignal5.clickMethod = self.signal3Clicked
            #label for spectogram of channel 1 
        self.spectoLabel3 = QtWidgets.QLabel("spectogram for channel 3")
        self.spectoLabel3.setGeometry(self.signal1.width() + 10, self.signal5.height() + self.signal4.height() + 60, 150, 20)
        self.spectoLabel3.setParent(self.centralwidget)
        self.spectoLabel3.show()
        self.spectoLabel3.setObjectName("specto3")
            # spectogram of channel 3 we will name it signal 6 to be easly detect
        self.signal6 = GraphicsLayoutWidget(self.centralwidget)
        self.signal6.setGeometry( self.signal1.width() + 10, self.signal2.height()+ self.signal3.height() + 85,self.signal1.width(),170)
        self.signal6.setObjectName("signal2")

        #timer
        self.timer1 = QtCore.QTimer()
        self.timer2 = QtCore.QTimer()
        self.timer3 = QtCore.QTimer()
        

        self.retranslateUi(SignalViewer)
        QtCore.QMetaObject.connectSlotsByName(SignalViewer)

    def retranslateUi(self, SignalViewer):
        _translate = QtCore.QCoreApplication.translate
        SignalViewer.setWindowTitle(_translate("SignalViewer", "Signal Viewer"))
        self.menuFile.setTitle(_translate("SignalViewer", "File"))
        self.toolBar.setWindowTitle(_translate("SignalViewer", "toolBar"))
        self.toolBar_2.setWindowTitle(_translate("SignalViewer", "toolBar_2"))
        self.actionnew_file.setText(_translate("SignalViewer", "newfile"))
        self.actionnew_file.setShortcut(_translate("SignalViewer","Ctrl+N"))
        self.actionzoom_in_h.setText(_translate("SignalViewer", "zoom in horizontally"))
        self.actionzoom_in_h.setShortcut(_translate("SignalViewer", "Ctrl+H+Plus"))
        self.actionzoom_out_h.setText(_translate("SignalViewer", "zoom out horizontally"))
        self.actionzoom_out_h.setShortcut(_translate("SignalViewer", "Ctrl+Minus+H"))
        self.actionzoom_in_v.setText(_translate("SignalViewer", "zoom in virtically"))
        self.actionzoom_in_v.setShortcut(_translate("SignalViewer", "Ctrl+Plus+V"))
        self.actionzoom_out_v.setText(_translate("SignalViewer", "zoom out virtically"))
        self.actionzoom_out_v.setShortcut(_translate("SignalViewer", "Ctrl+Minus+V"))
        self.actionPause.setText(_translate("SignalViewer", "Pause"))
        self.actionResume.setText(_translate("SignalViewer", "Resume"))
        self.actionsave_file.setText(_translate("SignalViewer", "save file"))
        self.actionsave_file.setShortcut(_translate("SignalViewer", "Ctrl+S"))
        self.actionChoose_File.setText(_translate("SignalViewer", "Choose File"))
    
    def windowResize(self,event) : 
        self.signal1.setGeometry(QtCore.QRect(5, 30,int((SignalViewer.width() - 20) / 2 ),170))
        self.signal4.setGeometry(self.signal1.width() + 10, 30,self.signal1.width(),170)
        self.signal2.setGeometry(QtCore.QRect(5, self.signal1.height() + 55,  self.signal1.width() ,170))
        self.signal5.setGeometry( self.signal1.width() + 10, self.signal4.height() + 55,self.signal1.width(),170)
        self.signal3.setGeometry(QtCore.QRect(5, self.signal1.height() + self.signal2.height() + 85,  self.signal1.width() ,170))
        self.signal6.setGeometry( self.signal1.width() + 10, self.signal2.height()+ self.signal3.height() + 85,self.signal1.width(),170)


    def enableWidgets(self) : 
        self.backGround.hide()
        self.actionPause.setEnabled(True)
        self.actionResume.setEnabled(True)
        self.actionzoom_in_h.setEnabled(True)
        self.actionzoom_in_v.setEnabled(True)
        self.actionzoom_out_h.setEnabled(True)
        self.actionzoom_out_v.setEnabled(True)
        self.actionsave_file.setEnabled(True)
    
    def spaceClicked(self,ev) : 
        if self.selectedSignal == 0 :
            self.warnDialog("please Select Signal")
        else : 
            if self.isPaused : 
                self.resume()
                self.isPaused = not self.isPaused
            else : 
                self.pause()
                self.isPaused = not self.isPaused


    def number_1_clicked(self,ev) : 
        self.selectedSignal = 1 

    def number_2_clicked(self,ev) : 
        self.selectedSignal = 2
    
    def number_3_clicked(self,ev) : 
        self.selectedSignal = 3



    def selectFolder(self) :
        dialog = QtWidgets.QFileDialog()
        dialog.setFileMode(QtWidgets.QFileDialog.AnyFile)
        directory = dialog.getOpenFileNames(None,'select file','c:\\','csv files (*.csv)')
        self.fileNames = directory[0]

        if len(self.fileNames) == 0 : self.warnDialog("please Select data files")
        if len(self.fileNames) >= 4 :
            self.warnDialog("please Select 3 files or less")

        if len(self.fileNames) == 3 :
            self.enableWidgets()
            #read 3 files
            csvFile1 = pd.read_csv(self.fileNames[0])
            csvFile2 = pd.read_csv(self.fileNames[1])
            csvFile3 = pd.read_csv(self.fileNames[2])

            # exctract data to draw signal 1 
            self.time1 = csvFile1.iloc[:,0]
            self.volts1 = csvFile1.iloc[:,1]
            self.sampleTime1 = self.time1[1] - self.time1[0]
            self.scrollStep1 = 10 * self.sampleTime1
            #plot spectogram
            self.drawSpectoForSignal1(self.signal4, self.volts1, 1 / self.sampleTime1)
            # plot the signal 
            self.plot1 = self.signal1.addPlot()
            self.plot1.plot(self.time1[self.xPointer1:self.plotIndex1],self.volts1[self.xPointer1:self.plotIndex1])
            self.plot1.setXRange(self.time1[self.xPointer1],self.time1[self.plotIndex1])
            self.timer1.timeout.connect(self.update1)
            self.timer1.start(50)

            # exctract data to draw signal 2 
            self.time2 = csvFile2.iloc[:,0]
            self.volts2 = csvFile2.iloc[:,1]
            self.sampleTime2 = self.time2[1] - self.time2[0]
            self.scrollStep2 = 10 * self.sampleTime2
            #plot spectogram
            self.drawSpectoForSignal1(self.signal5, self.volts2, 1 / self.sampleTime2)
            # plot the signal 
            self.plot2 = self.signal2.addPlot()
            self.plot2.plot(self.time2[self.xPointer2:self.plotIndex2],self.volts2[self.xPointer2:self.plotIndex2])
            self.plot2.setXRange(self.time2[self.xPointer2],self.time2[self.plotIndex2])
            self.timer2.timeout.connect(self.update2)
            self.timer2.start(50)

            # exctract data to draw signal 3 
            self.time3 = csvFile3.iloc[:,0]
            self.volts3 = csvFile3.iloc[:,1]
            self.sampleTime3 = self.time3[1] - self.time3[0]
            self.scrollStep3 = 10 * self.sampleTime3
            #plot spectogram
            self.drawSpectoForSignal1(self.signal6, self.volts3, 1 / self.sampleTime3)
            # plot the signal 
            self.plot3 = self.signal3.addPlot()
            self.plot3.plot(self.time3[self.xPointer3:self.plotIndex3],self.volts3[self.xPointer3:self.plotIndex3])
            self.plot3.setXRange(self.time3[self.xPointer3],self.time3[self.plotIndex3])
            self.timer3.timeout.connect(self.update3)
            self.timer3.start(50)

        if len(self.fileNames) == 2 : 
            self.enableWidgets()
            #read 2 files
            csvFile1 = pd.read_csv(self.fileNames[0])
            csvFile2 = pd.read_csv(self.fileNames[1])

            # exctract data to draw signal 1 
            self.time1 = csvFile1.iloc[:,0]
            self.volts1 = csvFile1.iloc[:,1]
            self.sampleTime1 = self.time1[1] - self.time1[0]
            self.scrollStep1 = 10 * self.sampleTime1
            #plot spectogram
            self.drawSpectoForSignal1(self.signal4, self.volts1, 1 / self.sampleTime1)
            # plot the signal 
            self.plot1 = self.signal1.addPlot()
            self.plot1.plot(self.time1[self.xPointer1:self.plotIndex1],self.volts1[self.xPointer1:self.plotIndex1])
            self.plot1.setXRange(self.time1[self.xPointer1],self.time1[self.plotIndex1])
            self.timer1.timeout.connect(self.update1)
            self.timer1.start(50)

            # exctract data to draw signal 2 
            self.time2 = csvFile2.iloc[:,0]
            self.volts2 = csvFile2.iloc[:,1]
            self.sampleTime2 = self.time2[1] - self.time2[0]
            self.scrollStep2 = 10 * self.sampleTime2
            #plot spectogram
            self.drawSpectoForSignal1(self.signal5, self.volts2, 1 / self.sampleTime2)
            # plot the signal 
            self.plot2 = self.signal2.addPlot()
            self.plot2.plot(self.time2[self.xPointer2:self.plotIndex2],self.volts2[self.xPointer2:self.plotIndex2])
            self.plot2.setXRange(self.time2[self.xPointer2],self.time2[self.plotIndex2])
            self.timer2.timeout.connect(self.update2)
            self.timer2.start(50)
        if len(self.fileNames) == 1 : 
            self.enableWidgets()
            #read 1 file
            csvFile1 = pd.read_csv(self.fileNames[0])
            # exctract data to draw signal 1 
            self.time1 = csvFile1.iloc[:,0].to_numpy()
            self.volts1 = csvFile1.iloc[:,1].to_numpy()
            self.sampleTime1 = self.time1[1] - self.time1[0]
            self.scrollStep1 = 10 * self.sampleTime1
            #plot spectogram
            self.drawSpectoForSignal1(self.signal4, self.volts1, 1 / self.sampleTime1)
            # plot the signal 
            self.plot1 = self.signal1.addPlot()
            self.plot1.plot(self.time1[self.xPointer1:self.plotIndex1],self.volts1[self.xPointer1:self.plotIndex1])
            self.plot1.setXRange(self.time1[self.xPointer1],self.time1[self.plotIndex1])
            self.timer1.timeout.connect(self.update1)
            self.timer1.start(50)

          

        
    def update1(self) :
        self.signal1.clear()
        self.xPointer1 += 1
        self.plotIndex1 += 1
        self.plot1 = self.signal1.addPlot()
        self.plot1.setXRange(self.time1[self.xPointer1],self.time1[self.plotIndex1])
        self.plot1.plot(self.time1[0:self.plotIndex1],self.volts1[0:self.plotIndex1])
    
    def update2(self) : 
        self.signal2.clear()
        self.xPointer2 += 1
        self.plotIndex2 += 1
        self.plot2 = self.signal2.addPlot()
        self.plot2.setXRange(self.time2[self.xPointer2],self.time2[self.plotIndex2])
        self.plot2.plot(self.time2[0:self.plotIndex2],self.volts2[0:self.plotIndex2])
    
    def update3(self) : 
        self.signal3.clear()
        self.xPointer3 += 1
        self.plotIndex3 += 1
        self.plot3 = self.signal3.addPlot()
        self.plot3.setXRange(self.time3[self.xPointer3],self.time3[self.plotIndex3])
        self.plot3.plot(self.time3[0:self.plotIndex3],self.volts3[0:self.plotIndex3])
        
    def generateReport(self) : 
        if self.fileNames != None : 
            if len(self.fileNames) == 3 : 
                fig, (ax1, ax2, ax3, ax4, ax5, ax6) = plt.subplots(6)
                fig.suptitle('Axes values are scaled individually by default')

                ax1.plot(self.time1, self.volts1, color="rEd")
                ax2.specgram(self.volts1,int(1 / self.sampleTime1))

                ax3.plot(self.time2, self.volts2, color="magenta")
                ax4.specgram(self.volts2, int(1 / self.sampleTime2))

                ax5.plot(self.time3, self.volts3, color="blue")
                ax6.specgram(self.volts3, int(1 / self.sampleTime3))

                fig.set_figheight(12)
                fig.set_figwidth(12)

                ax1.title.set_text('signal 1')
                ax2.title.set_text('spectogram for signal 1')
                ax3.title.set_text('signal 2')
                ax4.title.set_text('spectogram for signal 2')
                ax5.title.set_text('signal 3')
                ax6.title.set_text('spectogram for signal 3')

                ax1.set_xlabel('time (s)')
                ax3.set_xlabel('time (s)')
                ax5.set_xlabel('time (s)')
                ax1.set_ylabel('volts (v)')
                ax3.set_ylabel('volts (v)')
                ax5.set_ylabel('volts (v)')

                fig.tight_layout()
                R = list(range(0, 11))
                z = random.choice(R)

                fig.savefig(f"Report_{z}.pdf", bbox_inches='tight')
                window = QtWidgets.QMessageBox()
                window.setWindowTitle("done")
                window.setText("file has been saved as " + str(f"Report_{z}.pdf")+ " in your current directory")
                window.exec_()
            if len(self.fileNames) == 2 : 
                fig, (ax1, ax2, ax3, ax4) = plt.subplots(4)
                fig.suptitle('Axes values are scaled individually by default')

                ax1.plot(self.time1, self.volts1, color="rEd")
                ax2.specgram(self.volts1, int(1 / self.sampleTime1) )

                ax3.plot(self.time2, self.volts2, color="magenta")
                ax4.specgram(self.volts2, int(1 / self.sampleTime2))

                fig.set_figheight(12)
                fig.set_figwidth(12)

                ax1.title.set_text('signal 1')
                ax2.title.set_text('spectogram for signal 1')
                ax3.title.set_text('signal 2')
                ax4.title.set_text('spectogram for signal 2')

                ax1.set_xlabel('time (s)')
                ax3.set_xlabel('time (s)')
                ax1.set_ylabel('volts (v)')
                ax3.set_ylabel('volts (v)')

                fig.tight_layout()
                R = list(range(0, 11))
                z = random.choice(R)
                
                fig.savefig(f"Report_{z}.pdf", bbox_inches='tight')
                window = QtWidgets.QMessageBox()
                window.setWindowTitle("done")
                window.setText("file has been saved as report.pdf in your current directory")
                window.exec_()
            if len(self.fileNames) == 1 : 
                fig, (ax1, ax2) = plt.subplots(2)
                fig.suptitle('Axes values are scaled individually by default')

                ax1.plot(self.time1, self.volts1, color="rEd")
                ax2.specgram(self.volts1, int(1 / self.sampleTime1))

                fig.set_figheight(12)
                fig.set_figwidth(12)

                ax1.title.set_text('signal 1')
                ax2.title.set_text('spectogram for signal 1')

                ax1.set_xlabel('time (s)')
                ax1.set_ylabel('volts (v)')

                fig.tight_layout()
                R = list(range(0, 11))
                z = random.choice(R)
                
                fig.savefig(f"Report_{z}.pdf", bbox_inches='tight')
                window = QtWidgets.QMessageBox()
                window.setWindowTitle("done")
                window.setText("file has been saved as report.pdf in your current directory")
                window.exec_()
    

    def pause(self) :
        if self.selectedSignal == 0 : self.warnDialog("please choose signal")
        else : 
            timer = getattr(self, "timer" + str(self.selectedSignal)) # self.timer1
            if timer.isActive() : 
                timer.stop()
                ranges = getattr(getattr(self, "plot" + str(self.selectedSignal)), "viewRange")() # self.plot.viewRange()
                setattr(self, "xRangeOfSignal" + str(self.selectedSignal),ranges[0])
                setattr(self, "yRangeOfSignal" + str(self.selectedSignal),ranges[1])
                    

    def resume(self) : 
        if self.selectedSignal == 0 : self.warnDialog("please choose signal")
        else : 
            timer = getattr(self, "timer" + str(self.selectedSignal))
            if timer.isActive() == False : 
                timer.start()
        
        
    def warnDialog(self,message):
        window = QtWidgets.QMessageBox()
        window.setWindowTitle("error")
        window.setText(message)
        window.exec_()
    
    def signal1Clicked(self) : 
        self.selectedSignal = 1

    def signal2Clicked(self) :
        self.selectedSignal = 2
    
    def signal3Clicked(self) :
        self.selectedSignal = 3
        
    def zoom_in_h(self) :
        if self.selectedSignal == 0 : self.warnDialog("please Select signal")
        else : 
            timer = getattr(self, "timer" + str(self.selectedSignal))
            if timer.isActive() == False : 
                plot = getattr(self, "plot" + str(self.selectedSignal))
                if plot != None : 
                    xRangeOfSignal = getattr(self, "xRangeOfSignal" + str(self.selectedSignal))
                    getattr(getattr(self, "xRangeStack" + str(self.selectedSignal)), "append")([xRangeOfSignal[0],xRangeOfSignal[1]]) # self.xRangeStack1.append()
                    rangeOfX = getattr(self, "xRangeOfSignal" + str(self.selectedSignal))
                    rangeOfX[0] =  rangeOfX[0] * 0.8
                    rangeOfX[1] =  rangeOfX[1] * 0.8
                    getattr(getattr(self, "plot" + str(self.selectedSignal)), "setXRange")(rangeOfX[0],rangeOfX[1]) # self.plot1.setXRange()

    def zoom_out_h(self) :
        if self.selectedSignal == 0 : self.warnDialog("please Select signal")
        else :
            timer = getattr(self, "timer" + str(self.selectedSignal))
            if timer.isActive() == False : 
                plot = getattr(self, "plot" + str(self.selectedSignal))
                if plot != None : 
                    xRangeStack = getattr(self, "xRangeStack" + str(self.selectedSignal))
                    if len(xRangeStack) != 0 : 
                        rangeOfX = xRangeStack.pop()
                        getattr(getattr(self, "plot" + str(self.selectedSignal)), "setXRange")(rangeOfX[0],rangeOfX[1]) # self.plot1.setXRange()
                        setattr(self, "xRangeOfSignal" + str(self.selectedSignal), [rangeOfX[0],rangeOfX[1]])
    
    def zoom_in_v(self) : 
        if self.selectedSignal == 0 : self.warnDialog("please Select signal")
        else : 
            timer = getattr(self, "timer" + str(self.selectedSignal))
            if timer.isActive() == False : 
                plot = getattr(self, "plot" + str(self.selectedSignal))
                if plot != None : 
                    yRangeOfSignal = getattr(self, "yRangeOfSignal" + str(self.selectedSignal))
                    getattr(getattr(self, "yRangeStack" + str(self.selectedSignal)), "append")([yRangeOfSignal[0],yRangeOfSignal[1]]) # self.yRangeStack.append()
                    rangeOfY = getattr(self, "yRangeOfSignal" + str(self.selectedSignal))
                    rangeOfY[0] =  rangeOfY[0] * 0.8
                    rangeOfY[1] =  rangeOfY[1] * 0.8
                    getattr(getattr(self, "plot" + str(self.selectedSignal)), "setYRange")(rangeOfY[0],rangeOfY[1]) # self.plot1.setYRange()

    def zoom_out_v(self) :
        if self.selectedSignal == 0 : self.warnDialog("please Select signal")
        else :
            timer = getattr(self, "timer" + str(self.selectedSignal))
            if timer.isActive() == False : 
                plot = getattr(self, "plot" + str(self.selectedSignal))
                if plot != None : 
                    yRangeStack = getattr(self, "yRangeStack" + str(self.selectedSignal))
                    if len(yRangeStack) != 0 : 
                        rangeOfY = yRangeStack.pop()
                        getattr(getattr(self, "plot" + str(self.selectedSignal)), "setYRange")(rangeOfY[0],rangeOfY[1]) # self.plot1.setXRange()
                        setattr(self, "yRangeOfSignal" + str(self.selectedSignal), [rangeOfY[0],rangeOfY[1]])
    
    def scroll_up(self) :
        if self.selectedSignal == 0 : self.warnDialog("Please Select Signal")
        else : 
            timer = getattr(self, "timer" + str(self.selectedSignal))
            if timer.isActive() == False :
                plot = getattr(self, "plot" + str(self.selectedSignal))
                if plot != None : 
                    rangOfY = getattr(self, 'yRangeOfSignal' + str(self.selectedSignal))
                    rangOfY[0] += getattr(self, "scrollStep" + str(self.selectedSignal))
                    rangOfY[1] += getattr(self, "scrollStep" + str(self.selectedSignal))
                    getattr(getattr(self, "plot" + str(self.selectedSignal)), "setYRange")(rangOfY[0],rangOfY[1]) # self.plot1.setYRange()
    
    def scroll_down(self) : 
        if self.selectedSignal == 0 : self.warnDialog("Please Select Signal")
        else : 
            timer = getattr(self, "timer" + str(self.selectedSignal))
            if timer.isActive() == False :
                plot = getattr(self, "plot" + str(self.selectedSignal))
                if plot != None : 
                    rangOfY = getattr(self, 'yRangeOfSignal' + str(self.selectedSignal))
                    rangOfY[0] -= getattr(self, "scrollStep" + str(self.selectedSignal))
                    rangOfY[1] -= getattr(self, "scrollStep" + str(self.selectedSignal))
                    getattr(getattr(self, "plot" + str(self.selectedSignal)), "setYRange")(rangOfY[0],rangOfY[1]) # self.plot1.setYRange()

    def scroll_left(self) :
        if self.selectedSignal == 0 : self.warnDialog("Please Select Signal")
        else : 
            timer = getattr(self, "timer" + str(self.selectedSignal))
            if timer.isActive() == False : 
                plot = getattr(self, "plot" + str(self.selectedSignal))
                if plot != None : 
                    rangeOfX = getattr(self, 'xRangeOfSignal' + str(self.selectedSignal))
                    rangeOfX[0] -= getattr(self, "scrollStep" + str(self.selectedSignal))
                    rangeOfX[1] -= getattr(self, "scrollStep" + str(self.selectedSignal))
                    getattr(getattr(self, "plot" + str(self.selectedSignal)), "setXRange")(rangeOfX[0],rangeOfX[1]) # self.plot1.setXRange()

    def scroll_right(self) : 
        if self.selectedSignal == 0 : self.warnDialog("Please Select Signal")
        else : 
            timer = getattr(self, "timer" + str(self.selectedSignal))
            if timer.isActive() == False : 
                plot = getattr(self, "plot" + str(self.selectedSignal))
                if plot != None : 
                    rangeOfX = getattr(self, 'xRangeOfSignal' + str(self.selectedSignal))
                    rangeOfX[0] += getattr(self, "scrollStep" + str(self.selectedSignal))
                    rangeOfX[1] += getattr(self, "scrollStep" + str(self.selectedSignal))
                    getattr(getattr(self, "plot" + str(self.selectedSignal)), "setXRange")(rangeOfX[0],rangeOfX[1]) # self.plot1.setXRange()

    def drawSpectoForSignal1(self,GView,y,freq) : 
        
        f, t, Sxx = signal.spectrogram(y, freq)
        pyqtgraph.setConfigOptions(imageAxisOrder='row-major')

        win = GView
        p1 = win.addPlot()

        img = pyqtgraph.ImageItem()
        p1.addItem(img)
        hist = pyqtgraph.HistogramLUTItem()
        hist.setImageItem(img)
        win.addItem(hist)
        hist.setLevels(np.min(Sxx), np.max(Sxx))
        hist.gradient.restoreState({
            'mode':
            'rgb',
            'ticks': [(0.5, (0, 182, 188, 255)), (1.0, (246, 111, 0, 255)),
                      (0.0, (75, 0, 113, 255))]
        })
        img.setImage(Sxx)
        img.scale(t[-1] / np.size(Sxx, axis=1), f[-1] / np.size(Sxx, axis=0))
        p1.setLimits(xMin=0, xMax=t[-1], yMin=0, yMax=f[-1])
        p1.setLabel('bottom', "Time", units='s')
        p1.setLabel('left', "Frequency", units='Hz')

    def key_up(self,ev) : 
        self.scroll_up()
    
    def key_down(self,ev) : 
        self.scroll_down()
    def key_left(self,ev) : 
        self.scroll_left()
    def key_right(self,ev):
        self.scroll_right()	

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    SignalViewer = mainWindow()
    ui = Ui_SignalViewer()
    ui.setupUi(SignalViewer)
    SignalViewer.show()
    sys.exit(app.exec_())
