# this is not functional, only here for testing to run the python codes via dash webui, added by fabian z.
# i gonna delete this after we got the driving mode functions here
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

#from software.BaseCar import BaseCar as BC
import BaseCar as BC
import SonicCar as SC
import basisklassen
import time

forward_A = 0
forward_B = 0
turning_offset = 0

auto = BC.BaseCar(forward_A, forward_B, turning_offset)
auto.fahrmodus1()