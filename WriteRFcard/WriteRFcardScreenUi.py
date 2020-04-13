# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'WriteIDcardScreen.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Frame_containWriteIDcardScreen(object):
    def setupUi(self, Frame_containWriteIDcardScreen):
        Frame_containWriteIDcardScreen.setObjectName("Frame_containWriteIDcardScreen")
        Frame_containWriteIDcardScreen.resize(800, 429)
        Frame_containWriteIDcardScreen.setFrameShape(QtWidgets.QFrame.StyledPanel)
        Frame_containWriteIDcardScreen.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame = QtWidgets.QFrame(Frame_containWriteIDcardScreen)
        self.frame.setGeometry(QtCore.QRect(8, 6, 785, 417))
        self.frame.setStyleSheet("background-color: rgb(191, 191, 191);\n"
"border-radius:7px")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.label = QtWidgets.QLabel(self.frame)
        self.label.setGeometry(QtCore.QRect(172, 84, 449, 263))
        self.label.setText("")
        
        self.label.setObjectName("label")
        self.label_showNotify = QtWidgets.QLabel(self.frame)
        self.label_showNotify.setGeometry(QtCore.QRect(22, 362, 753, 53))
        self.label_showNotify.setStyleSheet("font: 57 bold 28pt \"Ubuntu\";\n"
"color: rgb(193, 0, 0);")
        self.label_showNotify.setAlignment(QtCore.Qt.AlignCenter)
        self.label_showNotify.setObjectName("label_showNotify")
        self.label_forShowName = QtWidgets.QLabel(self.frame)
        self.label_forShowName.setGeometry(QtCore.QRect(136, 8, 521, 63))
        self.label_forShowName.setStyleSheet("color: rgb(0, 170, 127);\n"
"font: 75 bold 22pt \"Ubuntu\";")
        self.label_forShowName.setText("")
        self.label_forShowName.setAlignment(QtCore.Qt.AlignCenter)
        self.label_forShowName.setObjectName("label_forShowName")

        self.retranslateUi(Frame_containWriteIDcardScreen)
        QtCore.QMetaObject.connectSlotsByName(Frame_containWriteIDcardScreen)

    def retranslateUi(self, Frame_containWriteIDcardScreen):
        _translate = QtCore.QCoreApplication.translate
        Frame_containWriteIDcardScreen.setWindowTitle(_translate("Frame_containWriteIDcardScreen", "Frame"))
        self.label_showNotify.setText(_translate("Frame_containWriteIDcardScreen", "Vui lòng đặt thẻ lên cảm biến"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Frame_containWriteIDcardScreen = QtWidgets.QFrame()
    ui = Ui_Frame_containWriteIDcardScreen()
    ui.setupUi(Frame_containWriteIDcardScreen)
    Frame_containWriteIDcardScreen.show()
    sys.exit(app.exec_())
