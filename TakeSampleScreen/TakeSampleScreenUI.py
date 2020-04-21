# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ManHinhLayMau.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Frame(object):
    def setupUi(self, Frame):
        Frame.setObjectName("Frame")
        Frame.resize(800, 480)
        Frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        Frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_containLogoAndDeviceName = QtWidgets.QFrame(Frame)
        self.frame_containLogoAndDeviceName.setGeometry(QtCore.QRect(0, 0, 800, 50))
        self.frame_containLogoAndDeviceName.setStyleSheet("background-color: rgb(150, 220, 170);")
        self.frame_containLogoAndDeviceName.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_containLogoAndDeviceName.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_containLogoAndDeviceName.setObjectName("frame_containLogoAndDeviceName")
        self.pushButton_settingButton = QtWidgets.QPushButton(self.frame_containLogoAndDeviceName)
        self.pushButton_settingButton.setGeometry(QtCore.QRect(6, 0, 57, 49))
        self.pushButton_settingButton.setStyleSheet("border-style:solid;\n"
"border-radius:5px;")
        self.pushButton_settingButton.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("../../../../../../../.designer/icon/shutdown.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.pushButton_settingButton.setIcon(icon)
        self.pushButton_settingButton.setIconSize(QtCore.QSize(40, 40))
        self.pushButton_settingButton.setObjectName("pushButton_settingButton")
        self.label_deviceName = QtWidgets.QLabel(self.frame_containLogoAndDeviceName)
        self.label_deviceName.setGeometry(QtCore.QRect(76, 0, 583, 41))
        self.label_deviceName.setStyleSheet("color: rgb(160, 0, 0);\n"
"font: 75 bold 14pt \"Ubuntu\";")
        self.label_deviceName.setAlignment(QtCore.Qt.AlignCenter)
        self.label_deviceName.setObjectName("label_deviceName")
        self.pushButton_exitexit = QtWidgets.QPushButton(self.frame_containLogoAndDeviceName)
        self.pushButton_exitexit.setGeometry(QtCore.QRect(730, 0, 61, 51))
        self.pushButton_exitexit.setText("")
        self.pushButton_exitexit.setObjectName("pushButton_exitexit")

        self.retranslateUi(Frame)
        QtCore.QMetaObject.connectSlotsByName(Frame)

    def retranslateUi(self, Frame):
        _translate = QtCore.QCoreApplication.translate
        Frame.setWindowTitle(_translate("Frame", "Frame"))
        self.label_deviceName.setText(_translate("Frame", "LẤY MẪU VÂN TAY, KHUÔN MẶT, THẺ"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Frame = QtWidgets.QFrame()
    ui = Ui_Frame()
    ui.setupUi(Frame)
    Frame.show()
    sys.exit(app.exec_())
