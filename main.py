from Sensores.InterfaceSensores import InterfaceSensor
import os


class Main:
    def __init__(self):
        self.interfaceSensor = InterfaceSensor()

    def cls(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def menuPrincipal(self):
        self.interfaceSensor.menuPrincipal()



if __name__ == '__main__':
    ip = Main()
    ip.menuPrincipal()
