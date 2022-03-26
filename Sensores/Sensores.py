import adafruit_dht
import datetime
import board
import time
import RPi.GPIO as GPIO

class Sensores:
    def TH(self,pin):
        a = 1
        b = 2
        return a,b

    def IR(self,pin):
        a=1
        return a

    def FR(self,pin):
        a=1
        return 1

    def US(self,pin):
        a=1
        return a

    def VerListaSensores(self):
        print('1) Temperatura y Humedad')
        print('2) Infrarrojo')
        print('3) Fotoresistencia')
        print('4) Humedad del suelo')
        print('5) Humo')
        print('6) Proximidad')
