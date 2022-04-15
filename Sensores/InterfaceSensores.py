from Sensores.ObjetoSensor import Sensores
from Sensores.Data import DataSensor
from Sensores.Sensores import LeerSensores
import datetime
import os


class InterfaceSensor:
    def __init__(self):
        self.leerSensores = LeerSensores()
        self.objetoSensor = Sensores()
        self.objetoSensor.toObjects()
        self.date = datetime.datetime.now()

    def cls(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def AgregarSensor(self):
        sensor = Sensores()
        ultimo = self.objetoSensor.len()
        sensor.id = ultimo
        print('1) Temperatura y Humedad')
        print('2) Infrarrojo')
        print('3) Fotoresistencia')
        print('4) Humo')
        print('5) Ultrasonico')
        valor = int(input('Selecciona el sensor:'))
        if valor != 5:
            lpines = self.agregarPines(1)
        else:
            lpines = self.agregarPines(2)
        sensor.pines = lpines
        if valor == 1:
            sensor.clave = 'TH'
        elif valor == 2:
            sensor.clave = 'IR'
        elif valor == 3:
            sensor.clave = 'FR'
        elif valor == 4:
            sensor.clave = 'HG'
        elif valor == 5:
            sensor.clave = 'US'
        sensor.isActive = 'true'
        sensor.seccion = int(input('Seleccione la seccion (1):'))
        sensor.created_at = self.date.strftime('%Y/%m/%d  %X')
        sensor.updated_at = self.date.strftime('%Y/%m/%d  %X')
        sensor.store = False
        return sensor

    def agregarPines(self, tipo):
        pines = list()
        if tipo == 1:
            pines.append(int(input('Escribe el pin:')))
            pines.append(0)
            return pines
        elif tipo == 2:
            pines.append(int(input('Escribe el pin 1 (ECHO):')))
            pines.append(int(input('Escribe el pin 2 (TRIG):')))
        return pines

    def ModificarSensor(self):
        self.VerSensores()
        dato = int(input('Escribe el id del sensor:'))
        sensor = self.objetoSensor.getlist()[dato]
        print("1) Pines")
        print("2) Seccion")
        dato1 = int(input('Selecciona la opcion:'))
        if dato1 == 1:
            if sensor.clave == 'US':
                sensor.pines = self.agregarPines(2)
                sensor.updated_at = self.date.strftime('%Y/%m/%d  %X')
                sensor.store = False
                sensor.isActive = str(sensor.isActive).lower()

            else:
                sensor.pines = self.agregarPines(1)
                sensor.updated_at = self.date.strftime('%Y/%m/%d  %X')
                sensor.store = False
                sensor.isActive = str(sensor.isActive).lower()
            self.objetoSensor.apiPut(sensor.id, sensor.__dict__)
        elif dato1 == 2:
            sensor.seccion = int(input('Seleccione la seccion (1):'))
            sensor.updated_at = self.date.strftime('%Y/%m/%d  %X')
            sensor.store = False
            sensor.isActive = str(sensor.isActive).lower()
            self.objetoSensor.apiPut(sensor.id, sensor.__dict__)
        else:
            print('Opcion no valida')

    def EliminarSensor(self):
        self.VerSensores()
        dato = int(input('Escribe el id del sensor:'))
        self.objetoSensor.apiDelete(dato)
        self.objetoSensor.eliminar(self.objetoSensor.getlist()[dato])

    def VerSensores(self, lista=None):
        self.cls()
        print("\n" + "-" * 20 + "Datos de Sensores" + "-" * 20)
        if (lista == None):
            mylista = self.objetoSensor
        else:
            mylista = lista
        print("Id" + "\t\t" + 'Clave' + '\t\t' +
              'isActive' + "\t\t" + 'Seccion' + "\t\t" + 'Invernadero')
        i = 0
        for p in mylista:
            print(str(i) + ' \t\t' + str(p))
            i += 1

    def ActivarTodos(self):
        print('1) Activar Todos')
        print('2) Desactivar Todos')
        print('3) Regresar')
        dato = int(input('Escribe la opcion:'))
        if dato == 1:
            for x in self.objetoSensor:
                x.isActive = 'true'
                x.store = False
                self.objetoSensor.apiPut(x.id, x.__dict__)
        elif dato == 2:
            for x in self.objetoSensor:
                print(x)
                x.isActive = 'false'
                x.store = False
                self.objetoSensor.apiPut(x.id, x.__dict__)
        elif dato == 3:
            pass
        else:
            input('Opcion no valida')

    def ActivarUno(self):
        self.VerSensores()
        dato = int(input('Escribe el id del sensor:'))
        x = self.objetoSensor.getlist()[dato]
        x.isActive = 'true'
        x.store = False
        self.objetoSensor.apiPut(x.id, x.__dict__)

    def DesactivarUno(self):
        self.VerSensores()
        dato = int(input('Escribe el id del sensor:'))
        x = self.objetoSensor.getlist()[dato]
        x.isActive = 'false'
        x.store = False
        self.objetoSensor.apiPut(x.id, x.__dict__)

    def Verificar(self):
        sensores = self.objetoSensor.getlist()
        while True:
            for x in sensores:
                if x.isActive == True:
                    dataObjeto = DataSensor()
                    date = datetime.datetime.now()
                    ultimo = len(x.data)
                    if ultimo == 0:
                        x.data.append({'hora': 0})
                    if x.clave == 'IR':
                        dataObjeto.valor = self.leerSensores.IR(x.pines)
                        if dataObjeto.valor != None:
                            dataObjeto.id = ultimo
                            dataObjeto.fecha = date.strftime('%Y/%m/%d')
                            dataObjeto.hora = date.strftime('%H:%M')
                            dataObjeto.medida = 'Persona'
                            dataObjeto.nombre = 'IR'
                            dataObjeto.store = 'false'
                            x.data.append(dataObjeto.__dict__)
                            x.store = False
                            print(dataObjeto.nombre + ': ' + str(dataObjeto.valor))
                            self.objetoSensor.apiPutData(x.id, dataObjeto.__dict__)
                    elif x.clave == 'US':
                        if int(date.strftime('%I')) == 12 and x.data[-1]['hora'] != date.strftime('%H:%M'):
                            dataObjeto.valor = self.leerSensores.US(x.pines)
                            dataObjeto.id = ultimo
                            dataObjeto.fecha = date.strftime('%Y/%m/%d')
                            dataObjeto.hora = date.strftime('%H:%M')
                            dataObjeto.medida = 'M'
                            dataObjeto.nombre = 'US'
                            dataObjeto.store = 'false'
                            x.data.append(dataObjeto.__dict__)
                            x.store = False
                            print(dataObjeto.nombre + ': ' + str(dataObjeto.valor))
                            self.objetoSensor.apiPutData(x.id, dataObjeto.__dict__)
                    elif x.clave == 'FR':
                        if (int(date.strftime('%M')) + 5) % 5 == 0 and x.data[-1]['hora'] != date.strftime('%H:%M'):
                            dataObjeto.valor = self.leerSensores.FR(x.pines)
                            dataObjeto.id = ultimo
                            dataObjeto.fecha = date.strftime('%Y/%m/%d')
                            dataObjeto.hora = date.strftime('%H:%M')
                            dataObjeto.medida = 'O'  #################
                            dataObjeto.nombre = 'FR'
                            dataObjeto.store = 'false'
                            x.data.append(dataObjeto.__dict__)
                            x.store = False
                            print(dataObjeto.nombre + ': ' + str(dataObjeto.valor))
                            self.objetoSensor.apiPutData(x.id, dataObjeto.__dict__)
                    elif x.clave == 'HG':
                        dataObjeto.valor = self.leerSensores.HG(x.pines)
                        if dataObjeto.valor != None:
                            dataObjeto.id = ultimo
                            dataObjeto.fecha = date.strftime('%Y/%m/%d')
                            dataObjeto.hora = date.strftime('%H:%M')
                            dataObjeto.medida = 'Humo'  #################
                            dataObjeto.nombre = 'HG'
                            dataObjeto.store = 'false'
                            x.data.append(dataObjeto.__dict__)
                            x.store = False
                            print(dataObjeto.nombre + ': ' + str(dataObjeto.valor))
                            self.objetoSensor.apiPutData(x.id, dataObjeto.__dict__)
                    elif x.clave == 'TH':
                        if (int(date.strftime('%M')) + 5) % 5 == 0 and x.data[-1]['hora'] != date.strftime('%H:%M'):
                            valores = self.leerSensores.TH(x.pines)
                            dataObjeto.valor = valores[0]
                            dataObjeto.id = ultimo
                            dataObjeto.fecha = date.strftime('%Y/%m/%d')
                            dataObjeto.hora = date.strftime('%H:%M')
                            dataObjeto.medida = 'C'
                            dataObjeto.nombre = 'TM'
                            dataObjeto.store = 'false'
                            x.data.append(dataObjeto.__dict__)
                            x.store = False
                            print(dataObjeto.nombre + ': ' + str(dataObjeto.valor))
                            self.objetoSensor.apiPutData(x.id, dataObjeto.__dict__)
                            dataObjeto.valor = valores[1]
                            dataObjeto.id = ultimo + 1
                            dataObjeto.fecha = date.strftime('%Y/%m/%d')
                            dataObjeto.hora = date.strftime('%H:%M')
                            dataObjeto.medida = '%'
                            dataObjeto.nombre = 'HM'
                            dataObjeto.store = 'false'
                            x.data.append(dataObjeto.__dict__)
                            x.store = False
                            print(dataObjeto.nombre + ': ' + str(dataObjeto.valor))
                            self.objetoSensor.apiPutData(x.id, dataObjeto.__dict__)
                        if ultimo == 0:
                            x.data.remove([0])
                self.objetoSensor.toJson(self.objetoSensor)

    def menuPrincipal(self):
        a = ""
        while a != "x":
            self.cls()
            self.objetoSensor.Verificar()
            self.objetoSensor.toObjects()
            print("\n" + "-" * 10 + "Menu Principal" + "-" * 10)
            print("a) Agregar Sensor")
            print("b) Ver Sensores")
            print("c) Activar/Desactivar todos")
            print("d) Activar un Sensor")
            print("e) Desactivar un Sensor")
            print("f) Modificar un Sensor")
            print("g) Eliminar un Sensor")
            print("h) Leer Sensores")
            print("x) Salir")
            a = input("Selecciona una opción: ")
            if (a.lower() == 'a'):
                s = self.AgregarSensor()
                self.objetoSensor.agregar(s)
                self.objetoSensor.toJson(self.objetoSensor)
                self.objetoSensor.apiPost(s.__dict__)
            elif (a.lower() == 'b'):
                self.VerSensores()
            elif (a.lower() == 'c'):
                self.ActivarTodos()
                self.objetoSensor.toJson(self.objetoSensor)
                pass
            elif (a.lower() == 'd'):
                self.ActivarUno()
                self.objetoSensor.toJson(self.objetoSensor)
                pass
            elif (a.lower() == 'e'):
                self.DesactivarUno()
                self.objetoSensor.toJson(self.objetoSensor)
                pass
            elif (a.lower() == 'f'):
                self.ModificarSensor()
                self.objetoSensor.toJson(self.objetoSensor)
                pass
            elif (a.lower() == 'g'):
                self.EliminarSensor()
                self.objetoSensor.toJson(self.objetoSensor)
                pass
            elif (a.lower() == 'h'):
                self.objetoSensor.toJson(self.objetoSensor)
                self.Verificar()
                pass
            elif (a == 'x'):
                break
            else:
                print("Opcion invalida")
