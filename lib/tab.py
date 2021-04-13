from PyQt5 import QtCore, QtGui, QtWidgets

class newTab(QtWidgets.QTabWidget) : 
    def __init__ (self) :
        super(newTab, self).__init__()
    
    def add_new_viewer(self) : 
        centralwidget = QtWidgets.QWidget()
        self.addTab(centralwidget, "Tab 1")

# we are going to put all of our widgets inside the tab wrapped by a QWidget
class centralWidget(QtWidgets.QWidget) : 
    def __init__(self) :
        super(centralWidget,self).__init__()
