import basisklassen
import time

class BaseCar:
    def __init__(self, forward_A, forward_B, turning_offset ):
        """Initialisiert die Eigenschaften und erzeugt Objekte der Klasse Backwheels und Frontwheels."""
        #self.steering_angle = 0
        self.speed_tmp = 0
        self.lenkwinkel = 0
        self.back_wheels = basisklassen.BackWheels(forward_A, forward_B)
        self.frontwheels = basisklassen.FrontWheels(turning_offset)
        self.stop_requested = False  # Add stop flag


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
        return self.lenkwinkel

    @steering_angle.setter
    def steering_angle(self, value):
        if value < 45:
            self.lenkwinkel = 45
        elif value > 135:
            self.lenkwinkel = 135
        else:
            self.lenkwinkel = value

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

    def interruptible_sleep(self, duration):
        """Sleep that can be interrupted by stop request"""
        sleep_interval = 0.1  # Check every 100ms
        elapsed = 0
        while elapsed < duration:
            if self.check_stop():
                return True  # Stop was requested
            time.sleep(min(sleep_interval, duration - elapsed))
            elapsed += sleep_interval
        return False  # Completed normally

    def fahrmodus1(self):
        """Bedaten der Eigenschaften des Objetkts und Aufruf der Methoden gemäß Lastenheft für Fahrmodus1"""
        self.stop_requested = False
        self.frontwheels.turn(90)
        self.speed = 30
        self.drive()

        if self.interruptible_sleep(3):
            return "Fahrmodus 1 gestoppt"        
        
        self.speed = -30
        self.drive()

        if self.interruptible_sleep(3):
            return "Fahrmodus 1 gestoppt"        
        self.stop()
        return "Fahrmodus 1 beendet"

    def fahrmodus2(self):
        """Bedaten der Eigenschaften des Objetkts und Aufruf der Methoden gemäß Lastenheft für Fahrmodus2"""
        self.stop_requested = False  # Reset stop flag
        
        self.frontwheels.turn(90)
        self.speed = 30
        self.drive()
        if self.interruptible_sleep(1):
            return "Fahrmodus 2 gestoppt"
            
        self.frontwheels.turn(135)
        self.speed = 30
        if self.interruptible_sleep(8):
            return "Fahrmodus 2 gestoppt"
            
        self.stop()
        if self.interruptible_sleep(2):
            return "Fahrmodus 2 gestoppt"

        self.speed = -40
        self.frontwheels.turn(135)
        self.drive()
        if self.interruptible_sleep(8):
            return "Fahrmodus 2 gestoppt"
            
        self.stop()
        if self.interruptible_sleep(2):
            return "Fahrmodus 2 gestoppt"

        self.frontwheels.turn(90)
        self.speed = -40
        self.drive()
        if self.interruptible_sleep(1):
            return "Fahrmodus 2 gestoppt"
            
        self.stop()

        self.frontwheels.turn(90)
        self.speed = 30
        self.drive()
        if self.interruptible_sleep(1):
            return "Fahrmodus 2 gestoppt"
            
        self.frontwheels.turn(45)
        self.speed = 30
        if self.interruptible_sleep(8):
            return "Fahrmodus 2 gestoppt"
            
        self.stop()
        if self.interruptible_sleep(2):
            return "Fahrmodus 2 gestoppt"

        self.speed = -40
        self.frontwheels.turn(45)
        self.drive()
        if self.interruptible_sleep(8):
            return "Fahrmodus 2 gestoppt"
            
        self.stop()
        if self.interruptible_sleep(2):
            return "Fahrmodus 2 gestoppt"

        self.frontwheels.turn(90)
        self.speed = -40
        self.drive()
        if self.interruptible_sleep(1):
            return "Fahrmodus 2 gestoppt"
            
        self.stop()
        return "Fahrmodus 2 beendet"  

    def request_stop(self):
        """Method to request stopping from external source"""
        self.stop_requested = True

    def check_stop(self):
        """Check if stop was requested and handle it"""
        if self.stop_requested:
            self.stop()
            self.stop_requested = False
            return True
        return False
