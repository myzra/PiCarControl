# Importiere die Basisklasse, Sensor- und Speicherfunktionen
from BaseCar import BaseCar
import basisklassen as bk
import time
import json
import os
from save import save_fahrdaten

# Erweiterte Klasse für autonomes Fahren mit Ultraschallsensor
class SonicCar(BaseCar):
    def __init__(self, forward_A, forward_B, turning_offset):
        super().__init__(forward_A, forward_B, turning_offset)
        self.fahrdaten = []                     # Hier werden Messwerte während der Fahrt gespeichert
        self.USo = bk.Ultrasonic()              # Objekt für Ultraschallsensor wird erstellt
        self.distance = 0                       # Anfangswert für die gemessene Distanz
        self.frontwheels = bk.FrontWheels()     # Frontlenkung wird initialisiert

    # Gibt die gemessene Entfernung in cm zurück
    def get_distance(self):
        self.distance = self.USo.distance()
        return self.distance

    # Einfacher Fahrmodus: Fahre vorwärts, bis Hindernis erkannt wird
    def fahrmodus3(self):
        while True:
            print(f"Abstand: {self.get_distance()}")
            # Wenn genug Abstand oder Sensorfehler (-2, -4), fahre geradeaus
            if self.get_distance() >= 5 or self.get_distance() in [-2, -4]:
                self.frontwheels.turn(90)  # Geradeaus lenken
                self.speed = 30            # Geschwindigkeit setzen
                self.drive()               # Vorwärts fahren
            # Bei Hindernis stoppen und Schleife verlassen
            elif 0 <= self.get_distance() <= 5:
                self.stop()
                break
        return "Fahrmodus 3 beendet"

    # Dynamischer Fahrmodus: Geschwindigkeit je nach Abstand anpassen, mit Rückwärts-Ausweichmanöver
    def fahrmodus4(self):
        dauer = 20                        # Dauer des Fahrmodus in Sekunden
        startzeit = time.time()
        doku = 'nein'                     # Steuerung für Datenaufzeichnung

        while time.time() - startzeit < dauer:
            print(f"Richtung: {self.direction} Entfernung: {self.get_distance()} Geschwindigkeit:{self.speed} ")

            # Wenn ausreichend Abstand oder kein Hindernis erkennbar
            if self.get_distance() >= 5 or self.get_distance() == -2:
                # Geschwindigkeit je nach Entfernung dynamisch anpassen
                if self.get_distance() >= 100 and self.speed != 100:
                    self.speed = 100; doku = 'ja'
                elif 80 <= self.get_distance() < 100 and self.speed != 80:
                    self.speed = 80; doku = 'ja'
                elif 50 <= self.get_distance() < 80 and self.speed != 50:
                    self.speed = 50; doku = 'ja'
                elif 0 <= self.get_distance() < 50 and self.speed != 30:
                    self.speed = 30; doku = 'ja'

                self.steering_angle = 90                # Geradeaus lenken
                self.frontwheels.turn(self.steering_angle)

                # Wenn Parameter geändert wurden, speichere aktuellen Zustand
                if doku == 'ja':
                    self.fahrdaten.append({
                        "Fahrmodus": 4,
                        "Zeit": time.time(),
                        "Richtung": self.direction,
                        "Geschwindigkeit": self.speed,
                        "Lenkwinkel": self.steering_angle,
                        "Entfernung": self.get_distance()
                    })
                    doku = 'nein'

                self.drive()

            # Hindernis erkannt → Rückwärts fahren und speichern
            elif 0 <= self.get_distance() <= 5 and self.get_distance() != -2:
                self.stop()
                self.steering_angle = 135              # Voll nach rechts lenken
                self.frontwheels.turn(self.steering_angle)
                self.speed = -48                       # Rückwärtsgeschwindigkeit
                self.fahrdaten.append({
                    "Fahrmodus": 4,
                    "Zeit": time.time(),
                    "Richtung": self.direction,
                    "Geschwindigkeit": self.speed,
                    "Lenkwinkel": self.steering_angle,
                    "Entfernung": self.get_distance()
                })
                self.drive()
                time.sleep(2.5)                        # 2,5 Sekunden zurücksetzen
                self.stop()

                # Zustand nach Rückwärtsfahrt speichern
                self.fahrdaten.append({
                    "Fahrmodus": 4,
                    "Zeit": time.time(),
                    "Richtung": self.direction,
                    "Geschwindigkeit": self.speed,
                    "Lenkwinkel": self.steering_angle,
                    "Entfernung": self.get_distance()
                })

        self.stop()
        speichern = save_fahrdaten(self.fahrdaten)     # Messdaten abspeichern
        speichern.save()
        return "Fahrmodus 4 beendet"

car = SonicCar(0,0,0,)
car.fahrmodus4()
