from JSONS.JsonComandos import JsonFile
import pymongo
import requests
from requests.structures import CaseInsensitiveDict


class Sensores(JsonFile):
    def __init__(self, id='', created_at='', updated_at='', pines=[], data=[], clave='', isActive=bool, seccion='', invernadero=1, store=bool, lista=list()):
        self.id = id
        self.pines = pines
        self.clave = clave
        self.isActive = isActive
        self.seccion = seccion
        self.invernadero = invernadero
        self.data = data
        self.created_at = created_at
        self.updated_at = updated_at
        self.store = store
        self.lista = lista
        super().__init__()

    def agregar(self, sensor):
        self.lista.append(sensor)

    def eliminar(self, sensor):
        self.lista.remove(sensor)

    def len(self):
        return len(self.lista)

    def getlist(self):
        return self.lista

    def __str__(self):
        return str(self.clave) + ' \t\t\t' + str(self.isActive) + ' \t\t\t' + \
               str(self.seccion) + ' \t\t\t' + str(self.invernadero)

    def toObjects(self):
        lista = list()
        data1 = self.getDataJson()
        for x in data1:
            lista.append(
                Sensores(id=x['id'], pines=x['pines'], clave=x['clave'], isActive=x['isActive'], data=x['data'], seccion=x['seccion'], invernadero=x['invernadero'], store=x['store'], created_at=x['created_at'], updated_at=x['updated_at']))
        self.lista = lista


    def apiGet(self):
        try:
            path = "http://3.87.205.61:3333/sensores"
            headers = CaseInsensitiveDict()
            headers["Accept"] = "application/json"
            token = self.Token()
            headers["Authorization"] = "Bearer %s" % f"{token}"
            resp = requests.get(path, headers=headers)
            return resp.json()
        except:
            return 'Fail'

    def apiPost(self,data):
        try:
            path = "http://3.87.205.61:3333/sensores"
            headers = CaseInsensitiveDict()
            headers["Accept"] = "application/json"
            token = self.Token()
            headers["Authorization"] = "Bearer %s" % f"{token}"
            resp = requests.post(path, data=data, headers=headers)
            return resp.json()
        except:
            return 'Fail'

    def apiPut(self, id,data):
        try:
            path = f"http://3.87.205.61:3333/sensores/{id}"
            headers = CaseInsensitiveDict()
            headers["Accept"] = "application/json"
            token = self.Token()
            headers["Authorization"] = "Bearer %s" % f"{token}"
            resp = requests.put(path, data=data, headers=headers)
            print(resp.json())
            return resp.json()
        except:
            return 'Fail'

    def apiDelete(self, id):
        try:
            path = f"http://3.87.205.61:3333/sensores/{id}"
            headers = CaseInsensitiveDict()
            headers["Accept"] = "application/json"
            token = self.Token()
            headers["Authorization"] = "Bearer %s" % f"{token}"
            resp = requests.delete(path, headers=headers)
            return resp.json()
        except:
            return 'Fail'

    def apiPutData(self,id,data):
        try:
            path = f"http://3.87.205.61:3333/data/{id}"
            headers = CaseInsensitiveDict()
            headers["Accept"] = "application/json"
            token = self.Token()
            headers["Authorization"] = "Bearer %s" % f"{token}"
            resp = requests.put(path, data=data, headers=headers)
            print(resp.json())
            return resp.json()
        except:
            return 'Fail'

    def Sincronizar(self):
        try:
            find = self.apiGet()
            self.toJsonApi(find['find'])
            self.toObjects()
        except:
            return False

    def getDataApi(self):
        lista = list()
        mycol = self.apiGet()
        data = mycol.find()
        for x in data:
            lista.append(
                Sensores(id=x['id'], pines=x['pines'], clave=x['clave'], isActive=x['isActive'], seccion=x['seccion'],
                         invernadero=x['invernadero'], data=x['data'], created_at=x['created_at'],
                         updated_at=x['updated_at']))
        self.lista = lista

    def __iter__(self):
        self.__idx__ = 0
        return self

    def __next__(self):
        if self.__idx__ < len(self.lista):
            x = self.lista[self.__idx__]
            self.__idx__ += 1
            return x
        else:
            raise StopIteration

    def Verificar(self):
        for x in self.lista:
            if x.store == False:
                try:
                    path = f"http://3.87.205.61:3333/sensores/{x.id}"
                    headers = CaseInsensitiveDict()
                    headers["Accept"] = "application/json"
                    token = self.Token()
                    headers["Authorization"] = "Bearer %s" % f"{token}"
                    resp = requests.put(path,data=x, headers=headers)
                except:
                    print('Fail')
                    return 'Fail'
        self.Sincronizar()

