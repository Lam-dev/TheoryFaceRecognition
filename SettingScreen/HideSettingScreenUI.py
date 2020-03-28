# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'HideSettingScreen.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Frame_containHideSettingScreen(object):
    def setupUi(self, Frame_containHideSettingScreen):
        Frame_containHideSettingScreen.setObjectName("Frame_containHideSettingScreen")
        Frame_containHideSettingScreen.resize(800, 480)
        Frame_containHideSettingScreen.setStyleSheet("background-color: rgb(170, 170, 255);")
        Frame_containHideSettingScreen.setFrameShape(QtWidgets.QFrame.StyledPanel)
        Frame_containHideSettingScreen.setFrameShadow(QtWidgets.QFrame.Raised)
        self.groupBox = QtWidgets.QGroupBox(Frame_containHideSettingScreen)
        self.groupBox.setGeometry(QtCore.QRect(0, 2, 239, 475))
        self.groupBox.setStyleSheet("background-color: rgb(0, 147, 220);")
        self.groupBox.setObjectName("groupBox")
        self.pushButton_addNewAccount = QtWidgets.QPushButton(self.groupBox)
        self.pushButton_addNewAccount.setGeometry(QtCore.QRect(48, 392, 129, 71))
        self.pushButton_addNewAccount.setObjectName("pushButton_addNewAccount")
        self.listWidget_showListAdminAccount = QtWidgets.QListWidget(self.groupBox)
        self.listWidget_showListAdminAccount.setGeometry(QtCore.QRect(4, 40, 229, 333))
        self.listWidget_showListAdminAccount.setObjectName("listWidget_showListAdminAccount")
        self.groupBox_2 = QtWidgets.QGroupBox(Frame_containHideSettingScreen)
        self.groupBox_2.setGeometry(QtCore.QRect(244, 4, 553, 469))
        self.groupBox_2.setObjectName("groupBox_2")
        self.listWidget_forShowListStudent = QtWidgets.QListWidget(self.groupBox_2)
        self.listWidget_forShowListStudent.setGeometry(QtCore.QRect(2, 58, 459, 411))
        self.listWidget_forShowListStudent.setObjectName("listWidget_forShowListStudent")
        self.label_iconSearch = QtWidgets.QLabel(self.groupBox_2)
        self.label_iconSearch.setGeometry(QtCore.QRect(166, 8, 47, 41))
        self.label_iconSearch.setText("")
        self.label_iconSearch.setPixmap(QtGui.QPixmap("../../icon/iconSearch.png"))
        self.label_iconSearch.setObjectName("label_iconSearch")
        self.lineEdit_inputTextToSearch = QtWidgets.QLineEdit(self.groupBox_2)
        self.lineEdit_inputTextToSearch.setGeometry(QtCore.QRect(220, 6, 241, 43))
        self.lineEdit_inputTextToSearch.setObjectName("lineEdit_inputTextToSearch")
        self.pushButton_selectAll = QtWidgets.QPushButton(self.groupBox_2)
        self.pushButton_selectAll.setGeometry(QtCore.QRect(468, 180, 79, 73))
        self.pushButton_selectAll.setObjectName("pushButton_selectAll")
        self.pushButton_removeSelectAlll = QtWidgets.QPushButton(self.groupBox_2)
        self.pushButton_removeSelectAlll.setGeometry(QtCore.QRect(468, 276, 79, 73))
        self.pushButton_removeSelectAlll.setObjectName("pushButton_removeSelectAlll")
        self.pushButton_exit = QtWidgets.QPushButton(self.groupBox_2)
        self.pushButton_exit.setGeometry(QtCore.QRect(468, 374, 79, 71))
        self.pushButton_exit.setObjectName("pushButton_exit")

        self.retranslateUi(Frame_containHideSettingScreen)
        QtCore.QMetaObject.connectSlotsByName(Frame_containHideSettingScreen)

    def retranslateUi(self, Frame_containHideSettingScreen):
        _translate = QtCore.QCoreApplication.translate
        Frame_containHideSettingScreen.setWindowTitle(_translate("Frame_containHideSettingScreen", "Frame"))
        self.groupBox.setTitle(_translate("Frame_containHideSettingScreen", "Danh sách tài khoản"))
        self.pushButton_addNewAccount.setText(_translate("Frame_containHideSettingScreen", "Thêm mới"))
        self.groupBox_2.setTitle(_translate("Frame_containHideSettingScreen", "Chọn thí sinh"))
        self.pushButton_selectAll.setText(_translate("Frame_containHideSettingScreen", "Chọn \n"
"tất cả"))
        self.pushButton_removeSelectAlll.setText(_translate("Frame_containHideSettingScreen", "Bỏ chọn\n"
"Tất cả"))
        self.pushButton_exit.setText(_translate("Frame_containHideSettingScreen", "Thoát"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Frame_containHideSettingScreen = QtWidgets.QFrame()
    ui = Ui_Frame_containHideSettingScreen()
    ui.setupUi(Frame_containHideSettingScreen)
    Frame_containHideSettingScreen.show()
    sys.exit(app.exec_())
