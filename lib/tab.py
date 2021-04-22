from PyQt5 import QtCore, QtGui, QtWidgets
from pyqtgraph import PlotWidget , GraphicsLayoutWidget
from scipy import signal
import pyqtgraph 
import numpy as np
from lib.FT import fourierTransform,soundfileUtility
import random

class Tabs(QtWidgets.QTabWidget) : 
    def __init__ (self) :
        super(Tabs, self).__init__()
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
        self.plot = None # original Plot
        self.plot1 = None # plot After Editing

        self.xRangeStack = []
        self.yRangeStack = []

        self.sampleTime = timeData[1] - timeData[0]
        yrange = voltsData[len(voltsData) - 1] - voltsData[0]
        self.scrollStep_x = 100 * self.sampleTime
        self.scrollStep_y = yrange / 10
        
        
        # sliders values 
        for i in range(1,11) : 
            setattr(self, "_value"+str(i), 1) # self._value[1-10] = 1

        #Pallete of spectrogram *viridis as deafult
        self.RGB_Pallete_1 = (0, 182, 188, 255)
        self.RGB_Pallete_2 = (246, 111, 0, 255)
        self.RGB_Pallete_3 = (75, 0, 113, 255)

        #set labels text
        ft = fourierTransform(self.originalVoltsData, int(1 / self.sampleTime))
        ranges = ft.rangesOfFrequancy

        for i in range(10) : 
            getattr(getattr(self,"label"+str(i+1)),"setText")(str(ranges[i][0] / 1000 ) + " Khz : \n" + str(ranges[i][1] / 1000 ) + " Khz")

        self.HorizontalLabel1.setText("Set Minimun Frequancy")
        self.HorizontalLabel2.setText("Set Maximum Frequancy")

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
        self.plot = self.OriginalSignalViewer.addPlot()
        self.plot.plot(self.timeData,self.originalVoltsData)
        # plot data After Editing
        self.plot1 = self.EditedSignalViewer.addPlot()
        self.plot1.plot(self.timeData,self.editedVoltsData)
    
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
            'ticks': [(0.5, self.RGB_Pallete_1), (1.0, self.RGB_Pallete_2),
                      (0.0, self.RGB_Pallete_3)]
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

        # add 10 labels for 10 sliders
        for i in range(10) :
            setattr(self, "label" + str(i+1), QtWidgets.QLabel(self.SignalEditorGroupBox)) # self.label[1-10] = QtWidgets.QLabel(self.SignalEditorGroupBox)
            font = QtGui.QFont()
            font.setPointSize(5)
            font.setBold(False)
            font.setWeight(50)
            getattr(getattr(self,"label" + str(i + 1)),"setFont")(font) #self.label1.setFont(font)
            getattr(getattr(self,"label" + str(i + 1)),"setObjectName")("label"+str(i+1)) #self.label[1-10].setObjectName("label[1-10]")
            getattr(getattr(self,"gridLayout_7"),"addWidget")(getattr(self, "label" + str(i + 1)), 0, i, 1, 1) #self.gridLayout_7.addWidget(self.label1, 0, 0, 1, 1)

        self.gridLayout.addLayout(self.gridLayout_7, 1, 0, 1, 10)

        # add 10 sliders to gui 
        for i in range(10) : 
            setattr(self, "Slider"+str(i+1), QtWidgets.QSlider(self.SignalEditorGroupBox))
            Slider = getattr(self, "Slider" + str(i + 1))
            Slider.setCursor(QtGui.QCursor(QtCore.Qt.ClosedHandCursor))
            Slider.setMinimum(0)
            Slider.setMaximum(5)
            Slider.setSliderPosition(1)
            Slider.setOrientation(QtCore.Qt.Vertical)
            Slider.setTickPosition(QtWidgets.QSlider.TicksAbove)
            Slider.setTickInterval(1)
            Slider.setObjectName("Slider" + str(i + 1))
            getattr(getattr(self,"gridLayout"), "addWidget")(Slider, 0, i, 1, 1)

        self.gridLayout_4.addWidget(self.SignalEditorGroupBox, 1, 0, 1, 1)
        self.gridLayout_6.addLayout(self.gridLayout_4, 0, 0, 1, 1)
        ###########################################################################
        # Linkage is here
        ###########################################################################
        for i in range(1,11) : 
            getattr(getattr(getattr(self,"Slider" + str(i)),"valueChanged")[int], "connect")(getattr(self, "fn_slider"+str(i)+"Value"))

        self.horizontalSlider1.valueChanged[int].connect(self.minSliderOfSpectrogram)
        self.horizontalSlider2.valueChanged[int].connect(self.maxSliderOfSpectrogram)

        QtCore.QMetaObject.connectSlotsByName(self)
        # self.setTabOrder(self.Slider2, self.Slider3)
        # self.setTabOrder(self.Slider3, self.Slider4)
        # self.setTabOrder(self.Slider4, self.Slider5)
        # self.setTabOrder(self.Slider5, self.Slider6)
        # self.setTabOrder(self.Slider6, self.Slider7)
        # self.setTabOrder(self.Slider7, self.Slider8)
        # self.setTabOrder(self.Slider8, self.Slider9)
        # self.setTabOrder(self.Slider9, self.Slider10)
        # self.setTabOrder(self.Slider10, self.OriginalSignalViewer)
        # self.setTabOrder(self.OriginalSignalViewer, self.EditedSignalViewer)
        # self.setTabOrder(self.EditedSignalViewer, self.SpectrogramViewer)

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
        ft = fourierTransform(list(self.originalVoltsData).copy(), 1 / self.sampleTime)
        complex_data = ft.gain(self._value1,self._value2,self._value3,self._value4,
        self._value5,self._value6,self._value7,self._value8,self._value9,self._value10)
        reals = ft.fn_InverceFourier(complex_data)
        #update Plot
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
        ft = fourierTransform(list(self.editedVoltsData).copy(), 1 / self.sampleTime)
        complex_data = ft.gain(self._value1,self._value2,self._value3,self._value4,
        self._value5,self._value6,self._value7,self._value8,self._value9,self._value10)
        reals = ft.fn_InverceFourier(complex_data)
        sound = soundfileUtility()
        sound.fn_CreateSoundFile(list(reals),int(1 / self.sampleTime))
        sound.fn_PlaySoundFile()
        



