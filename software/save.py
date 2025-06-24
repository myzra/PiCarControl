import json
import os

class save_fahrdaten:
    def __init__(self, fahrdaten):        
        self.log_ordner = os.path.join(os.path.dirname(__file__), "..", "logs")
        self.dateiname = os.path.join(log_ordner,"fahrtenbuch.json")
        print(self.dateiname)
    # Ordner erstellen, falls er noch nicht existiert
    def save(self):
        if not os.path.exists(log_ordner):
            os.makedirs(log_ordner)
            print(f"Log-Ordner wurde erstellt: {log_ordner}")
        else:
            print(f"Log-Ordner existiert bereits: {log_ordner}")
            
        try:
            # Vorherige Daten laden, falls vorhanden
            with open(dateiname, "r") as datei:
                daten = json.load(datei)
        except FileNotFoundError:
            daten = []

        daten.append(self.fahrdaten)

        # Neue Daten wieder speichern
        with open(dateiname, "w") as datei:
            json.dump(daten, datei, indent=4)
            print("Eintrag gespeichert")
        print(self.fahrdaten)