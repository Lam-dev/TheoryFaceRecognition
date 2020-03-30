# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'WaitToSaveDialog.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(530, 303)
        Dialog.setStyleSheet("background-color: rgb(196, 200, 195);")
        self.label_forShowAddFaceResult = QtWidgets.QLabel(Dialog)
        self.label_forShowAddFaceResult.setGeometry(QtCore.QRect(90, 50, 431, 51))
        self.label_forShowAddFaceResult.setStyleSheet("\n"
"color: rgb(0, 85, 255);\n"
"font: 75 bold 14pt \"Ubuntu\";")
        self.label_forShowAddFaceResult.setText("")
        self.label_forShowAddFaceResult.setAlignment(QtCore.Qt.AlignCenter)
        self.label_forShowAddFaceResult.setWordWrap(True)
        self.label_forShowAddFaceResult.setObjectName("label_forShowAddFaceResult")
        self.pushButton_ok = QtWidgets.QPushButton(Dialog)
        self.pushButton_ok.setGeometry(QtCore.QRect(190, 240, 151, 61))
        self.pushButton_ok.setStyleSheet("border-radius:3px;\n"
"font: 75 bold 14pt \"Ubuntu\";\n"
"background-color: rgb(0, 170, 255);\n"
"color: rgb(255, 0, 0);")
        self.pushButton_ok.setObjectName("pushButton_ok")
        self.label_forShowAddFGPresult = QtWidgets.QLabel(Dialog)
        self.label_forShowAddFGPresult.setGeometry(QtCore.QRect(90, 110, 431, 51))
        self.label_forShowAddFGPresult.setStyleSheet("\n"
"color: rgb(0, 85, 255);\n"
"font: 75 bold 14pt \"Ubuntu\";")
        self.label_forShowAddFGPresult.setText("")
        self.label_forShowAddFGPresult.setAlignment(QtCore.Qt.AlignCenter)
        self.label_forShowAddFGPresult.setWordWrap(True)
        self.label_forShowAddFGPresult.setObjectName("label_forShowAddFGPresult")
        self.label_forShowAddCardResult = QtWidgets.QLabel(Dialog)
        self.label_forShowAddCardResult.setGeometry(QtCore.QRect(90, 170, 431, 51))
        self.label_forShowAddCardResult.setStyleSheet("\n"
"color: rgb(0, 85, 255);\n"
"font: 75 bold 14pt \"Ubuntu\";")
        self.label_forShowAddCardResult.setText("")
        self.label_forShowAddCardResult.setAlignment(QtCore.Qt.AlignCenter)
        self.label_forShowAddCardResult.setWordWrap(True)
        self.label_forShowAddCardResult.setObjectName("label_forShowAddCardResult")
        self.label_forShowNameStudent = QtWidgets.QLabel(Dialog)
        self.label_forShowNameStudent.setGeometry(QtCore.QRect(80, 0, 361, 51))
        self.label_forShowNameStudent.setStyleSheet("\n"
"color: rgb(0, 85, 255);\n"
"font: 75 bold 18pt \"Ubuntu\";")
        self.label_forShowNameStudent.setAlignment(QtCore.Qt.AlignCenter)
        self.label_forShowNameStudent.setWordWrap(True)
        self.label_forShowNameStudent.setObjectName("label_forShowNameStudent")
        self.label_forShowFaceIcon = QtWidgets.QLabel(Dialog)
        self.label_forShowFaceIcon.setGeometry(QtCore.QRect(10, 60, 51, 41))
        self.label_forShowFaceIcon.setText("")

        self.label_forShowFaceIcon.setObjectName("label_forShowFaceIcon")
        self.label_forShowFGPicon = QtWidgets.QLabel(Dialog)
        self.label_forShowFGPicon.setGeometry(QtCore.QRect(10, 120, 51, 41))
        self.label_forShowFGPicon.setText("")

        self.label_forShowFGPicon.setObjectName("label_forShowFGPicon")
        self.label_forShowCardIcon = QtWidgets.QLabel(Dialog)
        self.label_forShowCardIcon.setGeometry(QtCore.QRect(10, 180, 51, 41))
        self.label_forShowCardIcon.setText("")

        self.label_forShowCardIcon.setObjectName("label_forShowCardIcon")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.pushButton_ok.setText(_translate("Dialog", "OK"))
        self.label_forShowNameStudent.setText(_translate("Dialog", "TÊN HỌC VIÊN"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())

