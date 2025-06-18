from BaseCar import BaseCar
import basisklassen as bk
import time
import threading

class SonicCar(BaseCar):
    def __init__(self, forward_A, forward_B, turning_offset):
        super().__init__(forward_A, forward_B, turning_offset)
        self.USo = bk.Ultrasonic()
        self.distance = 0
        self.frontwheels = bk.FrontWheels()

    def get_distance(self):
        self.distance = self.USo.distance()
        return(self.USo.distance())
    
    def fahrmodus3(self):
        """Bedaten der Eigenschaften des Objetkts und Aufruf der Methoden gemäß Lastenheft für Fahrmodus1"""
        while True:
            if self.get_distance() >= 5:
                self.frontwheels.turn(90)
                self.speed = 30
                self.drive()
            elif self.get_distance() >= 0 and self.get_distance() <= 5:
                self.stop()
                break
               
    

# Objekt erzeugen und Methode aufrufen

# mein_auto = SonicCar()
# mein_auto.fahrmodus3()
