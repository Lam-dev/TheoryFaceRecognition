import enum
class DefineWriteCardNotify():
    def __init__(self):
        self.waitCard = 1
        self.written = 2

class AddDataResult():
    def __init__(self):
        self.faceAdded = bool
        self.FGPadded = bool
        self.numberFGPadded = int
        self.cardWritten = bool

class RequestFromTakeSample(enum.Enum):
    Reset = 1
    Shutdown = 2
    Restore = 3
    UpdateFW = 4
    DelAllTeacher = 5
    CheckVersion = 6
        