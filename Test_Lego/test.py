import tkinter as tk
from tkinter import ttk
import basisklassen
import BaseCar as BC
import time


input
auto = BC.BaseCar()

print("Bitte wählen Sie einen Fahrmodus:")
print("1 - Fahrmodus 1")
print("2 - Fahrmodus 2")

wahl = input("Ihre Auswahl: ")
if wahl == '1':
    auto.fahrmodus1()
if wahl == '2':
    auto.fahrmodus2()
"""
# Fenster erstellen
root = tk.Tk()
root.title("PiCar-Steuerung")2

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
