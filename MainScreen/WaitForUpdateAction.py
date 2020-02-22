from        MainScreen.WaitForUpdateUI    import Ui_Frame_ContainWaitForSync
from        PyQt5.QtCore    import pyqtSlot, pyqtSignal,QTimer, QDateTime,Qt, QObject
from        PyQt5.QtGui     import QPixmap
from        PyQt5           import QtWidgets, QtGui, QtCore
from        PIL             import Image, ImageQt

class MainScreen(QObject, Ui_Frame_ContainWaitForSync):

    def __init__(self, Frame):
        QObject.__init__(self)
        Ui_Frame_ContainWaitForSync.__init__(self)
        self.setupUi(Frame)
        Frame.setGeometry((800-Frame.width())/2, (480-Frame.height())/2, Frame.width(), Frame.height())
        self.label.setPixmap(QtGui.QPixmap("icon/iconReadFace.png"))
        

