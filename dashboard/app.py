import dash
from dash import html, dcc, Output, Input, State, ctx
import subprocess
import pandas as pd
import sys
import os
import json
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "software")))
from BaseCar import BaseCar
from SonicCar import SonicCar
import json

# Pfad zum Log-Ordner bestimmen
log_ordner = os.path.join(os.path.dirname(__file__), "..", "logs")

try:
    with open(os.path.join(log_ordner,"fahrtenbuch.json"), "r", encoding="utf-8") as file:
        data = json.load(file)
    print("Datei erfolgreich geladen.")
except FileNotFoundError:
    print("Achtung: Die Datei 'fahrtenbuch.json' wurde nicht gefunden.")
    data = []  
except json.JSONDecodeError:
    print("Die Datei ist vorhanden, aber enthält kein gültiges JSON.")
    data = []

print(data[0])
print(data[1][0]["Zeit"])
print(len(data))
#df = pd.json_normalize(data)
# Dann evtl. normalisieren:
df = pd.json_normalize(data)
# App init
app = dash.Dash(__name__, external_stylesheets=["/assets/styles.css"])

with open(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "software", "config.json"))) as f:
    config = json.load(f)
    print(config)

bcar = BaseCar(
    forward_A=config["forward_A"],
    forward_B=config["forward_B"],
    turning_offset=config["turning_offset"]
)
socar = SonicCar(
    forward_A=config["forward_A"],
    forward_B=config["forward_B"],
    turning_offset=config["turning_offset"]    
)

# the py files needs to be adjusted -> currently its acting more as a template for further usecase
modes = [
    ("Fahrmodus 1", "fahrmodus1"),
    ("Fahrmodus 2", "fahrmodus2"),
    ("Fahrmodus 3", "fahrmodus3"),
    ("Fahrmodus 4", "fahrmodus4"),
    ("Fahrmodus 5", "fahrmodus5"),
    ("Fahrmodus 6", "fahrmodus6"),
    ("Fahrmodus 7", "fahrmodus7"),
]
anzahl_fahrten = len(data)  # z. B. Anzahl der Fahrten in deiner Struktur
fahrten = [(f"Fahrt {i+1}", i) for i in range(anzahl_fahrten)]
print(fahrten)
# Worthless test data
data = pd.DataFrame({
    "timestamp": pd.date_range(start="2025-06-17 12:00", periods=6, freq="min"),
    "speed": [12.3, 15.5, 13.2, 17.8, 14.0, 16.7],
    "distance": [0.2, 0.3, 0.25, 0.4, 0.35, 0.3]
})

max_speed = data["speed"].max()
min_speed = data["speed"].min()
avg_speed = data["speed"].mean()
total_distance = data["distance"].sum()
total_duration = data["timestamp"].iloc[-1] - data["timestamp"].iloc[0]

def create_card(title, value, unit):
    return html.Div(className="kpi-card", children=[
        html.H4(title),
        html.P(f"{value:.2f} {unit}")
    ])

# Webui structure-code
app.layout = html.Div(className="container", children=[
    html.H1("PiCarStats Dashboard", className="title"),
    html.P("Not gonna lie, the styles.css is completely generated lol", className="disclaimer"), # for information only, not really needed
    html.Div(className="kpi-container", children=[
    create_card("Maximale Geschwindigkeit", max_speed, "km/h"),
    create_card("Minimale Geschwindigkeit", min_speed, "km/h"),
    create_card("Durchschnittsgeschwindigkeit", avg_speed, "km/h"),
    create_card("Gesamtfahrstrecke", total_distance, "km"),
    create_card("Gesamtfahrzeit", total_duration.total_seconds() / 60, "Minuten"),
    ]),

    html.P("Wähle ein Fahrmodus zum Ausführen:", className="subtitle"),

    html.Div([
        dcc.Dropdown(
            id="modus-auswahl",
            options=[
                {"label": name, "value": method_name}
                for name, method_name in modes
            ],
            placeholder="Fahrmodus auswählen",
            className="dropdown"
        ),
        html.Button("Start", id="start-btn", n_clicks=0, className="run-btn")
    ], className="dropdown-box"),

    html.P("Wähle eine Fahrt um die Daten anzuzeigen!", className="subtitle"),
    html.Div([
        dcc.Dropdown(
            id="fahrt-auswahl",
            options=[
                {"label": name, "value": method_name}
                for name, method_name in fahrten
            ],
            placeholder="Fahrt auswählen",
            className="dropdown"
        ),
        
    ], className="dropdown-box"),

    html.Div(id="script-output", className="output-box"),
    html.Footer("Project 1 • PiCarControl", className="footer")
])

@app.callback(
    Output("script-output", "children"),
    Input("start-btn", "n_clicks"),
    State("modus-auswahl", "value"),
    prevent_initial_call=True
)
def start_driving_mode(n_clicks, fahrmodus):
    if not fahrmodus:
        return html.Pre("⚠️ Kein Fahrmodus ausgewählt.")
    elif fahrmodus == 'fahrmodus1' or fahrmodus == 'fahrmodus2':
        methode = getattr(bcar, fahrmodus)
    elif fahrmodus == 'fahrmodus3' or fahrmodus == 'fahrmodus4': 
        methode = getattr(socar, fahrmodus)
    else:
        #vorbereitet für Sensorcar
        pass  
    try:
        result = methode()
        return html.Pre(str(result))
    except Exception as e:
        return html.Pre(f"Fehler: {str(e)}")

@app.callback(
    Output("script-output", "children1"),
    Input("fahrt-auswahl", "value"),
    prevent_initial_call=True
)
def anzeige_daten(value):
    max_speed = data[0]["Geschwindigkeit"].max()
    min_speed = data[0]["Geschwindigkeit"].min()
    avg_speed = data[0]["Geschwindigkeit"].mean()
    print(max_speed)
    

if __name__ == "__main__":
    app.run_server(debug=True, host="0.0.0.0", port=4200)
