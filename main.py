from Sensores.InterfaceSensores import InterfaceSensor
import os
import requests
from requests.structures import CaseInsensitiveDict
import json


class Main:
    def __init__(self):
        self.interfaceSensor = InterfaceSensor()

    def cls(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def getToken(self):
        try:
            data = {'email':'rasp@rasp.com','password':'12345678'}
            path = "http://3.87.205.61:3333/users/login"
            headers = CaseInsensitiveDict()
            headers["Accept"] = "application/json"
            resp = requests.post(path, data=data)
            data = resp.json()
            data1 = data['token']
            token = data1['token']
            self.toJson(token)
            self.menuPrincipal()
        except:
            print('Fail')

    def toJson(self, token):
        file = open("JSONS/Token.json", "w")
        file = json.dump(token, file, indent=4)

    def menuPrincipal(self):
        self.interfaceSensor.menuPrincipal()



if __name__ == '__main__':
    ip = Main()
    ip.getToken()
