import tkinter as tk
from tkinter import ttk
import basisklassen
import BaseCar as BC
import time

auto = BC.BaseCar()
def fahrmodus1():
    auto.frontwheel.turn(90)
    auto.speed = 30
    auto.drive()
    time.sleep(3)
    auto.speed = -30
    auto.drive()
    time.sleep(3)
    auto.stop()

def fahrmodus2():
    auto.frontwheel.turn(90)
    auto.speed = 30
    auto.drive()
    time.sleep(1)
    auto.frontwheel.turn(135)
    auto.speed = 30
    time.sleep(8)
    auto.speed = -40
    auto.drive()
    time.sleep(8)
    auto.frontwheel.turn(90)
    auto.speed = -40
    auto.drive()
    time.sleep(1)
    auto.stop()

fahrmodus2()
"""
# Fenster erstellen
root = tk.Tk()
root.title("PiCar-Steuerung")

# Eingabefelder
ttk.Label(root, text="Geschwindigkeit:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
geschw_entry = ttk.Entry(root, width=15)
geschw_entry.grid(row=0, column=1, padx=5, pady=5)

ttk.Label(root, text="Richtung:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
richtung_entry = ttk.Entry(root, width=15)
richtung_entry.grid(row=1, column=1, padx=5, pady=5)

ttk.Label(root, text="Lenkwinkel:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
lenk_entry = ttk.Entry(root, width=15)
lenk_entry.grid(row=2, column=1, padx=5, pady=5)

# Buttons
los_button = ttk.Button(root, text="Los", command=los)
los_button.grid(row=3, column=0, padx=5, pady=10)

stop_button = ttk.Button(root, text="Stop", command=stop)
stop_button.grid(row=3, column=1, padx=5, pady=10)

root.mainloop()"""
