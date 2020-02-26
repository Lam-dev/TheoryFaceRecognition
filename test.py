# from  ParseXML.ParseXML   import ParseXML
# from DatabaseAccess.DatabaseAccess   import ThiSinhRepository

# x = ParseXML()
# listHocVien = x.ReadListStudentFromXML("/home/lam/AppLoadXml/K13C003VietBac.xml")
# khoThiSinh = ThiSinhRepository()
# for hocVien in listHocVien:
#     khoThiSinh.ghiDuLieu(hocVien)
import socket
from   datetime     import datetime
import json
SERVER_IP                                           = "192.168.1.59"
SERVER_PORT                                         = 2019
import getmac
def __DungKhungGiaoTiep(noiDung, malenh):
        
        if(type(noiDung) is not str): 
            return False, False
        highChieuDaiTen = int(len(noiDung) / 256)
        lowChieuDaiTen = int(len(noiDung) % 256)                                                                                                                                                                                                                                                                                    
        khungTruyen = [0x45,0x4C, 0x54, malenh,lowChieuDaiTen, highChieuDaiTen]
        tong = malenh + lowChieuDaiTen + highChieuDaiTen
        j = 0
        for i in range (len(khungTruyen), len(khungTruyen) + len(noiDung)):
            khungTruyen.append('')
            khungTruyen[i] = ord(noiDung[j])
            tong = tong + ord(noiDung[j])
            j = j+ 1
            
        tong = -(~tong) % 256
        khungTruyen.append(0x00)
        khungTruyen[len(khungTruyen)-1] = tong
        return bytes(khungTruyen), tong

def ConvertStringToByteArray(string):
    lstByte = []
    for i in range (0, len(string)):
        lstByte.append(ord(string[i]))
    return bytes(lstByte)
# f,s = __DungKhungGiaoTiep()

# client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# client.connect((SERVER_IP, SERVER_PORT))
# client.send(ConvertStringToByteArray('{"success":"true","code":"3","data":{"CardNumber":["1","2","3","4","5"],"action":"update"},"message":"null","checksum":"23"}'))
# clientObj = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# clientObj.connect((SERVER_IP, SERVER_PORT))
# clientObj.sendall(b'aaaa')

# clientObj = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# clientObj.connect((SERVER_IP, SERVER_PORT))
# clientObj.sendall(b'aaaa')
# x = [1,2,3]
# print(x)
# x.extend([3,4,5])
# print(x)

# dictData = {
#     "cardNumber":2,
#     "time":datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
#     "imageLength":0
# }
# dictToSend = {
#     "success":"true",
#     "code":2,
#     "massage":"",
#     "checksum":0,
#     "data":dictData
# }
# print(json.dumps(dictToSend))

# print(datetime.now().strftime("%d_%m_%Y"))
####### create course and update listStuden##################################
course = {
    "IDKhoaThi": 1,
    "TenKhoaThi":"KhoaThi 2/1/2020",
    "NgayTao":"13:32:32 02/01/2020",
    "DuongDanLuuAnh":""
}

lstName = ["Nguyễn Hồng Lâm", "Nguyễn Xuân Lộc", "Bùi Văn Trung", "Đỗ Mạnh Cường", "Đinh Trọng Tiến"]
lstStudent = []
for i in range(1, 5):
    student = {
        "CardNumber":i,
        "TraineeName":lstName[i]
    }
    lstStudent.append(student)

dic = {
    "success":"True",
    "code":3,
    "data":{
        # "CourseInfo":course,
        # "CardNumber":lstStudent,
        "fileName":"TTND_2020_02_19_CN.json",
        "action":"sync",
    },
    "message":12,
    "checksum":21
}

jsonStr = json.dumps(dic)
khungGui, tong = __DungKhungGiaoTiep(jsonStr, 3)
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((SERVER_IP, SERVER_PORT))
client.send(khungGui)

# ############################################################
# def __ConvertStringToUTF8String(string):
#     x = []
#     for elem in string:
#         x.append(ord(elem))
#     return(bytes(x).decode("utf8", "ignore"))


# string = "Nguy\xe1\xbb\x85n V\xc4\x83n A"


# print(__ConvertStringToUTF8String(string))

# }
# jsonObj = json.dumps(dicta, ensure_ascii=True)
# jsonDict =  json.loads(jsonObj)
# stra = jsonDict["stra"]
# print(stra)
# import os
# strTime = "2020-02-19 11:20:24.166959"
# os.system('date +%Y%m%d -s "20081128"')
# os.system('date +%T -s "21:02:00"')