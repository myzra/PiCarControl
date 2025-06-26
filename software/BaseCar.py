import basisklassen
import time

class BaseCar:
    """
    Diese Klasse abstrahiert die Steuerung (definiert in 
    'basisklassen') und bietet einfache Methoden zum Fahren, Lenken, Stoppen
    sowie vordefinierte Fahrmodi.
    """

    MIN_LENKWINKEL = 45   # Limit für den Lenkeinschlag links
    MAX_LENKWINKEL = 135  # Limit für den Lenkeinschlag rechts
    MITTELSTELLUNG = 90   # Servo-Position für Geradeausfahrt
    
    MIN_GESCHWINDIGKEIT = -100 # max Geschwindigkeit rückwärts
    MAX_GESCHWINDIGKEIT = 100 # max Geschwindigkeit vorwärts

    def __init__(self, forward_A, forward_B, turning_offset ):
        """
        Initialisiert das Auto und die zugehörigen Hardware-Komponenten.

        Args:
            forward_A (int): Offset Ansteuerung Motor A.
            forward_B (int): Offset Ansteuerung Motor B.
            turning_offset (int): Kalibrierungswert für die Lenkung, um eine exakte 
                                  Geradeausfahrt zu gewährleisten.
        """
        self._speed_tmp = 0
        self.lenkwinkel = 0
        self.back_wheels = basisklassen.BackWheels(forward_A, forward_B)
        self.frontwheels = basisklassen.FrontWheels(turning_offset)

    @property
    def direction(self):
        """
        Gibt die aktuelle Fahrtrichtung basierend auf der Geschwindigkeit zurück.

        Returns:
            int: 1 für vorwärts, -1 für rückwärts, 0 für Stillstand.
        """
        if self._speed_tmp < 0:
            return -1
        elif self._speed_tmp > 0:
            return 1
        else:
            return 0                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   
        
    @property
    def steering_angle(self):
        """Lesezugriff auf den aktuellen Lenkwinkel."""
        return self.lenkwinkel

    @steering_angle.setter
    def steering_angle(self, value):
        """
        Setzt den Lenkwinkel und begrenzt ihn auf die definierten Min/Max-Werte.
        """
        if value < self.MIN_LENKWINKEL:
            self.lenkwinkel = self.MIN_LENKWINKEL
        elif value > self.MAX_LENKWINKEL:
            self.lenkwinkel = self.MAX_LENKWINKEL
        else:
            self.lenkwinkel = value

    @property
    def speed(self):
        """Lesezugriff auf die aktuell eingestellte Geschwindigkeit"""
        return self.back_wheels.speed

    @speed.setter
    def speed(self, value):
        """
        Setzt die Geschwindigkeit des Autos.

        Nimmt einen Wert von -100 (rückwärts) bis 100 (vorwärts) entgegen.
        Der Funktion zum Setzen der Geschwindigkeit (back_wheels) benötigt einen absoluten
        Speed-Wert (0-100), während anhand der _speed_tmp die Richtung erechnet wird.
        """
        if value < self.MIN_GESCHWINDIGKEIT:
            self._speed_tmp = self.MIN_GESCHWINDIGKEIT
            self.back_wheels.speed = self.MAX_GESCHWINDIGKEIT
        elif value > self.MAX_GESCHWINDIGKEIT:
            self.back_wheels.speed = self.MAX_GESCHWINDIGKEIT
            self._speed_tmp = self.MAX_GESCHWINDIGKEIT
        else:
            self.back_wheels.speed = abs(value)        
            self._speed_tmp = value
    def drive(self):
        """
        Aktiviert die Motoren entsprechend der gesetzten Geschwindigkeit und Richtung.
        """
        if self.direction == 1:
            print("Das Auto fährt vorwärts...")
            self.back_wheels.forward()
        if self.direction == -1:
            self.back_wheels.speed = abs(self.speed)
            print("Das Auto fährt rückwärts...")
            self.back_wheels.backward()
        if self.direction == 0:
            print("Keine Richtung/Geschwindigkeit angegben.")
    
    def stop(self):
        """Stoppt das Auto."""
        self.back_wheels.stop()
        print("Das Auto wurde gestoppt.")

    def fahrmodus1(self):
        """
        Führt eine einfache Fahrt aus: 3s vor, 3s zurück.

        Returns:
            str: Eine Nachricht über die Beendigung des Modus.
        """
        #Bedaten der Eigenschaften des Objetkts und Aufruf der Methoden gemäß Lastenheft für Fahrmodus1
        self.frontwheels.turn(90)
        self.speed = 30
        self.drive()
        time.sleep(3)
        self.speed = -30
        self.drive()
        time.sleep(3)
        self.stop()
        return "Fahrmodus1 beendet"

    def fahrmodus2(self):
        """
        Führt eine komplexere Fahrsequenz mit Lenkmanövern und Richtungsänderung durch.
        
         Returns:
            str: Eine Nachricht über die Beendigung des Modus.
        """
        #Bedaten der Eigenschaften des Objetkts und Aufruf der Methoden gemäß Lastenheft für Fahrmodus2"""
        self.frontwheels.turn(90)
        self.speed = 30
        self.drive()
        time.sleep(1)
        self.frontwheels.turn(135)
        self.speed = 30
        time.sleep(8)
        self.stop() 
        time.sleep(2)
        self.speed = -40
        self.frontwheels.turn(135)
        self.drive()
        time.sleep(8)
        self.stop() 
        time.sleep(2)
        self.frontwheels.turn(90)
        self.speed = -40
        self.drive()
        time.sleep(1)
        self.stop() 
        self.frontwheels.turn(90)
        self.speed = 30
        self.drive()
        time.sleep(1)
        self.frontwheels.turn(45)
        self.speed = 30
        time.sleep(8)
        self.stop() 
        time.sleep(2)
        self.speed = -40
        self.frontwheels.turn(45)
        self.drive()
        time.sleep(8)
        self.stop() 
        time.sleep(2)
        self.frontwheels.turn(90)
        self.speed = -40
        self.drive()
        time.sleep(1)
        self.stop() 
        return "Fahrmodus2 beendet"      








