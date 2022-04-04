from JSONS.JsonComandos import JsonFile
import pymongo


class Sensores(JsonFile):
    def __init__(self, id='', created_at='', updated_at='', pines=[], data=[], clave='', isActive=bool, seccion='', invernadero=1, save=bool, lista=list()):
        self.id = id
        self.pines = pines
        self.clave = clave
        self.isActive = isActive
        self.seccion = seccion
        self.invernadero = invernadero
        self.data = data
        self.created_at = created_at
        self.updated_at = updated_at
        self.save = save
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
        return str(self.id) + ' \t\t' + str(self.clave) + ' \t\t\t' + str(self.isActive) + ' \t\t\t' + \
               str(self.seccion) + ' \t\t\t' + str(self.invernadero)

    def toObjects(self):
        lista = list()
        data1 = self.getDataJson()
        for x in data1:
            lista.append(
                Sensores(id=x['id'], pines=x['pines'], clave=x['clave'], isActive=x['isActive'], seccion=x['seccion'], invernadero=x['invernadero'], data=x['data'], created_at=x['created_at'], updated_at=x['updated_at']))
        self.lista = lista

    def verificarDB(self):
        try:
            pymongo.MongoClient(
                'mongodb+srv://admin:admin@sensores.gr9v5.mongodb.net/proyecto?retryWrites=true&w=majority')
            return True
        except pymongo.errors.ConnectionFailure:
            return False
        except pymongo.errors.ConfigurationError:
            return False

    def MyCol(self):
        x = self.verificarDB()
        if x == True:
            y = self.DB()
            return y
        else:
            y = self.DBLocal()
            return y

    def DBLocal(self):
        myclient = pymongo.MongoClient('localhost:27017')
        mydb = myclient['proyecto']
        mycol = mydb['sensores']
        return mycol

    def DB(self):
        myclient = pymongo.MongoClient(
            'mongodb+srv://admin:admin@sensores.gr9v5.mongodb.net/proyecto?retryWrites=true&w=majority')
        mydb = myclient['proyecto']
        mycol = mydb['sensores']
        return mycol

    def SincronizarDB(self):
        mycol = self.MyCol()
        for x in self.lista:
            m = mycol.find_one({'id': x.id})
            if m == None:
                mycol.insert_one(x.__dict__)

    def SincronizarDatosDB(self):
        mycol = self.MyCol()
        for x in self.lista:
            m = mycol.find_one({'id': x.id})
            for y in m['data']:
                print(y)


    def getDataMongo(self):
        lista = list()
        mycol = self.MyCol()
        data = mycol.find()
        for x in data:
            lista.append(
                Sensores(id=x['id'], pines=x['pines'], clave=x['clave'], isActive=x['isActive'], seccion=x['seccion'],
                         invernadero=x['invernadero'], data=x['data'], created_at=x['created_at'],
                         updated_at=x['updated_at']))
        self.lista = lista

    def AgregarDB(self, dato):
        myloc= self.DBLocal()
        mycol = self.MyCol()
        if myloc == mycol:
            dato['save']=False
            myloc.insert_one(dato)
        else:
            mycol.insert_one(dato)

    def EliminarDB(self, id):
        myloc = self.DBLocal()
        mycol = self.MyCol()

#asdasd
    def AgregarDato(self, id, dato):
        mycol = self.MyCol()
        mycol.update_one({'id':id},{'$push':{'data':dato.__dict__}},True)

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
