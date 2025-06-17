import basisklassen
import time

class BaseCar:
    def __init__(self):
        """Initialisiert die Eigenschaften und die Hinterräder."""
        self.steering_angle = 0
        self.speed = 0
        self.direction = 0
        self.back_wheels = basisklassen.BackWheels()

    def drive(self,richtung,lenkwinkel=0):
        """Lässt das Auto für eine bestimmte Zeit fahren."""
        self.back_wheels.speed = self.speed
        print(self.speed)
        if richtung == 'v':
                print("Das Auto fährt vorwärts...")
                self.back_wheels.forward()
        if richtung == 'r':
                print("Das Auto fährt rückwärts...")
                self.back_wheels.backward()
                  
      

    def stop(self):
        """Stoppt das Auto."""
        self.back_wheels.stop()
        print("Das Auto wurde gestoppt.")

# Eine Instanz von BaseCar erstellen und die Methoden aufrufen
auto = BaseCar()
auto.speed = 50
auto.drive('v')
time.sleep(3)
auto.stop()
auto.drive('r')
time.sleep(3)
auto.stop()

