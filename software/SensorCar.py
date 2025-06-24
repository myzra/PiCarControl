from BaseCar import BaseCar
import basisklassen as bk
import time
import json
import os
#import save

class SensorCar(BaseCar):
    def __init__(self, forward_A, forward_B, turning_offset, INf_offset):
        super().__init__(forward_A, forward_B, turning_offset)
        self.USo = bk.Ultrasonic()
        self.distance = 0
        self.INf = bk.Infrared(INf_offset)
        self.fahrdaten = []
    def fahrmodus5(self): #Funktion für Fahrmodus5.
        doku = "nein"
        zaehler = 0 #Wird benötigt wenn Fahrzeug zwischen dem Sensor steht --> Weiterfahrt zwischen IR-Sensor.
        while True:
            #print(self.INf.read_digital())
            print(self.INf.read_analog())
            print(self.INf.read_digital())
            print(self.USo.distance())
            #time.sleep(1)

            INf_daten = self.INf.read_digital() # Liste mit IR-Werte Sensor 1-5
            if INf_daten[2] == 1: # 2 = Sensor in der Mitte --> Abfrage belegt.
                if self.steering_angle != 90:
                    doku = "ja"
                self.steering_angle = 90
                self.frontwheels.turn(self.steering_angle)
                self.speed = 30
                self.drive()
                zaehler = 0
            else:# Lenkwinkelkorrektur wenn Sensor in der Mitte nicht belegt. 0 = Sensor in Fahrtrichtung Links aussen 1,2,..., 4 = Sensor in Fahrtrichtung rechts aussen.
                if INf_daten[1] == 1:
                    if self.steering_angle != 70:
                        doku = "ja" 
                    self.steering_angle = 70
                    self.frontwheels.turn(self.steering_angle)
                    zaehler = 0
                elif INf_daten[3] == 1:
                    if self.steering_angle != 110:
                        doku = "ja"
                    self.steering_angle = 110
                    self.frontwheels.turn(self.steering_angle)
                    zaehler = 0
                elif INf_daten[0] == 1:
                    if self.steering_angle != 45:
                        doku = "ja"
                    self.steering_angle = 45
                    self.frontwheels.turn(self.steering_angle)
                    zaehler = 0
                elif INf_daten[4] == 1:
                    if self.steering_angle != 135:
                        doku = "ja"
                    self.steering_angle = 135
                    self.frontwheels.turn(self.steering_angle)
                    zaehler = 0         
                else: # Stopp bei Fahrbahnende wenn 10 Schleifen keiner der 5 Sensor belegt wird.
                    zaehler += 1
                    if zaehler == 10:
                        self.stop()
                        break
                if doku=='ja':
                    self.fahrdaten.append({"Fahrmodus": 3, "Zeit": time.time(), "Richtung": self.direction, "Geschwindigkeit": self.speed, "Lenkwinkel": self.steering_angle, "Entfernung": self.get_distance()})
                    doku = 'nein'
                    print(self.fahrdaten)
    def kalibrieren(self):
        while True:
            print(self.INf.read_analog())
            print(self.INf.read_digital())
            print(self.USo.distance())
            time.sleep(1)
 
#car = SensorCar(0,0,0,[60,70,80,60,40])    
#car.kalibrieren()  
