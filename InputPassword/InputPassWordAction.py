from        InputPassword.InputPassWordUi  import Ui_Frame
from        PyQt5.QtCore    import pyqtSlot, pyqtSignal,QTimer, QDateTime,Qt, QObject
from        PyQt5.QtGui     import QPixmap
from        PyQt5           import QtWidgets, QtGui, QtCore
from        PIL             import Image, ImageQt
import      threading

class InputPassword(QObject, Ui_Frame):
    SignalRecognizedStudent = pyqtSignal(int)
    SignalCloseInputPassword = pyqtSignal()
    def __init__(self, Frame):
        QObject.__init__(self)
        Ui_Frame.__init__(self)
        self.setupUi(Frame)
        self.frame = Frame
        Frame.setGeometry((800-Frame.width())/2, (480-Frame.height())/2, Frame.width(), Frame.height())
        self.currentNumber = ""
        self.pushButton_0.clicked.connect(lambda:self.ButtonClick(0))
        self.pushButton_1.clicked.connect(lambda:self.ButtonClick(1))
        self.pushButton_2.clicked.connect(lambda:self.ButtonClick(2))
        self.pushButton_3.clicked.connect(lambda:self.ButtonClick(3))
        self.pushButton_4.clicked.connect(lambda:self.ButtonClick(4))
        self.pushButton_5.clicked.connect(lambda:self.ButtonClick(5))
        self.pushButton_6.clicked.connect(lambda:self.ButtonClick(6))
        self.pushButton_7.clicked.connect(lambda:self.ButtonClick(7))
        self.pushButton_8.clicked.connect(lambda:self.ButtonClick(8))
        self.pushButton_9.clicked.connect(lambda:self.ButtonClick(9))
        self.pushButton_OK.clicked.connect(lambda:self.ButtonControlClick(True))
        self.pushButton_del.clicked.connect(lambda:self.ButtonControlClick(False))
        self.lstStudent = []

    def CloseScreen(self):
        self.frame.hide()


    def ButtonClick(self, number):
        if(len(self.currentNumber) >= 6):
            return

        self.currentNumber += str(number)
        self.label_forShowNumber.setText(self.currentNumber)
        self.ThreadFindStudent()
    
    def ButtonControlClick(self, buttonOK):
        if(buttonOK):
            self.SignalCloseInputPassword.emit()
        else:
            if(self.currentNumber.__len__() >= 1):
                self.currentNumber = self.currentNumber[0:self.currentNumber.__len__()-1]
                self.label_forShowNumber.setText(self.currentNumber)
        
    def ThreadFindStudent(self):
        thread = threading.Thread(target = self.SearchStudent, args=(), daemon= True)
        thread.start()

    def SearchStudent(self):
        for student in self.lstStudent:
            if(str(student.ID) == self.currentNumber):
                self.SignalRecognizedStudent.emit(student.ID)