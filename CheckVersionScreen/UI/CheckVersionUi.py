# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'CheckVersion.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Frame(object):
    def setupUi(self, Frame):
        Frame.setObjectName("Frame")
        Frame.resize(402, 243)
        Frame.setStyleSheet("background-color: rgb(199, 199, 199);")
        Frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        Frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frameNotNewVersion = QtWidgets.QFrame(Frame)
        self.frameNotNewVersion.setGeometry(QtCore.QRect(0, 0, 400, 250))
        self.frameNotNewVersion.setStyleSheet("border-style: solid;\n"
"border-width:0px;")
        self.frameNotNewVersion.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frameNotNewVersion.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frameNotNewVersion.setObjectName("frameNotNewVersion")
        self.label_7 = QtWidgets.QLabel(self.frameNotNewVersion)
        self.label_7.setGeometry(QtCore.QRect(20, 48, 355, 47))
        self.label_7.setStyleSheet("color: rgb(85, 170, 0);\n"
"font: 75 bold 18pt \"Ubuntu\";")
        self.label_7.setAlignment(QtCore.Qt.AlignCenter)
        self.label_7.setObjectName("label_7")
        self.pushButton = QtWidgets.QPushButton(self.frameNotNewVersion)
        self.pushButton.setGeometry(QtCore.QRect(130, 142, 129, 59))
        self.pushButton.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.pushButton.setObjectName("pushButton")
        self.frame_containConnectingNotify = QtWidgets.QFrame(Frame)
        self.frame_containConnectingNotify.setGeometry(QtCore.QRect(0, 0, 400, 250))
        self.frame_containConnectingNotify.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_containConnectingNotify.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_containConnectingNotify.setObjectName("frame_containConnectingNotify")
        self.label_iconConnecting = QtWidgets.QLabel(self.frame_containConnectingNotify)
        self.label_iconConnecting.setGeometry(QtCore.QRect(12, 60, 53, 51))
        self.label_iconConnecting.setText("")
        self.label_iconConnecting.setPixmap(QtGui.QPixmap("../icon/connectIcon50.png"))
        self.label_iconConnecting.setObjectName("label_iconConnecting")
        self.label_6 = QtWidgets.QLabel(self.frame_containConnectingNotify)
        self.label_6.setGeometry(QtCore.QRect(70, 58, 291, 51))
        self.label_6.setStyleSheet("color: rgb(85, 170, 0);\n"
"font: 75 bold 14pt \"Ubuntu\";")
        self.label_6.setAlignment(QtCore.Qt.AlignCenter)
        self.label_6.setObjectName("label_6")
        self.pushButton_cancelCheck = QtWidgets.QPushButton(self.frame_containConnectingNotify)
        self.pushButton_cancelCheck.setGeometry(QtCore.QRect(154, 146, 105, 47))
        self.pushButton_cancelCheck.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.pushButton_cancelCheck.setObjectName("pushButton_cancelCheck")
        self.frameDetectNewVersion = QtWidgets.QFrame(Frame)
        self.frameDetectNewVersion.setGeometry(QtCore.QRect(0, 0, 400, 250))
        self.frameDetectNewVersion.setStyleSheet("border-style: solid;\n"
"border-width:0px;")
        self.frameDetectNewVersion.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frameDetectNewVersion.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frameDetectNewVersion.setObjectName("frameDetectNewVersion")
        self.label_3 = QtWidgets.QLabel(self.frameDetectNewVersion)
        self.label_3.setGeometry(QtCore.QRect(18, 14, 355, 47))
        self.label_3.setStyleSheet("color: rgb(85, 170, 0);\n"
"font: 75 bold 18pt \"Ubuntu\";")
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.pushButton_update = QtWidgets.QPushButton(self.frameDetectNewVersion)
        self.pushButton_update.setGeometry(QtCore.QRect(48, 144, 125, 51))
        self.pushButton_update.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.pushButton_update.setObjectName("pushButton_update")
        self.pushButton_cancelUpdated = QtWidgets.QPushButton(self.frameDetectNewVersion)
        self.pushButton_cancelUpdated.setGeometry(QtCore.QRect(228, 144, 127, 51))
        self.pushButton_cancelUpdated.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.pushButton_cancelUpdated.setObjectName("pushButton_cancelUpdated")
        self.label_forShowNewVersion = QtWidgets.QLabel(self.frameDetectNewVersion)
        self.label_forShowNewVersion.setGeometry(QtCore.QRect(78, 66, 233, 45))
        self.label_forShowNewVersion.setStyleSheet("color: rgb(85, 170, 0);\n"
"font: 75 bold 18pt \"Ubuntu\";")
        self.label_forShowNewVersion.setAlignment(QtCore.Qt.AlignCenter)
        self.label_forShowNewVersion.setObjectName("label_forShowNewVersion")
        self.frame_containConnectingNotify.raise_()
        self.frameDetectNewVersion.raise_()
        self.frameNotNewVersion.raise_()

        self.retranslateUi(Frame)
        QtCore.QMetaObject.connectSlotsByName(Frame)

    def retranslateUi(self, Frame):
        _translate = QtCore.QCoreApplication.translate
        Frame.setWindowTitle(_translate("Frame", "Frame"))
        self.label_7.setText(_translate("Frame", "Không có phiên bản mới"))
        self.pushButton.setText(_translate("Frame", "Đóng"))
        self.label_6.setText(_translate("Frame", "ĐANG KẾT NỐI MÁY CHỦ..."))
        self.pushButton_cancelCheck.setText(_translate("Frame", "Dừng"))
        self.label_3.setText(_translate("Frame", "ĐÃ CÓ PHIÊN BẢN MỚI"))
        self.pushButton_update.setText(_translate("Frame", "Cập nhật"))
        self.pushButton_cancelUpdated.setText(_translate("Frame", "Hủy"))
        self.label_forShowNewVersion.setText(_translate("Frame", "v1.0.1"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Frame = QtWidgets.QFrame()
    ui = Ui_Frame()
    ui.setupUi(Frame)
    Frame.show()
    sys.exit(app.exec_())
