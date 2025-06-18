import basisklassen
import time

class BaseCar:
    def __init__(self, forward_A, forward_B, turning_offset ):
        """Initialisiert die Eigenschaften und erzeugt Objekte der Klasse Backwheels und Frontwheels."""
        #self.steering_angle = 0
        self.speed_tmp = 0
        #self.direction = 0
        self.back_wheels = basisklassen.BackWheels(forward_A, forward_B)
        self.frontwheels = basisklassen.FrontWheels(turning_offset)

    @property
    def direction(self):
        if self.speed_tmp < 0:
            return -1
        elif self.speed_tmp > 0:
            return 1
        else:
            return 0
        
    @property
    def steering_angle(self):
        return self.frontwheels.get_angles()

    @steering_angle.setter
    def steering_angle(self, value):
        if value < 45:
            self.frontwheels._angles = 45
        elif value > 135:
            self.frontwheels._angles = 135
        else:
            self.frontwheels._angles = value

    @property
    def speed(self):
        return self.back_wheels.speed

    @speed.setter
    def speed(self, value):
        if value < -100:
            self.speed_tmp = -100
            self.back_wheels.speed = 100
        elif value > 100:
            self.back_wheels.speed = 100
            self.speed_tmp = 100
        else:
            self.back_wheels.speed = abs(value)        
            self.speed_tmp = value
    def drive(self):
        """Lässte das Auto anhand der Variable speed entweder vorwärts oder rückwärts fahren"""
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
        """Bedaten der Eigenschaften des Objetkts und Aufruf der Methoden gemäß Lastenheft für Fahrmodus1"""
        self.frontwheels.turn(90)
        self.speed = 30
        self.drive()
        time.sleep(3)
        self.speed = -30
        self.drive()
        time.sleep(3)
        self.stop()

    def fahrmodus2(self):
        """Bedaten der Eigenschaften des Objetkts und Aufruf der Methoden gemäß Lastenheft für Fahrmodus2"""
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

# Eine Instanz von BaseCar erstellen und die Methoden aufrufen






