# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'NoiDungManHinhCaiDatAmThanh.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Widget_ContainSoundSettingContent(object):
    def setupUi(self, Widget_ContainSoundSettingContent):
        Widget_ContainSoundSettingContent.setObjectName("Widget_ContainSoundSettingContent")
        Widget_ContainSoundSettingContent.resize(420, 145)
        self.frame_containVolumeSetting = QtWidgets.QFrame(Widget_ContainSoundSettingContent)
        self.frame_containVolumeSetting.setGeometry(QtCore.QRect(0, 56, 421, 81))
        self.frame_containVolumeSetting.setStyleSheet("border:0px;")
        self.frame_containVolumeSetting.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_containVolumeSetting.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_containVolumeSetting.setObjectName("frame_containVolumeSetting")
        self.label_amLuong = QtWidgets.QLabel(self.frame_containVolumeSetting)
        self.label_amLuong.setGeometry(QtCore.QRect(10, 10, 295, 21))
        self.label_amLuong.setMouseTracking(True)
        self.label_amLuong.setStyleSheet("font: 75 bold 12pt \"Ubuntu\";")
        self.label_amLuong.setObjectName("label_amLuong")
        self.label_iconVolume = QtWidgets.QLabel(self.frame_containVolumeSetting)
        self.label_iconVolume.setGeometry(QtCore.QRect(30, 40, 31, 31))
        self.label_iconVolume.setText("")
        self.label_iconVolume.setPixmap(QtGui.QPixmap("iconVolume.png"))
        self.label_iconVolume.setObjectName("label_iconVolume")
        self.horizontalSlider_ForChangeVolume = QtWidgets.QSlider(self.frame_containVolumeSetting)
        self.horizontalSlider_ForChangeVolume.setGeometry(QtCore.QRect(80, 40, 251, 29))
        self.horizontalSlider_ForChangeVolume.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider_ForChangeVolume.setObjectName("horizontalSlider_ForChangeVolume")
        self.label = QtWidgets.QLabel(Widget_ContainSoundSettingContent)
        self.label.setGeometry(QtCore.QRect(150, 10, 205, 41))
        self.label.setMouseTracking(True)
        self.label.setStyleSheet("font: 75 bold 18pt \"Ubuntu\";\n"
"color: rgb(85, 85, 0);")
        self.label.setObjectName("label")
        self.line_3 = QtWidgets.QFrame(Widget_ContainSoundSettingContent)
        self.line_3.setGeometry(QtCore.QRect(20, 44, 371, 16))
        self.line_3.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")

        self.retranslateUi(Widget_ContainSoundSettingContent)
        QtCore.QMetaObject.connectSlotsByName(Widget_ContainSoundSettingContent)

    def retranslateUi(self, Widget_ContainSoundSettingContent):
        _translate = QtCore.QCoreApplication.translate
        Widget_ContainSoundSettingContent.setWindowTitle(_translate("Widget_ContainSoundSettingContent", "Form"))
        self.label_amLuong.setText(_translate("Widget_ContainSoundSettingContent", "Âm lượng"))
        self.label.setText(_translate("Widget_ContainSoundSettingContent", "ÂM THANH"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Widget_ContainSoundSettingContent = QtWidgets.QWidget()
    ui = Ui_Widget_ContainSoundSettingContent()
    ui.setupUi(Widget_ContainSoundSettingContent)
    Widget_ContainSoundSettingContent.show()
    sys.exit(app.exec_())
