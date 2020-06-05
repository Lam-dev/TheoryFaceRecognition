# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'AddFace.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Frame_containAddFaceScreen(object):
    def setupUi(self, Frame_containAddFaceScreen):
        Frame_containAddFaceScreen.setObjectName("Frame_containAddFaceScreen")
        Frame_containAddFaceScreen.resize(801, 429)
        Frame_containAddFaceScreen.setFrameShape(QtWidgets.QFrame.StyledPanel)
        Frame_containAddFaceScreen.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame = QtWidgets.QFrame(Frame_containAddFaceScreen)
        self.frame.setGeometry(QtCore.QRect(8, 6, 785, 417))
        self.frame.setStyleSheet("background-color: rgb(191, 191, 191);\n"
"border-radius:7px")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.label_forShowCamera = QtWidgets.QLabel(self.frame)
        self.label_forShowCamera.setGeometry(QtCore.QRect(10, 10, 301, 401))
        self.label_forShowCamera.setText("")
        self.label_forShowCamera.setObjectName("label_forShowCamera")
        self.label_showGetFaceNotifyowGetFaceNotify = QtWidgets.QLabel(self.frame)
        self.label_showGetFaceNotifyowGetFaceNotify.setGeometry(QtCore.QRect(330, 210, 435, 121))
        self.label_showGetFaceNotifyowGetFaceNotify.setStyleSheet("color: rgb(198, 0, 0);\n"
"font: 75 bold 18pt \"Ubuntu\";")
        self.label_showGetFaceNotifyowGetFaceNotify.setText("")
        self.label_showGetFaceNotifyowGetFaceNotify.setAlignment(QtCore.Qt.AlignCenter)
        self.label_showGetFaceNotifyowGetFaceNotify.setWordWrap(True)
        self.label_showGetFaceNotifyowGetFaceNotify.setObjectName("label_showGetFaceNotifyowGetFaceNotify")
        self.label_forShowName = QtWidgets.QLabel(self.frame)
        self.label_forShowName.setGeometry(QtCore.QRect(340, 10, 421, 63))
        self.label_forShowName.setStyleSheet("color: rgb(0, 170, 127);\n"
"font: 75 bold 22pt \"Ubuntu\";")
        self.label_forShowName.setText("")
        self.label_forShowName.setAlignment(QtCore.Qt.AlignCenter)
        self.label_forShowName.setObjectName("label_forShowName")
        self.label_showIconNotifyowIconNotify = QtWidgets.QLabel(self.frame)
        self.label_showIconNotifyowIconNotify.setGeometry(QtCore.QRect(490, 90, 121, 111))
        self.label_showIconNotifyowIconNotify.setText("")
        self.label_showIconNotifyowIconNotify.setObjectName("label_showIconNotifyowIconNotify")

        self.retranslateUi(Frame_containAddFaceScreen)
        QtCore.QMetaObject.connectSlotsByName(Frame_containAddFaceScreen)

    def retranslateUi(self, Frame_containAddFaceScreen):
        _translate = QtCore.QCoreApplication.translate
        Frame_containAddFaceScreen.setWindowTitle(_translate("Frame_containAddFaceScreen", "Frame"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Frame_containAddFaceScreen = QtWidgets.QFrame()
    ui = Ui_Frame_containAddFaceScreen()
    ui.setupUi(Frame_containAddFaceScreen)
    Frame_containAddFaceScreen.show()
    sys.exit(app.exec_())
