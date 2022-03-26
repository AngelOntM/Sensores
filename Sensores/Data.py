from tkinter.font import BOLD
from JSONS.JsonComandos import JsonFile


class DataSensor(JsonFile):
    def __init__(self,  id='', fecha='', hora='', valor='', medida='', nombre='', save=bool, lista=list()):
        self.id = id
        self.fecha = fecha
        self.hora = hora
        self.valor = valor
        self.medida = medida
        self.nombre = nombre
        self.save = save
