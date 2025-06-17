import basisklassen
import time

class BaseCar:
    def __init__(self):
        """Initialisiert die Eigenschaften und erzeugt Objekte der Klasse Backwheels und Frontwheels."""
        self.steering_angle = 0
        self.speed = 0
        self.direction = 0
        self.back_wheels = basisklassen.BackWheels()
        self.frontwheel = basisklassen.FrontWheels()

    def drive(self):
        """Lässte das Auto anhand der Variable speed entweder vorwärts oder rückwärts fahren"""
        if self.speed > 0:
                self.back_wheels.speed = self.speed
                print("Das Auto fährt vorwärts...")
                self.back_wheels.forward()
        if self.speed < 0:
                self.speed= self.speed *-1
                self.back_wheels.speed = self.speed
                print("Das Auto fährt rückwärts...")
                self.back_wheels.backward()
                  
      

    def stop(self):
        """Stoppt das Auto."""
        self.back_wheels.stop()
        print("Das Auto wurde gestoppt.")

    def fahrmodus1(self):
        """Bedaten der Eigenschaften des Objetkts und Aufruf der Methoden gemäß Lastenheft für Fahrmodus1"""
        self.frontwheel.turn(90)
        self.speed = 30
        self.drive()
        time.sleep(3)
        self.speed = -30
        self.drive()
        time.sleep(3)
        self.stop()

    def fahrmodus2(self):
        """Bedaten der Eigenschaften des Objetkts und Aufruf der Methoden gemäß Lastenheft für Fahrmodus2"""
        self.frontwheel.turn(90)
        self.speed = 30
        self.drive()
        time.sleep(1)
        self.frontwheel.turn(135)
        self.speed = 30
        time.sleep(8)
        self.stop() 
        time.sleep(2)
        self.speed = -40
        self.frontwheel.turn(135)
        self.drive()
        time.sleep(8)
        self.stop() 
        time.sleep(2)
        self.frontwheel.turn(90)
        self.speed = -40
        self.drive()
        time.sleep(1)
        self.stop()    

# Eine Instanz von BaseCar erstellen und die Methoden aufrufen






