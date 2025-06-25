import json
import os

class save_fahrdaten:
    def __init__(self, fahrdaten):        
        self.log_ordner = os.path.join(os.path.dirname(__file__), "..", "logs")
        self.dateiname = os.path.join(self.log_ordner,"fahrtenbuch.json")
        self.fahrdaten = fahrdaten
        print(self.dateiname)
    # Ordner erstellen, falls er noch nicht existiert
    def save(self):
        if not os.path.exists(self.log_ordner):
            os.makedirs(self.log_ordner)
            print(f"Log-Ordner wurde erstellt: {self.log_ordner}")
        else:
            print(f"Log-Ordner existiert bereits: {self.log_ordner}")
         
        try:
            # Vorherige Daten laden, falls vorhanden
            with open(self.dateiname, "r") as datei:
                daten = json.load(datei)
                print("Datei wurde lesend geöffnet!")
        except FileNotFoundError:
            daten = []
            print("Datei konnte nicht geöffnet werden!")
        daten.append(self.fahrdaten)
        print(daten)
        
        # Neue Daten wieder speichern
        with open(self.dateiname, "w") as datei:
            print(daten)
            json.dump(daten, datei, indent=4)
            print("Eintrag gespeichert")
        print(self.fahrdaten)