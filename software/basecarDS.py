import os
import json
from basisklassen import BackWheels, FrontWheels

# Sichere Pfadbestimmung zur config.json (egal von wo das Script aufgerufen wird)
base_path = os.path.dirname(os.path.abspath(__file__))
config_path = os.path.join(base_path, "../config.json")

try:
    with open(config_path, "r") as f:
        config = json.load(f)
except Exception as e:
    print("⚠️ Fehler beim Laden der config.json:", e)
    config = {"forward_A": 0, "forward_B": 0, "turning_offset": 0}


class BaseCar:
    def __init__(self):
        self.front_wheels = FrontWheels(turning_offset=config["turning_offset"])
        self.back_wheels = BackWheels(forward_A=config["forward_A"], forward_B=config["forward_B"])
        self._speed = 0
        self._steering_angle = 90  # Geradeaus

    @property
    def speed(self):
        return self._speed

    @speed.setter
    def speed(self, value):
        value = max(-100, min(100, int(value)))
        self._speed = value

        if value > 0:
            self.back_wheels.speed = value
            self.back_wheels.forward()
        elif value < 0:
            self.back_wheels.speed = -value
            self.back_wheels.backward()
        else:
            self.back_wheels.stop()

    @property
    def steering_angle(self):
        return self._steering_angle

    @steering_angle.setter
    def steering_angle(self, angle):
        angle = max(45, min(135, int(angle)))
        self._steering_angle = angle
        self.front_wheels.turn(angle)

    @property
    def direction(self):
        if self._speed > 0:
            return 1
        elif self._speed < 0:
            return -1
        return 0

    def drive(self, speed=None, angle=None):
        if speed is not None:
            self.speed = speed
        if angle is not None:
            self.steering_angle = angle

    def stop(self):
        self.speed = 0
