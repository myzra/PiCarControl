import dash
from dash import html, dcc, Output, Input, State, ctx
import subprocess
import pandas as pd
import sys
import os
import json
import plotly.express as px
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "software")))
from BaseCar import BaseCar
from SonicCar import SonicCar
import json

# Pfad zum Log-Ordner bestimmen
log_ordner = os.path.join(os.path.dirname(__file__), "..", "logs")

try:
    with open(os.path.join(log_ordner,"fahrtenbuch.json"), "r", encoding="utf-8") as file:
        logdata = json.load(file)
    print("Datei erfolgreich geladen.")
except FileNotFoundError:
    print("Achtung: Die Datei 'fahrtenbuch.json' wurde nicht gefunden.")
    logdata = []  
except json.JSONDecodeError:
    print("Die Datei ist vorhanden, aber enthält kein gültiges JSON.")
    logdata = []



# Dann evtl. normalisieren:
df = pd.json_normalize(logdata)
# App init
app = dash.Dash(__name__, external_stylesheets=["/assets/styles.css"])

with open(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "software", "config.json"))) as f:
    config = json.load(f)
    
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
anzahl_fahrten = len(logdata)  # z. B. Anzahl der Fahrten in deiner Struktur
fahrten = [(f"Fahrt {i+1}", i) for i in range(anzahl_fahrten)]

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

def create_card(card_id, title, value, unit):
    return html.Div(className="kpi-card", children=[
        html.H4(title),
        html.P(id=card_id, children=f"{value:.2f} {unit}")
    ])

# Webui structure-code
app.layout = html.Div(className="container", children=[
    html.H1("PiCarStats Dashboard", className="title"),
    html.P("Not gonna lie, the styles.css is completely generated lol", className="disclaimer"), # for information only, not really needed
    html.Div(className="kpi-container", children=[
    create_card("kpi-max-speed","Maximale Geschwindigkeit", max_speed, "km/h"),
    create_card("kpi-min-speed","Minimale Geschwindigkeit", min_speed, "km/h"),
    create_card("kpi-avg-speed","Durchschnittsgeschwindigkeit", avg_speed, "km/h"),
    create_card("kpi-total-distance","Gesamtfahrstrecke", total_distance, "km"),
    create_card("kpi-total-duration","Gesamtfahrzeit", total_duration.total_seconds() / 60, "Minuten"),
   
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
    html.Div(className="graph-container", children=[dcc.Graph(id="fahrt-graph")]),
    html.Div(id="script-output", className="output-box"),
    html.Footer("Project 1 • PiCarControl", className="footer"),
     
])
    
@app.callback(
    Output("script-output", "children"),
    Input("start-btn", "n_clicks"),
    State("modus-auswahl", "value"),
    prevent_initial_call=True
)
def start_driving_mode(n_clicks, fahrmodus):
    if not fahrmodus:
        return html.Pre("Kein Fahrmodus ausgewählt.")
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
    Output("kpi-max-speed", "children"),
    Output("kpi-avg-speed", "children"),
    Output("kpi-min-speed", "children"),
    Input("fahrt-auswahl", "value"),
    prevent_initial_call=False 
)
def update_dashboard_data(selected_fahrt_id): 
    if selected_fahrt_id == None:
        return (
        f"--- km/h",
        f"--- km/h",
        f"--- km/h"
        )
    else:
        df=pd.DataFrame(logdata[selected_fahrt_id]) 
        print(df["Geschwindigkeit"].mean())
        print(df)
        max_speed = df["Geschwindigkeit"].max()
        min_speed = df["Geschwindigkeit"].min()
        avg_speed = df["Geschwindigkeit"].mean()
        
        return (
        f"{max_speed:.2f} km/h",
        f"{avg_speed:.2f} km/h",
        f"{min_speed:.2f} km/h"
        )
@app.callback(
    Output("fahrt-graph", "figure"),
    Input("fahrt-auswahl", "value"),
    prevent_initial_call=False
)
def update_graph(selected_fahrt_id):
    """
    Erstellt und aktualisiert den Graphen basierend auf der ausgewählten Fahrt.
    """
    # Standard-Graph für den Fall, dass keine Daten angezeigt werden können
    # if selected_fahrt_id == None:
    #     selected_fahrt_id = 0
        
    try:
        df=pd.DataFrame(logdata[selected_fahrt_id])
    except:
        print("keine Auswahl getroffen")
    empty_fig = px.line(template="plotly_dark").update_layout(
        paper_bgcolor='rgba(0,0,0,0)', 
        plot_bgcolor='rgba(25,28,32,0.8)'
    )

    if selected_fahrt_id is None:
        empty_fig.update_layout(title_text="Bitte eine Fahrt zur Analyse auswählen")
        return empty_fig

    

    if df.empty:
        empty_fig.update_layout(title_text=f"Fahrt {selected_fahrt_id + 1} enthält keine Daten")
        return empty_fig

    # Graph-Erstellung
    df_gefiltert = df.melt(id_vars=['Zeit'], value_vars=['Geschwindigkeit'], var_name='Metrik', value_name='Wert')
    fig = px.line(
        df_gefiltert, 
        x='Zeit', 
        y='Wert', 
        color='Metrik', 
        title=f"Datenanalyse für Fahrt {selected_fahrt_id + 1}", 
        template="plotly_dark"
    )
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)', 
        plot_bgcolor='rgba(25,28,32,0.8)',
        legend_title_text='Messgröße'
    )
    return fig    

if __name__ == "__main__":
    app.run_server(debug=True, host="0.0.0.0", port=4200)
