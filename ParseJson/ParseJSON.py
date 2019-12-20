import json
from    PyQt5.QtCore            import pyqtSlot, pyqtSignal,QTimer, QDateTime,Qt, QObject
from    collections import namedtuple

CODE_RECIPT_DATA_FROM_SERVER = 3
CODE_UPLOAD_DATA_TO_SERVER = 2
CODE_PING_PING = 1

class ParseJSON(QObject):
    def __init__(self):
        QObject.__init__(self)


    def ConvertJsonToObject(self, string):
        try:
            obj = json2obj(string)
            print(obj.data.CardNumber)
            
        except NameError as e:
            print(e)

def _json_object_hook(d): return namedtuple('X', d.keys())(*d.values())

def json2obj(data): return json.loads(data, object_hook=_json_object_hook)

ParseJSON().ConvertJsonToObject('{"success":"true","code":"3","data":{"CardNumber":["1","2","3","4","5"],"action":"update"},"message":"null","checksum":"23"}')