'''import RPi.GPIO as GPIO
import time
from gpiozero import LightSensor
import Adafruit_DHT'''



class LeerSensores():

    def US(self, pines=[]):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)
        GPIO.setup(pines[0], GPIO.OUT)
        GPIO.setup(pines[1], GPIO.IN)
        GPIO.output(pines[0], GPIO.LOW)
        time.sleep(0.5)
        GPIO.output(pines[0], GPIO.HIGH)
        time.sleep(0.00001)
        GPIO.output(pines[0], GPIO.LOW)
        while True:
            pulso_inicio = time.time()
            if GPIO.input(pines[1]) == GPIO.HIGH:
                break
        while True:
            pulso_fin = time.time()
            if GPIO.input(pines[1]) == GPIO.LOW:
                break
        duracion = pulso_fin - pulso_inicio
        distancia = (34300 * duracion) / 2
        return distancia
        GPIO.cleanup()

    def HG(self, pines=[]):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(pines[0], GPIO.IN)

        if GPIO.input(pines[0]):
            return None
        if GPIO.input(pines[0]) != 1:
            response = 1
            return response
        GPIO.cleanup()

    def IR(self, pines=[]):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)
        GPIO.setup(pines[0], GPIO.IN)
        if (GPIO.input(pines[0]) == True):  # object is far away
            return None
        else:
            persona = 1
            return persona
            time.sleep(1)
        GPIO.cleanup()

    def TH(self,pines=[]):
        Sensor_Dht = Adafruit_DHT.DHT11
        Pin_dht = pines[0]
        humedad,temperatura = Adafruit_DHT.read(Sensor_Dht, Pin_dht)
        if humedad is not None and temperatura is not None:
            dicciionario = {"temperatura": temperatura, "humedad": humedad}
            return dicciionario
        else:
            return None
   
    def FR(self, pines=[]):
        ldr = LightSensor(pines[0])
        return ldr.value
