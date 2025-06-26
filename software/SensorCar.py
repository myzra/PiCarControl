from BaseCar import BaseCar
import basisklassen as bk
import time
import json
import os
from save import save_fahrdaten

class SensorCar(BaseCar):
    def __init__(self, forward_A, forward_B, turning_offset, INf_offset):
        super().__init__(forward_A, forward_B, turning_offset)
        self.USo = bk.Ultrasonic()
        self.distance = 0
        self.INf = bk.Infrared(INf_offset)
        self.fahrdaten = []

    def fahrmodus(self, funktionserweiterung=0): #Funktion für Fahrmodus, Funktionserweiterung=1 --> für "scharfe" Kurven mit rücksetzen. Funktionserweiterung=2 --> "scharfe" Kurven + integration Ultraschallsensor.
        sensor = 99
        drive_korrektur = 99
        doku = "nein"
        zaehler = 0 #Wird benötigt wenn Fahrzeug zwischen dem Sensor steht --> Weiterfahrt zwischen IR-Sensor.
        while True:
            if funktionserweiterung == 2:
                if 0< self.USo.distance() < 5:
                    self.stop()
                    break
            #print(self.INf.read_digital())
            print(self.INf.read_analog())
            print(self.INf.read_digital())
            print(self.USo.distance())
            #time.sleep(1)

            INf_daten = self.INf.read_digital() # Liste mit IR-Werte Sensor 1-5
            if INf_daten[2] == 1 and INf_daten[0] == 0 and INf_daten[1] == 0 and INf_daten[3] == 0 and INf_daten[4] == 0: # 2 = Sensor in der Mitte --> Abfrage belegt.
                sensor = 2
                if self.steering_angle != 90:
                    doku = "ja"
                self.steering_angle = 90
                self.frontwheels.turn(self.steering_angle)
                self.speed = 30
                self.drive()
                zaehler = 0
            else:# Lenkwinkelkorrektur wenn Sensor in der Mitte nicht belegt. 0 = Sensor in Fahrtrichtung Links aussen 1,2,..., 4 = Sensor in Fahrtrichtung rechts aussen.
                if INf_daten[1] == 1:
                    sensor = 1
                    if self.steering_angle != 70:
                        doku = "ja" 
                    self.steering_angle = 70
                    self.frontwheels.turn(self.steering_angle)
                    zaehler = 0
                elif INf_daten[3] == 1:
                    sensor = 3
                    if self.steering_angle != 110:
                        doku = "ja"
                    self.steering_angle = 110
                    self.frontwheels.turn(self.steering_angle)
                    zaehler = 0
                elif INf_daten[0] == 1:
                    sensor = 0
                    if self.steering_angle != 45:
                        doku = "ja"
                    self.steering_angle = 45
                    self.frontwheels.turn(self.steering_angle)
                    zaehler = 0
                elif INf_daten[4] == 1:
                    sensor = 4
                    if self.steering_angle != 135:
                        doku = "ja"
                    self.steering_angle = 135
                    self.frontwheels.turn(self.steering_angle)
                    zaehler = 0         
                else: # Stopp bei Fahrbahnende wenn 20 Schleifen keiner der 5 Sensor belegt wird.
                    zaehler += 1
                    if zaehler == 10:
                        if sensor == 0 or sensor == 1:
                            self.steering_angle = 100
                        if sensor == 3 or sensor == 4:
                            self.steering_angle = 80
                        print("korrektur ausgefuehrt")    
                    if zaehler == 20:
                        if sensor == 2:
                            self.stop()
                            break
                        else:
                            if funktionserweiterung > 0:
                                self.stop()
                                while True:
                                    INf_daten = self.INf.read_digital()
                                    if sensor == 0 or sensor == 1:
                                        drive_korrektur = 4
                                        print("sensor 0 und 1")
                                        self.steering_angle = 135
                                    if sensor == 3 or sensor == 4:
                                        drive_korrektur = 0
                                        print("sensor 3 und 4")
                                        self.steering_angle = 45
                                    self.frontwheels.turn(self.steering_angle)
                                    self.speed = -30
                                    print(sensor)
                                    print(INf_daten)
                                    self.drive()
                                    if INf_daten[drive_korrektur] == 1:
                                        self.speed = 0
                                        self.stop()
                                        if sensor == 0 or sensor == 1:
                                            print("sensor 0 und 1")
                                            self.steering_angle = 45
                                        if sensor == 3 or sensor == 4:
                                            print("sensor 3 und 4")
                                            self.steering_angle = 135
                                        self.speed = 30
                                        self.drive()
                                        break
                if doku=='ja':
                    liste = self.INf.read_digital()
                    for i in range(len(liste)):
                        liste[i] = int(liste[i])
                    print(liste)
                    print(type(liste))
                    print(type(liste[0]))
                    try:
                        
                        self.fahrdaten.append({"Fahrmodus": 6, "Zeit": time.time(), "Richtung": self.direction,"Geschwindigkeit": self.speed, "Lenkwinkel": self.steering_angle,"Entfernung": self.USo.distance(), "IR-Sensor": liste})
                        
                    except Exception as e:
                        print(f"Konnte nicht gespeichert werden: {e}")
                    doku = 'nein'
                    print(self.fahrdaten)
        speichern = save_fahrdaten(self.fahrdaten)   
        speichern.save()
    def fahrmodus5(self): #Funktion für Fahrmodus 5.
        self.fahrmodus()
        return "Fahrmodus 5 beendet"
    def fahrmodus6(self): #Funktion für Fahrmodus 6.
        self.fahrmodus(1)
        return "Fahrmodus 6 beendet"
    def fahrmodus7(self): #Funktion für Fahrmodus 7.
        self.fahrmodus(2)
        return "Fahrmodus 7 beendet"

class Kalibrieren():
    def __init__(self):
        self.Dateipfad = os.path.abspath(os.path.join(os.path.dirname(__file__),"config.json"))
        pass
    
    def config_einlesen(self):
        with open(self.Dateipfad, "r") as f:
            config = json.load(f)
        return config
    
    def config_speichern(self,config,INf_offset):
        print(type(INf_offset))
        config["sensor_werte"] = INf_offset
        with open(self.Dateipfad, "w") as datei:
            json.dump(config, datei, indent=4)
            print("Offset Infrarot-Sensor gespeichert!")

    def string_zu_int_liste(self, wert):
        neuer_offset = wert
        neuer_offset1 = neuer_offset.split(',')
        neuer_offset = [int(item) for item in neuer_offset1]
        return neuer_offset


    def kalibrieren(self, INf_offset = [0,0,0,0,0]):
        print(INf_offset)
        INf = bk.Infrared(INf_offset)
        i = 0
        while i < 6:
            print(INf.read_analog())
            print(INf.read_digital())
            time.sleep(1)
            i += 1

# sensor_calib = Kalibrieren()
# config = sensor_calib.config_einlesen()
# config_offset = config["sensor_werte"]
# sensor_calib.kalibrieren(config_offset)
# neuer_offset = sensor_calib.string_zu_int_liste(input("Bitte den Offset im Format 0,0,0,0,0 eingeben:"))
# sensor_calib.config_speichern(config, neuer_offset)