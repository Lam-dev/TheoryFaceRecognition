# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'HienThiThongTinThiSinh.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Frame(object):
    def setupUi(self, Frame):
        Frame.setObjectName("Frame")
        Frame.resize(493, 351)
        Frame.setStyleSheet("background-color: rgb(255, 255, 255);")
        Frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        Frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.label_forShowStudentImage = QtWidgets.QLabel(Frame)
        self.label_forShowStudentImage.setGeometry(QtCore.QRect(16, 58, 151, 179))
        self.label_forShowStudentImage.setStyleSheet("background-color: rgb(170, 170, 255);")
        self.label_forShowStudentImage.setText("")
        self.label_forShowStudentImage.setObjectName("label_forShowStudentImage")
        self.label_thongTinHocVien = QtWidgets.QLabel(Frame)
        self.label_thongTinHocVien.setGeometry(QtCore.QRect(100, 10, 323, 31))
        self.label_thongTinHocVien.setStyleSheet("color: rgb(33, 33, 33);\n"
"font: 75 bold 18pt \"Ubuntu\";\n"
"")
        self.label_thongTinHocVien.setObjectName("label_thongTinHocVien")
        self.label_nameOfStudent = QtWidgets.QLabel(Frame)
        self.label_nameOfStudent.setGeometry(QtCore.QRect(184, 66, 275, 75))
        self.label_nameOfStudent.setStyleSheet("color: rgb(38, 38, 38);\n"
"font: 75 bold 16pt \"Ubuntu\";")
        self.label_nameOfStudent.setWordWrap(True)
        self.label_nameOfStudent.setObjectName("label_nameOfStudent")
        self.label_ngaySinh = QtWidgets.QLabel(Frame)
        self.label_ngaySinh.setGeometry(QtCore.QRect(178, 160, 97, 17))
        self.label_ngaySinh.setObjectName("label_ngaySinh")
        self.label_forShowDateOfBird = QtWidgets.QLabel(Frame)
        self.label_forShowDateOfBird.setGeometry(QtCore.QRect(292, 160, 189, 17))
        self.label_forShowDateOfBird.setObjectName("label_forShowDateOfBird")
        self.label_soCMTND = QtWidgets.QLabel(Frame)
        self.label_soCMTND.setGeometry(QtCore.QRect(178, 188, 97, 17))
        self.label_soCMTND.setObjectName("label_soCMTND")
        self.label_forShowIDnumber = QtWidgets.QLabel(Frame)
        self.label_forShowIDnumber.setGeometry(QtCore.QRect(292, 186, 189, 17))
        self.label_forShowIDnumber.setObjectName("label_forShowIDnumber")
        self.label_faceIcon = QtWidgets.QLabel(Frame)
        self.label_faceIcon.setGeometry(QtCore.QRect(20, 256, 39, 31))
        self.label_faceIcon.setText("")
        self.label_faceIcon.setObjectName("label_faceIcon")
        self.label_FGPicon = QtWidgets.QLabel(Frame)
        self.label_FGPicon.setGeometry(QtCore.QRect(20, 296, 39, 31))
        self.label_FGPicon.setText("")
        self.label_FGPicon.setObjectName("label_FGPicon")
        self.label_nhanDienKhuonMat = QtWidgets.QLabel(Frame)
        self.label_nhanDienKhuonMat.setGeometry(QtCore.QRect(76, 256, 181, 31))
        self.label_nhanDienKhuonMat.setObjectName("label_nhanDienKhuonMat")
        self.label_nhanDienVanTay = QtWidgets.QLabel(Frame)
        self.label_nhanDienVanTay.setGeometry(QtCore.QRect(74, 300, 181, 31))
        self.label_nhanDienVanTay.setObjectName("label_nhanDienVanTay")
        self.label_forShowNumberFaceAdded = QtWidgets.QLabel(Frame)
        self.label_forShowNumberFaceAdded.setGeometry(QtCore.QRect(270, 258, 149, 29))
        self.label_forShowNumberFaceAdded.setText("")
        self.label_forShowNumberFaceAdded.setObjectName("label_forShowNumberFaceAdded")
        self.label_forShowNumberFGPadded = QtWidgets.QLabel(Frame)
        self.label_forShowNumberFGPadded.setGeometry(QtCore.QRect(270, 300, 149, 29))
        self.label_forShowNumberFGPadded.setText("")
        self.label_forShowNumberFGPadded.setObjectName("label_forShowNumberFGPadded")
        self.pushButton_deleteFaceAdded = QtWidgets.QPushButton(Frame)
        self.pushButton_deleteFaceAdded.setGeometry(QtCore.QRect(448, 252, 39, 39))
        self.pushButton_deleteFaceAdded.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"color: rgba(0,190,255,255);\n"
"border-style: solid;\n"
"border-radius: 3px;\n"
"border-width: 0px;\n"
"border-color: rgba(0,140,255,255);")
        self.pushButton_deleteFaceAdded.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("../../../icon/iconDelete.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_deleteFaceAdded.setIcon(icon)
        self.pushButton_deleteFaceAdded.setIconSize(QtCore.QSize(38, 38))
        self.pushButton_deleteFaceAdded.setObjectName("pushButton_deleteFaceAdded")
        self.pushButton_deleteFGPadded = QtWidgets.QPushButton(Frame)
        self.pushButton_deleteFGPadded.setGeometry(QtCore.QRect(448, 296, 39, 39))
        self.pushButton_deleteFGPadded.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"color: rgba(0,190,255,255);\n"
"border-style: solid;\n"
"border-radius: 0px;\n"
"border-width: 0px;\n"
"border-color: rgba(0,140,255,255);")
        self.pushButton_deleteFGPadded.setText("")
        self.pushButton_deleteFGPadded.setIcon(icon)
        self.pushButton_deleteFGPadded.setIconSize(QtCore.QSize(38, 38))
        self.pushButton_deleteFGPadded.setObjectName("pushButton_deleteFGPadded")

        self.retranslateUi(Frame)
        QtCore.QMetaObject.connectSlotsByName(Frame)

    def retranslateUi(self, Frame):
        _translate = QtCore.QCoreApplication.translate
        Frame.setWindowTitle(_translate("Frame", "Frame"))
        self.label_thongTinHocVien.setText(_translate("Frame", "THÔNG TIN HỌC VIÊN"))
        self.label_nameOfStudent.setText(_translate("Frame", "Chọn một thí sinh"))
        self.label_ngaySinh.setText(_translate("Frame", "Ngày sinh"))
        self.label_forShowDateOfBird.setText(_translate("Frame", "TextLabel"))
        self.label_soCMTND.setText(_translate("Frame", "Số CMTND"))
        self.label_forShowIDnumber.setText(_translate("Frame", "cmtnd"))
        self.label_nhanDienKhuonMat.setText(_translate("Frame", "Nhận diện khuôn mặt:"))
        self.label_nhanDienVanTay.setText(_translate("Frame", "Nhận diện vân tay:"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Frame = QtWidgets.QFrame()
    ui = Ui_Frame()
    ui.setupUi(Frame)
    Frame.show()
    sys.exit(app.exec_())
