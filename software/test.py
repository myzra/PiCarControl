import tkinter as tk
from tkinter import ttk
import basisklassen
import BaseCar as BC
import SonicCar as SC
import time
import json
forward_A = 0
forward_B = 0
turning_offset = 0

try:
    with open("config.json", "r") as f:
        data = json.load(f)
        turning_offset = data["turning_offset"]
        forward_A = data["forward_A"]
        forward_B = data["forward_B"]
        print("Daten in config.json:")
        print(" - Turning Offset: ", turning_offset)
        print(" - Forward A: ", forward_A)
        print(" - Forward B: ", forward_B)
except:
    print("Keine geeignete Datei config.json gefunden!")
else:
    print("Test der Vorderräder:")

print(forward_A, forward_B, turning_offset)

auto = BC.BaseCar(forward_A, forward_B, turning_offset)
auto2 = SC.SonicCar(forward_A, forward_B, turning_offset)

print("Bitte wählen Sie einen Fahrmodus:")
print("1 - Fahrmodus 1")
print("2 - Fahrmodus 2")
print("3 - Fahrmodus 3")
print("4 - Fahrmodus 4")
#Eingabe wird in Varible wahl gespeichert
wahl = input("Ihre Auswahl: ")
#Vergleich welcher Fahrmodus gewählt wurde
if wahl == '1':
    auto.fahrmodus1()
if wahl == '2':
    auto.fahrmodus2()
if wahl == '3':
    auto2.fahrmodus3()
if wahl == '4':
    auto2.fahrmodus4()
