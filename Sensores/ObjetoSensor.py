from JSONS.JsonComandos import JsonFile
import pymongo


class Sensores(JsonFile):
    def __init__(self, id='', created_at='', updated_at='', pines=[], data=[], clave='', isActive=bool, seccion='', invernadero=1, lista=list()):
        self.id = id
        self.pines = pines
        self.clave = clave
        self.isActive = isActive
        self.seccion = seccion
        self.invernadero = invernadero
        self.data = data
        self.created_at = created_at
        self.updated_at = updated_at
        self.lista = lista

    def agregar(self, sensor):
        self.lista.append(sensor)

    def eliminar(self, sensor):
        self.lista.remove(sensor)

    def len(self):
        return len(self.lista)

    def getlist(self):
        return self.lista

    def toObjects(self):
        lista = list()
        data1 = self.getDataJson()
        for x in data1:
            lista.append(
                Sensores(id=x['id'], pines=x['pines'], clave=x['clave'], isActive=x['isActive'], seccion=x['seccion'], invernadero=x['invernadero'], data=x['data'], created_at=x['created_at'], updated_at=x['updated_at']))
        self.lista = lista

    def verificarDB(self):
        client = pymongo.MongoClient(
            'mongodb+srv://admin:admin@sensores.gr9v5.mongodb.net/proyecto?retryWrites=true&w=majority')
        client.server_info()
        print(client.server_info)
        if client.server_info == True:
            return True
        else:
            return False

    def MyCol(self, coleccion):
        x = self.verificarDB()
        if x == True:
            y = self.DB(coleccion)
            return y
        else:
            y = self.DBLocal(coleccion)
            return y

    def DBLocal(self, coleccion):
        myclient = pymongo.MongoClient(
            'mongodb://localhost:27017/?readPreference=primary&appname=MongoDB%20Compass&directConnection=true&ssl=false')
        mydb = myclient['proyecto']
        mycol = mydb[coleccion]
        return mycol

    def DB(self, coleccion):
        myclient = pymongo.MongoClient(
            'mongodb+srv://admin:admin@sensores.gr9v5.mongodb.net/proyecto?retryWrites=true&w=majority')
        mydb = myclient['proyecto']
        mycol = mydb[coleccion]
        return mycol

    def SincronizarDB(self, coleccion):
        mycol = self.DB(coleccion)
        data = self.getDataJson()
        for x in data:
            mycol.insert_one(x)
        data = []
        self.toJson(data)

    def AgregarDB(self, coleccion, dato):
        mycol = self.DB(coleccion)
        mycol.insert_one(dato)

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
