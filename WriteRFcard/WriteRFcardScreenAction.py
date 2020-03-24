from WriteRFcard.WriteRFcardScreenUi   import Ui_Frame_containWriteIDcardScreen
from PyQt5          import QtCore, QtGui
from PyQt5.QtCore   import pyqtSlot, pyqtSignal,QTimer, QDateTime, Qt, QObject, QPointF, QPropertyAnimation, pyqtProperty, QSize
from PyQt5          import QtWidgets
import json

class WriteRFcardAction(QObject, Ui_Frame_containWriteIDcardScreen):
    
    def __init__(self):
        QObject.__init__(self)
        Ui_Frame_containWriteIDcardScreen.__init__(self)
    
    
    
