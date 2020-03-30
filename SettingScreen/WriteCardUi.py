# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'GhiThe.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Frame(object):
    def setupUi(self, Frame):
        Frame.setObjectName("Frame")
        Frame.resize(493, 351)
        Frame.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"")
        Frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        Frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.label_forShowNameStudent = QtWidgets.QLabel(Frame)
        self.label_forShowNameStudent.setGeometry(QtCore.QRect(60, 0, 401, 41))
        self.label_forShowNameStudent.setStyleSheet("color: rgb(0, 85, 127);\n"
"font: 75 bold 16pt \"Ubuntu\";")
        self.label_forShowNameStudent.setText("")
        self.label_forShowNameStudent.setAlignment(QtCore.Qt.AlignCenter)
        self.label_forShowNameStudent.setObjectName("label_forShowNameStudent")
        self.label = QtWidgets.QLabel(Frame)
        self.label.setGeometry(QtCore.QRect(68, 50, 359, 199))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap("../../../icon/putRFcardIcon.png"))
        self.label.setObjectName("label")
        self.pushButton = QtWidgets.QPushButton(Frame)
        self.pushButton.setGeometry(QtCore.QRect(334, 266, 139, 73))
        self.pushButton.setStyleSheet("background-color: rgba(85, 255, 255, 70);\n"
"font: 75 bold 20pt \"Ubuntu\";\n"
"border-radius:5px;\n"
"border-color:rgb(33, 148, 255);\n"
"color: rgb(0, 0, 255);\n"
"border-width:1px;\n"
"border-style:solid;")
        self.pushButton.setObjectName("pushButton")
        self.label_showNotify = QtWidgets.QLabel(Frame)
        self.label_showNotify.setGeometry(QtCore.QRect(6, 280, 301, 49))
        self.label_showNotify.setStyleSheet("color: rgb(200, 0, 0);\n"
"font: 75 bold 16pt \"Ubuntu\";")
        self.label_showNotify.setAlignment(QtCore.Qt.AlignCenter)
        self.label_showNotify.setObjectName("label_showNotify")

        self.retranslateUi(Frame)
        QtCore.QMetaObject.connectSlotsByName(Frame)

    def retranslateUi(self, Frame):
        _translate = QtCore.QCoreApplication.translate
        Frame.setWindowTitle(_translate("Frame", "Frame"))
        self.pushButton.setText(_translate("Frame", "Ghi thẻ"))
        self.label_showNotify.setText(_translate("Frame", "ĐẶT THẺ LÊN THIẾT BỊ"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Frame = QtWidgets.QFrame()
    ui = Ui_Frame()
    ui.setupUi(Frame)
    Frame.show()
    sys.exit(app.exec_())

