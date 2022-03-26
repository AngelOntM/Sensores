from Lista import Lista
from ObjetoSensor import ObjetoSensor
from Sensores import Sensores
import os


class InterfaceSensor:
    def __init__(self):
        self.claseSensor = Sensores()
        self.listasensores = Lista()
        self.listasensores.toObjects()

    def cls(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def AgregarSensor(self):
        nombre = input('Escribe el nombre del sensor:')
        sensor = ObjetoSensor(nombre)
        sensor.id = self.listasensores.len()
        sensor.clave = input('Escribe la clave:(Ejemplo:TH)')
        x = 0
        while x.lower() == 's':
            pines = []
            pines.append(int(input('Escribe el pin')))
            x = input('Desea agregar otro pin?s/n')
            if x.lower() == 's':
                continue
            elif x.lower() == 'n':
                sensor.pin = pines
            else:
                print('Opcion invalida')
        sensor.filename=input('Escribe el nombre del sensor: ')
        return sensor

    def ListaSensores(self):
        for x in self.listasensores:
            x['clave']

    def EliminarSensor(self):
        self.listasensores

    def VerSensores(self, lista=None):
        self.cls()
        print("\n" + "-" * 20 + "Datos de Clientes" + "-" * 20)
        if (lista == None):
            mylista = self.listasensores
        else:
            mylista = lista
        print("Id".ljust(5) + "\t\t" + 'Clave'.ljust(20) + '\t\t' + 'Pines'.ljust(20) + "\t\t" + 'Clave'.ljust(20))
        i = 0
        for p in mylista:
            print(str(i).ljust(5) + "\t\t" + str(p))
            i += 1

    def ActivarTodos(self):
        x = 1

    def ActivarUno(self):
        x = 1

    def menuPrincipal(self):
        a = ""
        while a != "x":
            self.cls()
            print("\n" + "-" * 10 + "Menu Principal" + "-" * 10)
            print("a) Agregar Sensor")
            print("b) Ver Sensores")
            print("c) Activar todos")
            print("d) Activar un Sensor")
            print("e) Eliminar un Sensor")
            print("x) Salir")
            a = input("Selecciona una opción: ")
            if (a.lower() == 'a'):
                s = self.AgregarSensor()
                self.listasensores.agregar(s)
                self.listasensores.toJson(self.listasensores)
            elif (a.lower() == 'b'):
                self.VerSensores()
            elif (a.lower() == 'c'):
                self.ActivarTodos()
                pass
            elif (a.lower() == 'd'):
                self.ActivarUno()
                pass
            elif (a.lower() == 'e'):
                self.EliminarSensor()
                pass
            elif (a == 'x'):
                break
            else:
                print("Opcion invalida")
