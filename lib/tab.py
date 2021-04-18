from PyQt5 import QtCore, QtGui, QtWidgets
from pyqtgraph import PlotWidget , GraphicsLayoutWidget
from scipy import signal
import pyqtgraph 
import numpy as np
from lib.FT import fourierTransform,soundfileUtility
import random

class newTab(QtWidgets.QTabWidget) : 
    def __init__ (self) :
        super(newTab, self).__init__()
        self.numberOfTabs = 0
    def add_new_viewer(self,timeData,voltsData) :
        self.numberOfTabs += 1
        centralwidget = centralWidget(timeData,voltsData)
        self.addTab(centralwidget, "new tab")
        self.setCurrentWidget(centralwidget)
        self.setCurrentIndex(self.numberOfTabs)
    def tabRemoved(self, index) : 
        self.numberOfTabs = self.numberOfTabs - 1

# we are going to put all of our widgets inside the tab wrapped by a QWidget
class centralWidget(QtWidgets.QWidget) :
    def __init__(self,timeData,voltsData) :
        super(centralWidget,self).__init__()
        # first generating the widgets of the tab
        self.generateUiWidgets()
        # initializing important variables for plotting
        self.timeData = timeData
        self.originalVoltsData = voltsData
        self.editedVoltsData   = voltsData
        self.plotIndex = 200
        self.xPointer  = 0
        self.plot = None # original Plot
        self.plot1 = None # plot After Editing

        self.xRangeStack = []
        self.yRangeStack = []

        self.sampleTime = timeData[1] - timeData[0]
        yrange = voltsData[len(voltsData) - 1] - voltsData[0]
        self.scrollStep_x = 100 * self.sampleTime
        self.scrollStep_y = yrange / 10
        
        self.timer = QtCore.QTimer()
        
        # sliders values 
        self._value1 = 1
        self._value2 = 1
        self._value3 = 1
        self._value4 = 1
        self._value5 = 1
        self._value6 = 1
        self._value7 = 1
        self._value8 = 1
        self._value9 = 1
        self._value10 = 1

        #Pallete of spectrogram *Pallete1 as deafult
        self.pallete_name = "viridis"
        self.RGB_Pallete_1 = (0.0, (68, 1, 84, 255))
        self.RGB_Pallete_2 = (0.25, (58, 82, 139, 255))
        self.RGB_Pallete_3 = (0.5, (32, 144, 140, 255))
        self.RGB_palette_4 = (0.75, (94, 201, 97, 255))
        self.RGB_palette_5 = (1.0, (253, 231, 36, 255))

        #set labels text
        ft = fourierTransform(self.originalVoltsData, int(1 / self.sampleTime))
        ranges = ft.rangesOfFrequancy 
        _translate = QtCore.QCoreApplication.translate
        self.label1.setText(_translate("MainWindow", str(ranges[0][0] / 1000 ) + " Khz : \n" + str(ranges[0][1] / 1000 ) + " Khz"))
        self.label2.setText(_translate("MainWindow", str(ranges[1][0] / 1000 ) + " Khz : \n" + str(ranges[1][1] / 1000 ) + " Khz"))
        self.label3.setText(_translate("MainWindow", str(ranges[2][0] / 1000 ) + " Khz : \n" + str(ranges[2][1] / 1000 ) + " Khz"))
        self.label4.setText(_translate("MainWindow", str(ranges[3][0] / 1000 ) + " Khz : \n" + str(ranges[3][1] / 1000 ) + " Khz"))
        self.label5.setText(_translate("MainWindow", str(ranges[4][0] / 1000 ) + " Khz : \n" + str(ranges[4][1] / 1000 ) + " Khz"))
        self.label6.setText(_translate("MainWindow", str(ranges[5][0] / 1000 ) + " Khz : \n" + str(ranges[5][1] / 1000 ) + " Khz"))
        self.label7.setText(_translate("MainWindow", str(ranges[6][0] / 1000 ) + " Khz : \n" + str(ranges[6][1] / 1000 ) + " Khz"))
        self.label8.setText(_translate("MainWindow", str(ranges[7][0] / 1000 ) + " Khz : \n" + str(ranges[7][1] / 1000 ) + " Khz"))
        self.label9.setText(_translate("MainWindow", str(ranges[8][0] / 1000 ) + " Khz : \n" + str(ranges[8][1] / 1000 ) + " Khz"))
        self.label10.setText(_translate("MainWindow", str(ranges[9][0] / 1000 ) + " Khz : \n" + str(ranges[9][1] / 1000 ) + " Khz"))
        self.HorizontalLabel1.setText(_translate("MainWindow", "Set Minimun Frequancy"))
        self.HorizontalLabel2.setText(_translate("MainWindow", "Set Maximum Frequancy"))

        #start plotting the data 
        self.startPlotting()
        # values of range of spectrogram
        self.minFreqOfSpectrogram = 0
        self.maxFreqOfSpectrogram = ranges[-1][1]

        self.horizontalSlider1.setMinimum(self.minFreqOfSpectrogram)
        self.horizontalSlider1.setMaximum(self.maxFreqOfSpectrogram)
        self.horizontalSlider1.setTickInterval(self.maxFreqOfSpectrogram / 10 )

        self.horizontalSlider2.setMinimum(self.minFreqOfSpectrogram)
        self.horizontalSlider2.setMaximum(self.maxFreqOfSpectrogram)
        self.horizontalSlider2.setSliderPosition(self.maxFreqOfSpectrogram)
        self.horizontalSlider2.setTickInterval(self.maxFreqOfSpectrogram / 10)

        self.SpectrogramViewer.clear()
        self.drawSpectrogram()
        self.xRangeOfSignal = self.plot.viewRange()[0] # [from , to] 
        self.yRangeOfSignal = self.plot.viewRange()[1]
 
    def startPlotting(self) :
        # plot original signal 
        # self.plot = self.OriginalSignalViewer.addPlot()
        # self.plot.plot(self.timeData[self.xPointer:self.plotIndex],self.originalVoltsData[self.xPointer:self.plotIndex])
        # self.plot.setXRange(self.timeData[self.xPointer],self.timeData[self.plotIndex])
        self.plot = self.OriginalSignalViewer.addPlot()
        self.plot.plot(self.timeData,self.originalVoltsData)
        # plot data After Editing
        # self.plot1 = self.EditedSignalViewer.addPlot()
        # self.plot1.plot(self.timeData[self.xPointer:self.plotIndex],self.editedVoltsData[self.xPointer:self.plotIndex])
        self.plot1 = self.EditedSignalViewer.addPlot()
        self.plot1.plot(self.timeData,self.editedVoltsData)
        # self.plot1.setXRange(self.timeData[self.xPointer],self.timeData[self.plotIndex])
        # self.timer.timeout.connect(self.update)
        # self.timer.start(50)
    
    def update(self) :
        self.OriginalSignalViewer.clear()
        self.EditedSignalViewer.clear()
        self.xPointer += 1
        self.plotIndex += 1
        # original data
        self.plot = self.OriginalSignalViewer.addPlot()
        self.plot.setXRange(self.timeData[self.xPointer],self.timeData[self.plotIndex])
        self.plot.plot(self.timeData[0:self.plotIndex],self.originalVoltsData[0:self.plotIndex])
        # edited data 
        self.plot1 = self.EditedSignalViewer.addPlot()
        self.plot1.setXRange(self.timeData[self.xPointer],self.timeData[self.plotIndex])
        self.plot1.plot(self.timeData[0:self.plotIndex],self.editedVoltsData[0:self.plotIndex])
    
    def minSliderOfSpectrogram(self,value) : 
        self.minFreqOfSpectrogram = value
        self.SpectrogramViewer.clear()
        self.drawSpectrogram()
    
    def maxSliderOfSpectrogram(self,value) : 
        self.maxFreqOfSpectrogram = value
        self.SpectrogramViewer.clear()
        self.drawSpectrogram()

    def drawSpectrogram(self,minFreq = 1,maxFreq = 1) :
        minFreq = self.minFreqOfSpectrogram
        maxFreq = self.maxFreqOfSpectrogram
        freq = 1 / self.sampleTime
        frequancyArr, timeArr, Sxx = signal.spectrogram(self.editedVoltsData, freq)
        pyqtgraph.setConfigOptions(imageAxisOrder='row-major')

        win = self.SpectrogramViewer
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
            'ticks': [self.RGB_Pallete_1, self.RGB_Pallete_2,
                       self.RGB_Pallete_3,self.RGB_palette_4,self.RGB_palette_5]
        })
        img.setImage(Sxx)
        img.scale(timeArr[-1] / np.size(Sxx, axis=1), frequancyArr[-1] / np.size(Sxx, axis=0))
        p1.setLimits(xMin=0, xMax=timeArr[-1], yMin=minFreq, yMax=maxFreq)
        p1.setLabel('bottom', "Time", units='s')
        p1.setLabel('left', "Frequency", units='Hz')

    def generateUiWidgets(self) :
        font = QtGui.QFont()
        font.setFamily("Arial Unicode MS")
        font.setPointSize(10)
        font.setBold(False)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(50)
        font.setStrikeOut(False)
        font.setKerning(True)
        self.setFont(font)
        self.setTabletTracking(False)
        self.gridLayout_6 = QtWidgets.QGridLayout(self)
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.gridLayout_4 = QtWidgets.QGridLayout()
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.SpectrogramGroupBox = QtWidgets.QGroupBox(self)
        font = QtGui.QFont()
        font.setFamily("Arial Unicode MS")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.SpectrogramGroupBox.setFont(font)
        self.SpectrogramGroupBox.setStyleSheet("border-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(0, 0, 0, 255), stop:1 rgba(255, 255, 255, 255));")
        self.SpectrogramGroupBox.setObjectName("SpectrogramGroupBox")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.SpectrogramGroupBox)
        self.gridLayout_2.setObjectName("gridLayout_2")

        self.horizontalSlider2 = QtWidgets.QSlider(self.SpectrogramGroupBox)
        font = QtGui.QFont()
        font.setPointSize(7)
        self.horizontalSlider2.setFont(font)
        self.horizontalSlider2.setCursor(QtGui.QCursor(QtCore.Qt.ClosedHandCursor))
        self.horizontalSlider2.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider2.setTickPosition(QtWidgets.QSlider.TicksBelow)
        self.horizontalSlider2.setTickInterval(1)
        self.horizontalSlider2.setObjectName("horizontalSlider2")
        self.gridLayout_2.addWidget(self.horizontalSlider2, 3, 0, 1, 1)

        self.SpectrogramViewer = GraphicsLayoutWidget(self.SpectrogramGroupBox)
        self.SpectrogramViewer.viewport().setProperty("cursor", QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.SpectrogramViewer.setStyleSheet("background-color:rgb(0,0,0)")
        self.SpectrogramViewer.setObjectName("SpectrogramViewer")
        self.gridLayout_2.addWidget(self.SpectrogramViewer, 0, 0, 1, 1)

        self.horizontalSlider1 = QtWidgets.QSlider(self.SpectrogramGroupBox)
        self.horizontalSlider1.setCursor(QtGui.QCursor(QtCore.Qt.ClosedHandCursor))
        self.horizontalSlider1.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider1.setTickPosition(QtWidgets.QSlider.TicksBelow)
        self.horizontalSlider1.setTickInterval(1)
        self.horizontalSlider1.setObjectName("horizontalSlider1")
        self.gridLayout_2.addWidget(self.horizontalSlider1, 1, 0, 1, 1)
        self.HorizontalLabel1 = QtWidgets.QLabel(self.SpectrogramGroupBox)
        font = QtGui.QFont()
        font.setPointSize(7)
        self.HorizontalLabel1.setFont(font)
        self.HorizontalLabel1.setAlignment(QtCore.Qt.AlignCenter)
        self.HorizontalLabel1.setObjectName("HorizontalLabel1")
        self.gridLayout_2.addWidget(self.HorizontalLabel1, 2, 0, 1, 1)
        self.HorizontalLabel2 = QtWidgets.QLabel(self.SpectrogramGroupBox)
        self.HorizontalLabel2.setAlignment(QtCore.Qt.AlignCenter)
        self.HorizontalLabel2.setObjectName("HorizontalLabel2")
        self.gridLayout_2.addWidget(self.HorizontalLabel2, 4, 0, 1, 1)

        self.gridLayout_4.addWidget(self.SpectrogramGroupBox, 0, 1, 3, 1)
        self.OriginalSignalGroupbox = QtWidgets.QGroupBox(self)
        font = QtGui.QFont()
        font.setFamily("Arial Unicode MS")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.OriginalSignalGroupbox.setFont(font)
        self.OriginalSignalGroupbox.setObjectName("OriginalSignalGroupbox")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.OriginalSignalGroupbox)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.OriginalSignalViewer = GraphicsLayoutWidget(self.OriginalSignalGroupbox)
        self.OriginalSignalViewer.viewport().setProperty("cursor", QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.OriginalSignalViewer.setStyleSheet("background-color: rgb(0, 0, 0);")
        self.OriginalSignalViewer.setObjectName("OriginalSignalViewer")
        self.gridLayout_5.addWidget(self.OriginalSignalViewer, 0, 0, 1, 1)
        self.gridLayout_4.addWidget(self.OriginalSignalGroupbox, 0, 0, 1, 1)
        self.EditedSignalGroupBox = QtWidgets.QGroupBox(self)
        font = QtGui.QFont()
        font.setFamily("Arial Unicode MS")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.EditedSignalGroupBox.setFont(font)
        self.EditedSignalGroupBox.setObjectName("EditedSignalGroupBox")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.EditedSignalGroupBox)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.EditedSignalViewer = GraphicsLayoutWidget(self.EditedSignalGroupBox)
        self.EditedSignalViewer.viewport().setProperty("cursor", QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.EditedSignalViewer.setStyleSheet("background-color:rgb(0,0,0)")
        self.EditedSignalViewer.setObjectName("EditedSignalViewer")
        self.gridLayout_3.addWidget(self.EditedSignalViewer, 0, 0, 1, 1)
        self.gridLayout_4.addWidget(self.EditedSignalGroupBox, 2, 0, 1, 1)
        self.SignalEditorGroupBox = QtWidgets.QGroupBox(self)
        font = QtGui.QFont()
        font.setFamily("Arial Unicode MS")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.SignalEditorGroupBox.setFont(font)
        self.SignalEditorGroupBox.setObjectName("SignalEditorGroupBox")
        self.gridLayout = QtWidgets.QGridLayout(self.SignalEditorGroupBox)
        self.gridLayout.setObjectName("gridLayout")
        self.gridLayout_7 = QtWidgets.QGridLayout()
        self.gridLayout_7.setObjectName("gridLayout_7")
        self.label1 = QtWidgets.QLabel(self.SignalEditorGroupBox)
        font = QtGui.QFont()
        font.setPointSize(5)
        font.setBold(False)
        font.setWeight(50)
        self.label1.setFont(font)
        self.label1.setObjectName("label1")
        self.gridLayout_7.addWidget(self.label1, 0, 0, 1, 1)
        self.label2 = QtWidgets.QLabel(self.SignalEditorGroupBox)
        font = QtGui.QFont()
        font.setPointSize(5)
        font.setBold(False)
        font.setWeight(50)
        self.label2.setFont(font)
        self.label2.setObjectName("label2")
        self.gridLayout_7.addWidget(self.label2, 0, 1, 1, 1)
        self.label3 = QtWidgets.QLabel(self.SignalEditorGroupBox)
        font = QtGui.QFont()
        font.setPointSize(5)
        font.setBold(False)
        font.setWeight(50)
        self.label3.setFont(font)
        self.label3.setObjectName("label3")
        self.gridLayout_7.addWidget(self.label3, 0, 2, 1, 1)
        self.label4 = QtWidgets.QLabel(self.SignalEditorGroupBox)
        font = QtGui.QFont()
        font.setPointSize(5)
        font.setBold(False)
        font.setWeight(50)
        self.label4.setFont(font)
        self.label4.setObjectName("label4")
        self.gridLayout_7.addWidget(self.label4, 0, 3, 1, 1)
        self.label5 = QtWidgets.QLabel(self.SignalEditorGroupBox)
        font = QtGui.QFont()
        font.setPointSize(5)
        font.setBold(False)
        font.setWeight(50)
        self.label5.setFont(font)
        self.label5.setObjectName("label5")
        self.gridLayout_7.addWidget(self.label5, 0, 4, 1, 1)
        self.label6 = QtWidgets.QLabel(self.SignalEditorGroupBox)
        font = QtGui.QFont()
        font.setPointSize(5)
        font.setBold(False)
        font.setWeight(50)
        self.label6.setFont(font)
        self.label6.setObjectName("label6")
        self.gridLayout_7.addWidget(self.label6, 0, 5, 1, 1)
        self.label7 = QtWidgets.QLabel(self.SignalEditorGroupBox)
        font = QtGui.QFont()
        font.setPointSize(5)
        font.setBold(False)
        font.setWeight(50)
        self.label7.setFont(font)
        self.label7.setObjectName("label7")
        self.gridLayout_7.addWidget(self.label7, 0, 6, 1, 1)
        self.label8 = QtWidgets.QLabel(self.SignalEditorGroupBox)
        font = QtGui.QFont()
        font.setPointSize(5)
        font.setBold(False)
        font.setWeight(50)
        self.label8.setFont(font)
        self.label8.setObjectName("label8")
        self.gridLayout_7.addWidget(self.label8, 0, 7, 1, 1)
        self.label9 = QtWidgets.QLabel(self.SignalEditorGroupBox)
        font = QtGui.QFont()
        font.setPointSize(5)
        font.setBold(False)
        font.setWeight(50)
        self.label9.setFont(font)
        self.label9.setObjectName("label9")
        self.gridLayout_7.addWidget(self.label9, 0, 8, 1, 1)
        self.label10 = QtWidgets.QLabel(self.SignalEditorGroupBox)
        font = QtGui.QFont()
        font.setPointSize(5)
        font.setBold(False)
        font.setWeight(50)
        self.label10.setFont(font)
        self.label10.setObjectName("label10")
        self.gridLayout_7.addWidget(self.label10, 0, 9, 1, 1)
        self.gridLayout.addLayout(self.gridLayout_7, 1, 0, 1, 10)
        self.Slider1 = QtWidgets.QSlider(self.SignalEditorGroupBox)
        self.Slider1.setCursor(QtGui.QCursor(QtCore.Qt.ClosedHandCursor))
        self.Slider1.setMinimum(0)
        self.Slider1.setMaximum(5)
        self.Slider1.setSliderPosition(1)
        self.Slider1.setOrientation(QtCore.Qt.Vertical)
        self.Slider1.setTickPosition(QtWidgets.QSlider.TicksAbove)
        self.Slider1.setTickInterval(1)
        self.Slider1.setObjectName("Slider1")
        self.gridLayout.addWidget(self.Slider1, 0, 0, 1, 1)
        self.Slider10 = QtWidgets.QSlider(self.SignalEditorGroupBox)
        self.Slider10.setCursor(QtGui.QCursor(QtCore.Qt.ClosedHandCursor))
        self.Slider10.setMinimum(0)
        self.Slider10.setMaximum(5)
        self.Slider10.setSliderPosition(1)
        self.Slider10.setOrientation(QtCore.Qt.Vertical)
        self.Slider10.setTickPosition(QtWidgets.QSlider.TicksAbove)
        self.Slider10.setTickInterval(1)
        self.Slider10.setObjectName("Slider10")
        self.gridLayout.addWidget(self.Slider10, 0, 9, 1, 1)
        self.Slide6 = QtWidgets.QSlider(self.SignalEditorGroupBox)
        self.Slide6.setCursor(QtGui.QCursor(QtCore.Qt.ClosedHandCursor))
        self.Slide6.setMinimum(0)
        self.Slide6.setMaximum(5)
        self.Slide6.setSliderPosition(1)
        self.Slide6.setOrientation(QtCore.Qt.Vertical)
        self.Slide6.setTickPosition(QtWidgets.QSlider.TicksAbove)
        self.Slide6.setTickInterval(1)
        self.Slide6.setObjectName("Slide6")
        self.gridLayout.addWidget(self.Slide6, 0, 5, 1, 1)
        self.Slider8 = QtWidgets.QSlider(self.SignalEditorGroupBox)
        self.Slider8.setCursor(QtGui.QCursor(QtCore.Qt.ClosedHandCursor))
        self.Slider8.setMinimum(0)
        self.Slider8.setMaximum(5)
        self.Slider8.setSliderPosition(1)
        self.Slider8.setOrientation(QtCore.Qt.Vertical)
        self.Slider8.setTickPosition(QtWidgets.QSlider.TicksAbove)
        self.Slider8.setTickInterval(1)
        self.Slider8.setObjectName("Slider8")
        self.gridLayout.addWidget(self.Slider8, 0, 7, 1, 1)
        self.Slider3 = QtWidgets.QSlider(self.SignalEditorGroupBox)
        self.Slider3.setCursor(QtGui.QCursor(QtCore.Qt.ClosedHandCursor))
        self.Slider3.setMinimum(0)
        self.Slider3.setMaximum(5)
        self.Slider3.setSliderPosition(1)
        self.Slider3.setOrientation(QtCore.Qt.Vertical)
        self.Slider3.setTickPosition(QtWidgets.QSlider.TicksAbove)
        self.Slider3.setTickInterval(1)
        self.Slider3.setObjectName("Slider3")
        self.gridLayout.addWidget(self.Slider3, 0, 2, 1, 1)
        self.Slider2 = QtWidgets.QSlider(self.SignalEditorGroupBox)
        self.Slider2.setCursor(QtGui.QCursor(QtCore.Qt.ClosedHandCursor))
        self.Slider2.setMinimum(0)
        self.Slider2.setMaximum(5)
        self.Slider2.setSliderPosition(1)
        self.Slider2.setOrientation(QtCore.Qt.Vertical)
        self.Slider2.setTickPosition(QtWidgets.QSlider.TicksAbove)
        self.Slider2.setTickInterval(1)
        self.Slider2.setObjectName("Slider2")
        self.gridLayout.addWidget(self.Slider2, 0, 1, 1, 1)
        self.Slider9 = QtWidgets.QSlider(self.SignalEditorGroupBox)
        self.Slider9.setCursor(QtGui.QCursor(QtCore.Qt.ClosedHandCursor))
        self.Slider9.setMinimum(0)
        self.Slider9.setMaximum(5)
        self.Slider9.setSliderPosition(1)
        self.Slider9.setOrientation(QtCore.Qt.Vertical)
        self.Slider9.setTickPosition(QtWidgets.QSlider.TicksAbove)
        self.Slider9.setTickInterval(1)
        self.Slider9.setObjectName("Slider9")
        self.gridLayout.addWidget(self.Slider9, 0, 8, 1, 1)
        self.Slider5 = QtWidgets.QSlider(self.SignalEditorGroupBox)
        self.Slider5.setCursor(QtGui.QCursor(QtCore.Qt.ClosedHandCursor))
        self.Slider5.setMinimum(0)
        self.Slider5.setMaximum(5)
        self.Slider5.setSliderPosition(1)
        self.Slider5.setOrientation(QtCore.Qt.Vertical)
        self.Slider5.setTickPosition(QtWidgets.QSlider.TicksAbove)
        self.Slider5.setTickInterval(1)
        self.Slider5.setObjectName("Slider5")
        self.gridLayout.addWidget(self.Slider5, 0, 4, 1, 1)
        self.Slider4 = QtWidgets.QSlider(self.SignalEditorGroupBox)
        self.Slider4.setCursor(QtGui.QCursor(QtCore.Qt.ClosedHandCursor))
        self.Slider4.setMinimum(0)
        self.Slider4.setMaximum(5)
        self.Slider4.setSliderPosition(1)    
        self.Slider4.setProperty("value", 1)
        self.Slider4.setOrientation(QtCore.Qt.Vertical)
        self.Slider4.setTickPosition(QtWidgets.QSlider.TicksAbove)
        self.Slider4.setTickInterval(1)
        self.Slider4.setObjectName("Slider4")
        self.gridLayout.addWidget(self.Slider4, 0, 3, 1, 1)
        self.Slider7 = QtWidgets.QSlider(self.SignalEditorGroupBox)
        self.Slider7.setCursor(QtGui.QCursor(QtCore.Qt.ClosedHandCursor))
        self.Slider7.setMinimum(0)
        self.Slider7.setMaximum(5)
        self.Slider7.setSliderPosition(1)
        self.Slider7.setOrientation(QtCore.Qt.Vertical)
        self.Slider7.setTickPosition(QtWidgets.QSlider.TicksAbove)
        self.Slider7.setTickInterval(1)
        self.Slider7.setObjectName("Slider7")
        self.gridLayout.addWidget(self.Slider7, 0, 6, 1, 1)
        self.gridLayout_4.addWidget(self.SignalEditorGroupBox, 1, 0, 1, 1)
        self.gridLayout_6.addLayout(self.gridLayout_4, 0, 0, 1, 1)
        ###########################################################################
        # Linkage is here
        ###########################################################################
        self.Slider1.valueChanged[int].connect(self.fn_slider1Value)
        self.Slider2.valueChanged[int].connect(self.fn_slider2Value)
        self.Slider3.valueChanged[int].connect(self.fn_slider3Value)
        self.Slider4.valueChanged[int].connect(self.fn_slider4Value)
        self.Slider5.valueChanged[int].connect(self.fn_slider5Value)
        self.Slide6.valueChanged[int].connect(self.fn_slider6Value)
        self.Slider7.valueChanged[int].connect(self.fn_slider7Value)
        self.Slider8.valueChanged[int].connect(self.fn_slider8Value)
        self.Slider9.valueChanged[int].connect(self.fn_slider9Value)
        self.Slider10.valueChanged[int].connect(self.fn_slider10Value)

        self.horizontalSlider1.valueChanged[int].connect(self.minSliderOfSpectrogram)
        self.horizontalSlider2.valueChanged[int].connect(self.maxSliderOfSpectrogram)

        QtCore.QMetaObject.connectSlotsByName(self)
        self.setTabOrder(self.Slider2, self.Slider3)
        self.setTabOrder(self.Slider3, self.Slider4)
        self.setTabOrder(self.Slider4, self.Slider5)
        self.setTabOrder(self.Slider5, self.Slide6)
        self.setTabOrder(self.Slide6, self.Slider7)
        self.setTabOrder(self.Slider7, self.Slider8)
        self.setTabOrder(self.Slider8, self.Slider9)
        self.setTabOrder(self.Slider9, self.Slider10)
        self.setTabOrder(self.Slider10, self.OriginalSignalViewer)
        self.setTabOrder(self.OriginalSignalViewer, self.EditedSignalViewer)
        self.setTabOrder(self.EditedSignalViewer, self.SpectrogramViewer)

    def fn_slider1Value(self, value1=1):
        self._value1 = value1
        self.process()

    def fn_slider2Value(self, value2=1):
        self._value2 = value2
        self.process()

    def fn_slider3Value(self, value3=1):
        self._value3 = value3
        self.process()

    def fn_slider4Value(self, value4=1):
        self._value4 = value4
        self.process()

    def fn_slider5Value(self, value5=1):
        self._value5 = value5
        self.process()
  
    def fn_slider6Value(self, value6=1):
        self._value6 = value6
        # print(self._value6)
        self.process()

    def fn_slider7Value(self, value7=1):
        self._value7 = value7
        self.process()

    def fn_slider8Value(self, value8=1):
        self._value8 = value8
        self.process()

    def fn_slider9Value(self, value9=1):
        self._value9 = value9
        self.process()
  
    def fn_slider10Value(self, value10=1):
        self._value10 = value10
        self.process()

    def process(self): #(freq,complex_data,reals,time,np.abs(complex_data))
        # if self.timer.isActive() : return
        ft = fourierTransform(list(self.originalVoltsData).copy(), 1 / self.sampleTime)
        complex_data = ft.gain(self._value1,self._value2,self._value3,self._value4,
        self._value5,self._value6,self._value7,self._value8,self._value9,self._value10)
        reals = ft.fn_InverceFourier(complex_data)
        # print(self._value1,self._value2,self._value3,self._value4,
        # self._value5,self._value6,self._value7,self._value8,self._value9,self._value10)
        #update Plot
        # self.EditedSignalViewer.clear()
        # self.plot1 = self.EditedSignalViewer.addPlot()
        # self.plot1.plot(self.timeData[0:self.plotIndex],reals[0:self.plotIndex])
        # self.plot1.setXRange(self.xRangeOfSignal[0],self.xRangeOfSignal[1])
        # self.editedVoltsData = np.array(reals)
        self.EditedSignalViewer.clear()
        self.plot1 = self.EditedSignalViewer.addPlot()
        self.plot1.plot(self.timeData,reals)
        self.plot1.setXRange(self.xRangeOfSignal[0],self.xRangeOfSignal[1])
        self.plot1.setYRange(self.yRangeOfSignal[0],self.yRangeOfSignal[1])
        self.editedVoltsData = np.array(reals)
        # update spectrogram 
        self.SpectrogramViewer.clear()
        self.drawSpectrogram()
    
    def playSound(self) : 
        ft = fourierTransform(list(self.originalVoltsData).copy(), 1 / self.sampleTime)
        complex_data = ft.gain(self._value1,self._value2,self._value3,self._value4,
        self._value5,self._value6,self._value7,self._value8,self._value9,self._value10)
        reals = ft.fn_InverceFourier(complex_data)
        sound = soundfileUtility()
        sound.fn_CreateSoundFile(list(reals),int(1 / self.sampleTime))
        sound.fn_PlaySoundFile()
        



