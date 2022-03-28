import time
from Sensores.ObjetoSensor import Sensores
from Sensores.Data import DataSensor
from Sensores.Sensores import LeerSensores
import datetime
import os
import multiprocessing


class InterfaceSensor:
    def __init__(self):
        self.leerSensores = LeerSensores()
        self.objetoSensor = Sensores()
        self.objetoData = DataSensor()
        self.objetoSensor.toObjects()
        self.date = datetime.datetime.now()

    def cls(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def AgregarSensor(self):
        sensor = Sensores()
        sensor.id = self.objetoSensor.len()
        print('1) Temperatura y Humedad')
        print('2) Infrarrojo')
        print('3) Fotoresistencia')
        print('4) Humedad del suelo')
        print('5) Humo')
        print('6) Ultrasonico')
        valor = int(input('Selecciona el sensor:'))
        if valor != 6:
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
            sensor.clave = 'HS'
        elif valor == 5:
            sensor.clave = 'GH'
        elif valor == 6:
            sensor.clave = 'US'
        sensor.isActive = True
        sensor.seccion = int(input('Seleccione la seccion (1):'))
        sensor.created_at = self.date.strftime('%Y/%m/%d  %X')
        sensor.updated_at = self.date.strftime('%Y/%m/%d  %X')
        return sensor

    def agregarPines(self, tipo):
        pines = []
        if tipo == 1:
            pines.append(int(input('Escribe el pin:')))
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
            else:
                sensor.pines = self.agregarPines(1)
        elif dato1 == 2:
            sensor.seccion = int(input('Seleccione la seccion (1):'))
        else:
            print('Opcion no valida')

    def EliminarSensor(self):
        self.VerSensores()
        dato = int(input('Escribe el id del sensor:'))
        self.objetoSensor.eliminar(dato)

    def VerSensores(self, lista=None):
        self.cls()
        print("\n" + "-" * 20 + "Datos de Sensores" + "-" * 20)
        if (lista == None):
            mylista = self.objetoSensor
        else:
            mylista = lista
        print("Id" + "\t\t" + 'Clave' + '\t\t' +
              'isActive' + "\t\t" + 'Seccion' + "\t\t" + 'Invernadero')
        for p in mylista:
            print(str(p))

    def ActivarTodos(self):
        print('1) Activar Todos')
        print('2) Desactivar Todos')
        dato = int(input('Escribe la opcion:'))
        if dato == 1:
            lista = self.objetoSensor.getlist()
            for x in lista:
                x.isActive = True
        elif dato == 2:
            lista = self.objetoSensor.getlist()
            for x in lista:
                x.isActive = False
        else:
            input('Opcion no valida')

    def ActivarUno(self):
        self.VerSensores()
        dato = int(input('Escribe el id del sensor:'))
        x = self.objetoSensor.getlist()[dato]
        x.isActive = True

    def DesactivarUno(self):
        self.VerSensores()
        dato = int(input('Escribe el id del sensor:'))
        x = self.objetoSensor.getlist()[dato]
        x.isActive = False

    def Verificar(self):
        sensores = self.objetoSensor.getlist()
        y = 0
        for x in sensores:
            if x.isActive == True:
                p = multiprocessing.Process(target=self.Medicion(x))

    def Medicion(self, sensor):
        dataObjeto = DataSensor()
        if sensor.clave == 'IR':
            dataObjeto.valor = self.leerSensores.IR(sensor.pines)
            dataObjeto.id = len(sensor.data)
            dataObjeto.fecha = self.date.strftime('%Y/%m/%d')
            dataObjeto.hora = self.date.strftime('%X')
            dataObjeto.medida = 'Persona'
            dataObjeto.nombre = 'IR'
            dataObjeto.save = True
            sensor.data.append(dataObjeto.__dict__)
            print(dataObjeto.valor)
            self.objetoSensor.toJson(self.objetoSensor)
            time.sleep(2.0)
        elif sensor.clave == 'US':
            dataObjeto.valor = self.leerSensores.US(sensor.pines)
            dataObjeto.id = len(sensor.data)
            dataObjeto.fecha = self.date.strftime('%Y/%m/%d')
            dataObjeto.hora = self.date.strftime('%X')
            dataObjeto.medida = 'M'
            dataObjeto.nombre = 'US'
            dataObjeto.save = True
            sensor.data.append(dataObjeto.__dict__)
            self.objetoSensor.toJson(self.objetoSensor)
            print(dataObjeto.valor)
            time.sleep(4.0)

    def menuPrincipal(self):
        a = ""
        while a != "x":
            self.cls()
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
                # self.objetoSensor.AgregarDB(s.__dict__)
            elif (a.lower() == 'b'):
                self.VerSensores()
            elif (a.lower() == 'c'):
                self.ActivarTodos()
                pass
            elif (a.lower() == 'd'):
                self.ActivarUno()
                pass
            elif (a.lower() == 'e'):
                self.DesactivarUno()
                pass
            elif (a.lower() == 'f'):
                self.ModificarSensor()
                pass
            elif (a.lower() == 'g'):
                self.EliminarSensor()
                pass
            elif (a.lower() == 'h'):
                self.Verificar()
                pass
            elif (a == 'x'):
                break
            else:
                print("Opcion invalida")
