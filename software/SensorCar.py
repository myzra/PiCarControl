from BaseCar import BaseCar
import basisklassen as bk
import time
import json
import os
import pandas as pd
from save import save_fahrdaten

class SensorCar(BaseCar): # Klasse Sensor Car mit Vererbung aus Base Car um auf den Infrarot- und Ultraschallsensor zugreifen zu können.
    def __init__(self, forward_A, forward_B, turning_offset, INf_offset):
        super().__init__(forward_A, forward_B, turning_offset)
        self.USo = bk.Ultrasonic()
        self.distance = 0
        self.INf = bk.Infrared(INf_offset)
        self.fahrdaten = []
        self.debug=[]
        self.runde = 0
        self.timeout = 0
        self.merker = 0

    def fahrmodus(self, funktionserweiterung=0): #Funktion für Fahrmodus, Funktionserweiterung=1 --> für "scharfe" Kurven mit rücksetzen. Funktionserweiterung=2 --> "scharfe" Kurven + integration Ultraschallsensor.
        sensor = 99 # Wird benötigt für das Rücksetzen. Merker für aktuellen Lenkwinkel.
        drive_korrektur = 99 # Wird benötigt für Stop aus der Mitte. Merker für eingestellten Lenkwinkel.
        doku = "nein" # Wird benötigt zur Dokumentation. Doku "ja" speichert die Werte über save.py in den log.json. Doku "nein" speichert den Wert nicht.
        zaehler = 0 # Wird benötigt wenn Fahrzeug zwischen dem Sensor steht --> Weiterfahrt zwischen IR-Sensor, leichte Lenkkorrektur bei Zähler 10 und stop bei Zähler 20.
        if self.INf.read_digital() == [0,0,0,0,0]:
            print(f"Bitte Startposition einnehmen und Funktion erneut starten. Startposition: [1,1,1,1,1] aktuelle Position: {self.INf.read_digital()}")
            return f"Bitte Startposition einnehmen und Funktion erneut starten. Startposition: [1,1,1,1,1] aktuelle Position: {self.INf.read_digital()}"
        else:
            while True:
                if funktionserweiterung == 2: # Funktion stop bei aktivierten Ultraschallsensor --> Abstand zum Hinternis kleiner 5 cm.
                    if 0< self.USo.distance() < 5:
                        self.stop()
                        break
                #print(self.INf.read_digital())
                print(self.INf.read_analog())
                print(self.INf.read_digital())
                print(self.USo.distance())
                
                #time.sleep(1)
                INf_daten_analog= self.INf.read_analog()
                INf_daten = self.INf.read_digital() # Liste mit IR-Werte Sensor 1-5
                if INf_daten == [1,1,1,1,1]:
                    self.merker = 1
                    if self.runde == 0:
                        self.steering_angle = 90
                        self.frontwheels.turn(self.steering_angle)
                        self.speed = 40
                        self.drive()
                        zaehler = 0
                        
              
                        
                elif INf_daten[2] == 1 and INf_daten[0] == 0 and INf_daten[1] == 0 and INf_daten[3] == 0 and INf_daten[4] == 0: # 2 = Sensor in der Mitte --> Abfrage belegt.
                    #if INf_daten == [0,0,1,0,0]:
                    sensor = 2 
                    if self.steering_angle != 90:
                        doku = "ja"
                    self.steering_angle = 90
                    self.frontwheels.turn(self.steering_angle)
                    self.speed = 40
                    self.drive()
                    zaehler = 0
                    if self.merker == 1:
                        self.runde +=1
                        self.merker = 0
                else:# Lenkwinkelkorrektur wenn Sensor in der Mitte nicht belegt. 0 = Sensor in Fahrtrichtung Links aussen 1,2,..., 4 = Sensor in Fahrtrichtung rechts aussen.
                    if self.merker == 1:
                        self.runde +=1
                        self.merker = 0
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
                    else: 
                        zaehler += 1
                        if zaehler == 10: # Fahrbahnkorrektur wenn bei 10 Schleifen keiner der 5 Sensor belegt wird.
                            if sensor == 0 or sensor == 1:
                                self.steering_angle = 100
                            if sensor == 3 or sensor == 4:
                                self.steering_angle = 80
                            print("korrektur ausgefuehrt")    
                        if zaehler == 20: # Stopp bei Fahrbahnende wenn 20 Schleifen keiner der 5 Sensor belegt wird.
                            if sensor == 2:
                                self.stop()
                                break
                            else:
                                if funktionserweiterung > 0: # Rücksetzen und Fahrtkorrektur bei verlassen der Fahrbahn aufgrund enger kurven.
                                    self.stop()
                                    startzeit = time.time()
                                    while True:
                                        verstrichene_zeit = time.time() - startzeit
                                        print(verstrichene_zeit)
                                        if verstrichene_zeit > 5:
                                            print("Rückwärtsfahrt nach 5 sekunden abgebrochen")
                                            self.timeout= 1
                                            break
                                        INf_daten = self.INf.read_digital()
                                                                        
                                        if sensor == 0 or sensor == 1:
                                            drive_korrektur = 4
                                            print("sensor 0 und 1")
                                            self.steering_angle = 135
                                        elif sensor == 3 or sensor == 4:
                                            drive_korrektur = 0
                                            print("sensor 3 und 4")
                                            self.steering_angle = 45
                                        else:
                                            drive_korrektur = 2
                                            self.steering_angle = 90
                                        self.frontwheels.turn(self.steering_angle)
                                        self.speed = -30
                                        print(sensor)
                                        print(INf_daten)
                                        self.drive()
                                        if INf_daten[drive_korrektur] == 1:
                                            richtung = 'V'
                                        else:
                                            richtung = 'R'
                                        self.debug.append([INf_daten,self.INf.read_analog(), sensor, drive_korrektur, richtung])
                                        if INf_daten[drive_korrektur] == 1:
                                            self.speed = 0
                                            self.stop()
                                            if sensor == 0 or sensor == 1:
                                                print("sensor 0 und 1")
                                                self.steering_angle = 45
                                            if sensor == 3 or sensor == 4:
                                                print("sensor 3 und 4")
                                                self.steering_angle = 135
                                            self.speed = 40
                                            self.drive()
                                            break
                                    print(self.timeout)
                                    if self.timeout == 1:
                                        break        
                    self.debug.append([INf_daten, self.INf.read_analog(), sensor, 111, "V"])
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
                        #print(self.fahrdaten)
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
    def __del__(self):
        self.stop()
        print()

class Kalibrieren(): # Funktion zum Kalibrieren der Sensoren über das Dashboard.
    def __init__(self):
        self.Dateipfad = os.path.abspath(os.path.join(os.path.dirname(__file__),"config.json"))
        pass
    
    def config_einlesen(self):
        with open(self.Dateipfad, "r") as f:
            config = json.load(f)
        return config
    
    def config_speichern(self,config,INf_offset):
        """Mit dieser Funktion können neue offset Werte eingetragen werden.
        Es wird überprüft, ob die Werte kleiner als 301 sind. Zudem wird geprüft, ob es sich bei der Eingabe um ganze Zahlen handelt."""
        for i, val in enumerate(INf_offset):
            if not isinstance(val, int):
                raise ValueError(f"Die Eingabe an Position {i+1} ist keine ganze Zahl, gültige Werte sind 1 bis 300")
            if val > 301:
                raise ValueError(f"Die Eingabe {val} an Position {i+1} ist zu groß, gültige Werte sind 1 bis 300")
            if val < 1:
                raise ValueError(f"Die Eingabe {val} an Position {i+1} ist zu klein, gültige Werte sind 1 bis 300")
        print(type(INf_offset))
        config["sensor_werte"] = INf_offset
        with open(self.Dateipfad, "w") as datei:
            json.dump(config, datei, indent=4)
            print("Offset Infrarot-Sensor gespeichert!")

    def kalibrieren(self, INf_offset = [0,0,0,0,0]):
        print(INf_offset)
        INf = bk.Infrared(INf_offset)
        out = []
        for _ in range(100):
            out.append((INf.read_analog()))
            out.append((INf.read_digital()))
            time.sleep(1)
            print(INf.read_analog())
            print(INf.read_digital())
        return out
    
    


if __name__ == "__main__":
    sensor_calib = Kalibrieren()
    config = sensor_calib.config_einlesen()
    config_offset = config["sensor_werte"]
    car = SensorCar(0,0,0,config_offset)
    
    try:
        car.fahrmodus7()
    except Exception as e:
        car.stop()
        print(f"Skriptabbruch durch Fehler {e}")
    spalten = ['sensor_digital','sensor_analog', 'letzter erkannte sensor', 'Korrektur', 'Richtung']
    df = pd.DataFrame(car.debug, columns=spalten)
    pd.set_option('display.max_rows', None)
    print (df)
    print(f"Anzahl Runden: {car.runde}")

    #sensor_calib.kalibrieren(config_offset)
    # neuer_offset = sensor_calib.string_zu_int_liste(input("Bitte den Offset im Format 0,0,0,0,0 eingeben:"))
    # sensor_calib.config_speichern(config, neuer_offset)