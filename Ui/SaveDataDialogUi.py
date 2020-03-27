# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'SaveDataDialog.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(386, 213)
        Dialog.setStyleSheet("background-color: rgb(216, 216, 216);")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(6, 14, 365, 101))
        self.label.setStyleSheet("\n"
"color: rgb(0, 85, 255);\n"
"font: 75 bold 14pt \"Ubuntu\";")
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setWordWrap(True)
        self.label.setObjectName("label")
        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(58, 148, 111, 45))
        self.pushButton.setStyleSheet("border-radius:3px;\n"
"font: 75 bold 14pt \"Ubuntu\";\n"
"background-color: rgb(0, 170, 255);\n"
"color: rgb(255, 0, 0);")
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(Dialog)
        self.pushButton_2.setGeometry(QtCore.QRect(234, 148, 105, 47))
        self.pushButton_2.setStyleSheet("border-radius:3px;\n"
"font: 75 bold 14pt \"Ubuntu\";\n"
"background-color: rgb(0, 170, 255);\n"
"color: rgb(0, 170, 0);")
        self.pushButton_2.setObjectName("pushButton_2")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label.setText(_translate("Dialog", "Lưu "))
        self.pushButton.setText(_translate("Dialog", "Hủy"))
        self.pushButton_2.setText(_translate("Dialog", "Lưu"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
