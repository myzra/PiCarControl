import time
import PiCar as PyQt5
import BaseCar

def main():
    auto = BaseCar()
    auto.speed = 50
    auto.drive('v')
    time.sleep(3)
    auto.stop()
    auto.drive('r')
    time.sleep(3)
    auto.stop()

if __name__ == "__main__":
    main()
