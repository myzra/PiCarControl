from BaseCar import BaseCar
import basisklassen as bk
import time
import threading
import json

class SonicCar(BaseCar):
    def __init__(self, forward_A, forward_B, turning_offset):
        super().__init__(forward_A, forward_B, turning_offset)
        self.fahrdaten = []
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
               
    def fahrmodus4(self):
        """Bedaten der Eigenschaften des Objetkts und Aufruf der Methoden gemäß Lastenheft für Fahrmodus1"""
        dauer = 20  # Sekunden
        startzeit = time.time()
        doku='nein'

        while time.time() - startzeit < dauer:
            print(f"Richtung: {self.direction} Entfernung: {self.get_distance()} Geschwindigkeit:{self.speed} {self.speed_tmp}")
            if self.get_distance() >= 5 or self.get_distance() == -2:
                if self.get_distance() >= 100 and self.speed != 100:
                    self.speed = 100
                    doku='ja'
                elif self.get_distance() < 100 and self.get_distance() >= 80 and self.speed != 80:
                    self.speed = 80
                    doku='ja'
                elif self.get_distance() < 80 and self.get_distance() >= 50 and self.speed != 50:
                    self.speed = 50
                    doku='ja'  
                elif self.get_distance() < 50 and self.get_distance() >= 0  and self.speed != 30:
                    self.speed = 30 
                    doku='ja' 
                             
                self.steering_angle=90
                self.frontwheels.turn(self.steering_angle)
                if doku=='ja':
                    self.fahrdaten.append({"Zeit": time.time(), "Richtung": self.direction, "Geschwindigkeit": self.speed, "Lenkwinkel": self.steering_angle, "Entfernung": self.get_distance()})
                    doku='nein'
                self.drive()

            elif self.get_distance() >= 0 and self.get_distance() <= 5 and self.get_distance() != -2:
                self.stop()
                self.steering_angle=135
                self.frontwheels.turn(self.steering_angle)
                self.speed = -48
                self.fahrdaten.append({"Zeit": time.time(), "Richtung": self.direction, "Geschwindigkeit": self.speed, "Lenkwinkel": self.steering_angle, "Entfernung": self.get_distance()})
                self.drive()
                time.sleep(2.5)
                self.stop()
                self.fahrdaten.append({"Zeit": time.time(), "Richtung": self.direction, "Geschwindigkeit": self.speed, "Lenkwinkel": self.steering_angle, "Entfernung": self.get_distance()})
                
        self.stop()
        dateiname = 'fahrtenbuch.json'
        try:
        # Vorherige Daten laden, falls vorhanden
            with open(dateiname, "r") as datei:
                daten = json.load(datei)
        except FileNotFoundError:
            daten = []

        daten.append(self.fahrdaten)

        # Neue Daten wieder speichern
        with open(dateiname, "w") as datei:
            json.dump(daten, datei, indent=4)
            print("Eintrag gespeichert")
        print(self.fahrdaten)
# Objekt erzeugen und Methode aufrufen

# mein_auto = SonicCar()
# mein_auto.fahrmodus3()
