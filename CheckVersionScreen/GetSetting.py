import json

def LoadSettingFromFile():
    with open('Setting/setting.json') as json_file:
        setting = json.load(json_file)
    return setting

def UpdateServerImageDir(dir):
    with open('GetSettingFromJSON/setting.json') as json_file:
        setting = json.load(json_file)
    setting["ServerImageDir"] = dir
    with open('GetSettingFromJSON/setting.json', 'w') as json_file:
        json.dump(setting, json_file)

def GetSystemSetting():
    try:
        with open('../Setting/setting.json') as json_file:
            return json.load(json_file)
    except:
        return 0

def SavePersonalSetting(settingDict):
    try:
        with open('../Setting/persionalSetting.json', 'w', encoding='utf8') as json_file:
            json.dump(settingDict, json_file)
    except:
        pass

# UpdateServerImageDir("local/abde")
# print(GetSetting("--ServerImageDir"))
