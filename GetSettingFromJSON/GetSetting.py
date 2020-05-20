import json

def GetSetting(arg):
    with open('GetSettingFromJSON/setting.json') as json_file:
        setting = json.load(json_file)
    if(arg == "--ServerImageDir"):
        return setting["ServerImageDir"]
    if(arg == "--FTPserverIP"):
        return setting["FTPserverIP"]
    if(arg == "--FTPserverPort"):
        return setting["FTPserverPort"]
    if(arg == "--FTPaccount"):
        return setting["FTPaccount"]
    if(arg == "--FTPpassword"):
        return setting["FTPpassword"]
    if(arg == "--SocketServerIP"):
        return setting["SocketServerIP"]
    if(arg == "--SocketServerPort"):
        return setting["SocketServerPort"]

def LoadSettingFromFile():
    try:
        with open('../Setting/systemSetting.json') as json_file:
            setting = json.load(json_file)
        return setting
    except:
        return 0

def LoadPasswordSetting():
    try:
        with open('../Setting/settingPassword.json') as json_file:
            data = json.load(json_file)
        return data["password"]
    except Exception as ex:
        print(ex.args)
        try:
            with open('../Setting/settingPassword.json', 'w') as json_file:
                dict = {
                    "password":"12345",
                }
                json.dump(dict, json_file)
            return "12345"
        except:
            pass

def UpdateServerImageDir(dir):
    with open('GetSettingFromJSON/setting.json') as json_file:
        setting = json.load(json_file)
    setting["ServerImageDir"] = dir
    with open('GetSettingFromJSON/setting.json', 'w') as json_file:
        json.dump(setting, json_file)

def GetSystemSetting():
    try:
        with open('../Setting/systemSetting.json') as json_file:
            return json.load(json_file)
    except:
        return 0

def GetSoundSetting():
    try:
        with open('../Setting/soundSetting.json') as json_file:
            return json.load(json_file)
    except:
        try:
            with open('../Setting/soundSetting.json', 'w') as json_file:
                dict = {
                    "volume":50,
                }
                json.dump(dict, json_file)
            with open('../Setting/soundSetting.json') as json_file:
                return json.load(json_file)
        except:
            return 0

def GetPersionalSetting():
    try:
        with open('../Setting/persionalSetting.json', encoding= "utf-8") as json_file:
            return json.load(json_file)
    except:
        return 0


def GetEcotekServerSetting():
    try:
        with open('../Setting/setting.json') as json_file:
            return json.load(json_file)
    except:
        return 0

def GetUARTsetting():
    try:
        with open('../Setting/uartSetting.json') as json_file:
            return json.load(json_file)
    except:
        return 0
            
# UpdateServerImageDir("local/abde")
# print(GetSetting("--ServerImageDir"))
