import threading
import time
import simpleaudio as sa
import wave
from    PyQt5.QtCore   import QTimer, QObject
import os
from    GetSettingFromJSON    import GetSetting

fileXinCamOnPath = 'Sound/AudioFile/xinCamOn.wav'
fileVuiLongThuLaiPath = 'Sound/AudioFile/vuiLongThuLai.wav'
fileTemp = 'Sound/AudioFile/temp.wav'
fileBip = 'Sound/AudioFile/bip.wav'

class Sound(QObject):

    def __init__(self):
        QObject.__init__(self)
        # self.waveXinCamOn = sa.WaveObject.from_wave_file(fileXinCamOnPath)
        # self.waveVuiLongThuLai = sa.WaveObject.from_wave_file(fileVuiLongThuLaiPath)
        self.ReadConfigAndReadAudioFile()
        self.waveTemp = sa.WaveObject.from_wave_file(fileTemp)
        self.waveBip = sa.WaveObject.from_wave_file(fileBip)

        self.ThreadPlayTemp()
        self.timerPlayTemp = QTimer(self)
        self.timerPlayTemp.start(240000)
        self.timerPlayTemp.timeout.connect(self.ThreadPlayTemp)

    def ReadConfigAndReadAudioFile(self):
        try:
            SETTING_DICT  = GetSetting.GetSoundSetting()
            volume = SETTING_DICT["volume"]
            self.ReadAudioFile(volume)
        except:
            pass

    def ReadAudioFile(self, volume):
        try:

            if(volume < 30):
                self.waveXinCamOn = sa.WaveObject.from_wave_file('Sound/AudioFile/xinCamOn1.wav')
                self.waveVuiLongThuLai = sa.WaveObject.from_wave_file('Sound/AudioFile/vuiLongThuLai1.wav')
            elif(volume < 70):
                self.waveXinCamOn = sa.WaveObject.from_wave_file('Sound/AudioFile/xinCamOn2.wav')
                self.waveVuiLongThuLai = sa.WaveObject.from_wave_file('Sound/AudioFile/vuiLongThuLai2.wav')
            else:
                self.waveXinCamOn = sa.WaveObject.from_wave_file('Sound/AudioFile/xinCamOn3.wav')
                self.waveVuiLongThuLai = sa.WaveObject.from_wave_file('Sound/AudioFile/vuiLongThuLai3.wav')
            # stringSet = "amixer -D pulse sset Master " + str(volume) + "%"
            # os.system(stringSet)
        except:
            pass
        


    def __SetSound(self):
        try:
            SETTING_DICT  = GetSetting.GetSoundSetting()
            volume = SETTING_DICT["volume"]
            stringSet = "amixer -D pulse sset Master " + str(volume) + "%"
            os.system(stringSet)
        except:
            pass
        


    def __PlayBip(self):
        playSound = self.waveBip.play()
        playSound.wait_done()

    def ThreadPlayBip(self):
        thread = threading.Thread(target=self.__PlayBip, args=(), daemon=True)
        thread.start()

    def __PlayTemp(self):
        playSound = self.waveTemp.play()
        playSound.wait_done()

    def ThreadPlayTemp(self):
        thread = threading.Thread(target=self.__PlayTemp, args=(), daemon=True)
        thread.start()

    def __PlayXinCamOn(self):
        playSound = self.waveXinCamOn.play()
        playSound.wait_done()

    def __PlayVuiLongThuLai(self):
        
        playSound = self.waveVuiLongThuLai.play()
        playSound.wait_done()

    def ThreadPlayXinCamOn(self):
        self.timerPlayTemp.stop()
        self.timerPlayTemp.start(240000)
        thread = threading.Thread(target=self.__PlayXinCamOn, args=(), daemon=True)
        thread.start()

    def ThreadPlayVuiLongThuLai(self):
        self.timerPlayTemp.stop()
        self.timerPlayTemp.start(240000)
        thread = threading.Thread(target = self.__PlayVuiLongThuLai, args = (), daemon = True)
        thread.start()
