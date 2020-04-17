from SettingScreen.SoundSettingScreenContentUI import Ui_Widget_ContainSoundSettingContent
from PyQt5.QtCore import pyqtSlot, pyqtSignal,QTimer, QDateTime, Qt, QObject, QPointF, QPropertyAnimation, pyqtProperty
from PyQt5 import QtWidgets, QtGui
from GetSettingFromJSON   import GetSetting, SaveSetting
import os

class SoundSettingContent(Ui_Widget_ContainSoundSettingContent, QObject):
    def __init__(self):
        QObject.__init__(self)
        Ui_Widget_ContainSoundSettingContent.__init__(self)
        self.scrollAreaContent = QtWidgets.QWidget()
        self.setupUi(self.scrollAreaContent)
        self.label_iconVolume.setPixmap(QtGui.QPixmap("icon/iconVolume.png"))
        self.horizontalSlider_ForChangeVolume.mouseReleaseEvent = lambda event: self.VolumeChange()
        self.GetAndShowSetting()
    def VolumeChange(self):
        volume = self.horizontalSlider_ForChangeVolume.value()
        stringSet = "amixer -D pulse sset Master " + str(volume) + "%"
        os.system(stringSet)

    def GetWidgetContent(self):
        return self.scrollAreaContent
    
    def SaveSetting(self):
        volume = self.horizontalSlider_ForChangeVolume.value()
        settingDict = {
            # "autoShutdown" : self.comboBox_chooseTime.currentIndex(),
            "volume":int(volume)
        }
        SaveSetting.SaveSoundSetting(settingDict)
        

    def GetAndShowSetting(self):
        settingDict = GetSetting.GetSoundSetting()
        try:
            self.horizontalSlider_ForChangeVolume.setValue(settingDict["volume"])
        except:
            pass
