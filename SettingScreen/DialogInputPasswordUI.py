# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'NhapMatKhauChoAccount.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Frame_forInputPassword(object):
    def setupUi(self, Frame_forInputPassword):
        Frame_forInputPassword.setObjectName("Frame_forInputPassword")
        Frame_forInputPassword.resize(347, 212)
        Frame_forInputPassword.setStyleSheet("background-color: rgb(234, 234, 234);")
        Frame_forInputPassword.setFrameShape(QtWidgets.QFrame.StyledPanel)
        Frame_forInputPassword.setFrameShadow(QtWidgets.QFrame.Raised)
        self.lineEdit_forInputPassword = QtWidgets.QLineEdit(Frame_forInputPassword)
        self.lineEdit_forInputPassword.setGeometry(QtCore.QRect(36, 68, 279, 53))
        self.lineEdit_forInputPassword.setObjectName("lineEdit_forInputPassword")
        self.label_forShowNameAccount = QtWidgets.QLabel(Frame_forInputPassword)
        self.label_forShowNameAccount.setGeometry(QtCore.QRect(16, 8, 301, 53))
        self.label_forShowNameAccount.setStyleSheet("font: 75 12pt \"Ubuntu\";")
        self.label_forShowNameAccount.setText("")
        self.label_forShowNameAccount.setAlignment(QtCore.Qt.AlignCenter)
        self.label_forShowNameAccount.setWordWrap(True)
        self.label_forShowNameAccount.setObjectName("label_forShowNameAccount")
        self.pushButton_ok = QtWidgets.QPushButton(Frame_forInputPassword)
        self.pushButton_ok.setGeometry(QtCore.QRect(52, 134, 109, 51))
        self.pushButton_ok.setObjectName("pushButton_ok")
        self.pushButton_exit = QtWidgets.QPushButton(Frame_forInputPassword)
        self.pushButton_exit.setGeometry(QtCore.QRect(188, 134, 109, 51))
        self.pushButton_exit.setObjectName("pushButton_exit")

        self.retranslateUi(Frame_forInputPassword)
        QtCore.QMetaObject.connectSlotsByName(Frame_forInputPassword)

    def retranslateUi(self, Frame_forInputPassword):
        _translate = QtCore.QCoreApplication.translate
        Frame_forInputPassword.setWindowTitle(_translate("Frame_forInputPassword", "Frame"))
        self.pushButton_ok.setText(_translate("Frame_forInputPassword", "Kiểm tra"))
        self.pushButton_exit.setText(_translate("Frame_forInputPassword", "Hủy"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Frame_forInputPassword = QtWidgets.QFrame()
    ui = Ui_Frame_forInputPassword()
    ui.setupUi(Frame_forInputPassword)
    Frame_forInputPassword.show()
    sys.exit(app.exec_())
