import json
import os

class save_fahrdaten:
    """
    Eine Klasse zum Speichern von Fahrdaten in einer zentralen JSON-Datei.

    Diese Klasse kümmert sich um das Erstellen des Log-Verzeichnisses,
    das Laden bestehender Daten, das Anhängen neuer Daten und das
    zurückschreiben in die Datei 'fahrtenbuch.json'.
    """

    def __init__(self, fahrdaten): 
        """
        Initialisiert das Speicherobjekt mit den neuen Fahrdaten.

        Args:
            fahrdaten (dict): Ein Dictionary, das die Daten einer einzelnen Fahrt enthält.
        """
        # Der Pfad zum Log-Ordner wird relativ zum aktuellen Skript bestimmt.
        # os.path.dirname(__file__) -> Verzeichnis des Skripts
        # ".." -> eine Ebene höher
        # "logs" -> in den Ordner "logs"       
        self.log_ordner = os.path.join(os.path.dirname(__file__), "..", "logs")
        self.dateiname = os.path.join(self.log_ordner,"fahrtenbuch.json")
        self.fahrdaten = fahrdaten
        # Debug-Ausgabe: Zeigt den finalen Speicherpfad an.
        print(f"Zieldatei: {self.dateiname}")
        
    # Ordner erstellen, falls er noch nicht existiert
    def save(self):
        """
        Speichert die Fahrdaten in der JSON-Datei.

        Liest zuerst die bestehenden Daten aus der Datei, fügt den neuen
        Datensatz hinzu und schreibt dann die gesamte Liste zurück.
        Wenn die Datei oder der Ordner nicht existiert, werden sie erstellt.
        """

        # Sicherstellen, dass der Zielordner existiert.
        if not os.path.exists(self.log_ordner):
            os.makedirs(self.log_ordner)
            print(f"Log-Ordner wurde erstellt: {self.log_ordner}")
        else:
            print(f"Log-Ordner existiert bereits: {self.log_ordner}")
         # Versuchen, die bestehende Datei zu laden, um Daten anzuhängen. 
        try:
            with open(self.dateiname, "r") as datei:
                daten = json.load(datei)
                print("Datei wurde lesend geöffnet!")
        except FileNotFoundError:
            # Falls die Datei nicht existiert, mit einer leeren Liste starten.
            # Dies passiert beim allerersten Speichervorgang.
            daten = []
            print("Keine bestehende Fahrtenbuch-Datei gefunden. Es wird eine neue erstellt.")
        except json.JSONDecodeError:
            # Falls die Datei leer oder beschädigt ist.
            daten = []
            print("Warnung: Fahrtenbuch-Datei war leer oder beschädigt. Sie wird überschrieben.")
        daten.append(self.fahrdaten)        
        # ACHTUNG: Die Datei wird im Schreibmodus ("w") geöffnet, was den gesamten
        # Inhalt überschreibt. Deswegen mussten wir die Daten vorher laden.
        with open(self.dateiname, "w") as datei:
            json.dump(daten, datei, indent=4)
            print("Eintrag gespeichert")


        