import json
def SaveSystemSetting(settingDict):
    with open('../Setting/systemSetting.json', 'w') as json_file:
        json.dump(settingDict, json_file)

def SaveSoundSetting(settingDict):
    with open('../Setting/soundSetting.json', 'w') as json_file:
        json.dump(settingDict, json_file)