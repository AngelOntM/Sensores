import os.path
import json


class JsonFile:
    def __init__(self):
        self.filename = "JSONS/Sensores.json"

    def getDataJson(self):
        data = []
        if (os.path.isfile(self.filename)):
            file = open(self.filename, "r")
            data = json.loads(file.read())
        return data

    def toJson(self, lista):
        file = open(self.filename, "w")
        file = json.dump([ob.__dict__ for ob in lista], file, indent=4)

    def toJsonApi(self, lista):
        file = open(self.filename, "w")
        file = json.dump([ob for ob in lista], file, indent=4)

    def getInfoJson(self):
        data = {}
        if (os.path.isfile(self.filename)):
            file = open(self.filename, "r")
            data = json.loads(file.read())
        return data

    def setInfoJson(self, info):
        file = open(self.filename, "w")
        json.dump(info,file,indent=4)

