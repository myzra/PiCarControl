import dash
from dash import html, dcc, Output, Input, State, ctx
import threading
import pandas as pd
import sys
import os
import json
import plotly.express as px
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "software")))
from BaseCar import BaseCar # type: ignore
from SonicCar import SonicCar # type: ignore
from SensorCar import SensorCar, Kalibrieren # type: ignore
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

# stop flag
stop_driving = False
current_driving_thread = None

# Dann evtl. normalisieren:
df = pd.json_normalize(logdata)

# App init
app = dash.Dash(__name__, external_stylesheets=["/assets/styles.css"], suppress_callback_exceptions=True)

with open(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "software", "config.json"))) as f:
    config = json.load(f)

# created car instances   
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
secar = SensorCar(
    forward_A=config["forward_A"],
    forward_B=config["forward_B"],
    turning_offset=config["turning_offset"],
    INf_offset=config["sensor_werte"]
)

# list for dashboard dropdown menu providing both visual text and backend method 
modes = [
    ("Fahrmodus 1", "fahrmodus1"),
    ("Fahrmodus 2", "fahrmodus2"),
    ("Fahrmodus 3", "fahrmodus3"),
    ("Fahrmodus 4", "fahrmodus4"),
    ("Fahrmodus 5", "fahrmodus5"),
    ("Fahrmodus 6", "fahrmodus6"),
    ("Fahrmodus 7", "fahrmodus7"),
]

# dict for dahsboard driving mode preview
fahrmodus_beschreibungen = {
    "fahrmodus1": "Fahrmodus 1: Einfaches Vorwärtsfahren für Testzwecke.",
    "fahrmodus2": "Fahrmodus 2: Hinderniserkennung mit einfachem Stopp.",
    "fahrmodus3": "Fahrmodus 3: Linienverfolgung mit Infrarotsensoren.",
    "fahrmodus4": "Fahrmodus 4: Ultraschallsensoren für Abstandsmessung.",
    "fahrmodus5": "Fahrmodus 5: Erweiterte Linienverfolgung mit Kurvenerkennung.",
    "fahrmodus6": "Fahrmodus 6: Hindernisumfahrung im Parcoursmodus.",
    "fahrmodus7": "Fahrmodus 7: Vollautomatisierter Fahrmodus mit Logging.",
}

anzahl_fahrten = len(logdata)  # z. B. Anzahl der Fahrten in deiner Struktur
print(f"Anzahl der Fahrten: {anzahl_fahrten}")
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

# creating kpi-cards
def create_card(card_id, title, value, unit):
    return html.Div(className="kpi-card", children=[
        html.H4(title),
        html.P(id=card_id, children=f"{value:.2f} {unit}")
    ])

# Webui structure-code
app.layout = html.Div(className="container", children=[
    html.H1("PiCarStats Dashboard", className="title"),
    html.P("Not gonna lie, the styles.css is almost completely generated lol", className="disclaimer"), # for information only, not really needed
    html.Div(className="kpi-container", children=[
    create_card("kpi-max-speed","Maximale Geschwindigkeit", max_speed, "km/h"),
    create_card("kpi-min-speed","Minimale Geschwindigkeit", min_speed, "km/h"),
    create_card("kpi-avg-speed","Durchschnittliche Geschwindigkeit", avg_speed, "km/h"),
    create_card("kpi-total-distance","Gesamtfahrstrecke", total_distance, "km"),
    create_card("kpi-total-duration","Gesamtfahrzeit", total_duration.total_seconds() / 60, "Minuten"),
   
    ]),

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
        html.Div([
            html.Button("Start", id="start-btn", n_clicks=0, className="run-btn"),
            html.Button("Stop", id="stop-btn", n_clicks=0, className="stop-btn", style={"margin-left": "10px"}),
        ], style={"display": "flex"}),
        html.Div(id="fahrmodus-info", className="info-box")
    ], className="dropdown-box"),
    html.Div(id="script-output", className="output-box"),
    html.Button("Kalibrieren", id="kalibrieren-btn", n_clicks=0),

    html.Div(id="offset-input", style={"margin-top": "20px"}),
    html.Footer("Project 1 • PiCarControl", className="footer"),
     
])

"""function to calibrate the config.json"""
@app.callback(
    Output("script-output", "children", allow_duplicate=True),
    Output("offset-input", "children"),
    Input("kalibrieren-btn", "n_clicks"),
    prevent_initial_call=True
)
def calibrate(n_clicks):
    c = Kalibrieren()
    config = c.config_einlesen()
    print("test")
    out = c.kalibrieren(config["sensor_werte"])

    output_fields = html.Div([
        html.Label("Neuer Offset (jeweils eine Zahl):"),
        html.Div([
            dcc.Input(id=f"offset-{i}", type="number", style={"margin-right": "5px"}) for i in range(5)
        ]),
        html.Button("Speichern", id="save-offset-btn", n_clicks=0, style={"margin-top": "10px"})
    ])
    formatted = "\n".join(str(zeile) for zeile in out)
    return html.Pre(f"Kalibrierung abgeschlossen:\n{formatted}"), output_fields

"""Function to save the users input offset into config file"""
@app.callback(
    Output("script-output", "children", allow_duplicate=True),
    Output("offset-input", "children", allow_duplicate=True),
    Input("save-offset-btn", "n_clicks"),
    State("offset-0", "value"),
    State("offset-1", "value"),
    State("offset-2", "value"),
    State("offset-3", "value"),
    State("offset-4", "value"),
    prevent_initial_call=True
)
def save_offset(n_clicks, o0, o1, o2, o3, o4):
    if n_clicks < 1:
        raise dash.exceptions.PreventUpdate

    new_off = [o0, o1, o2, o3, o4]
    c = Kalibrieren()
    old_config = c.config_einlesen()
    c.config_speichern(old_config, new_off)

    return f'Neuer Offset gespeichert: {new_off}', html.Div()

"""function to update the dropdown driving mode preview info"""
@app.callback(
    Output("fahrmodus-info", "children"),
    Input("modus-auswahl", "value"),
    prevent_inital_call=False
)
def update_fahrmodus_info(selected_fahrmodus):
    if not selected_fahrmodus:
        return "Bitte einen Fahrmodus auswählen, um mehr Informationen zu erhalten."
    beschreibung = fahrmodus_beschreibungen.get(
        selected_fahrmodus, "Für diesen Fahrmodus liegt keine Beschreibung vor."
    )
    return beschreibung

"""Function that triggers the appropriate method of the corresponding class based on the dropdown menu selection"""
@app.callback(
    Output("script-output", "children", allow_duplicate=True),
    Input("start-btn", "n_clicks"),
    Input("stop-btn", "n_clicks"),
    State("modus-auswahl", "value"),
    prevent_initial_call=True
)
def handle_driving_control(start_clicks, stop_clicks, fahrmodus):
    global current_driving_thread, stop_driving
    
    if ctx.triggered_id == "stop-btn":
        stop_driving = True
        bcar.request_stop()
        socar.request_stop()
        secar.request_stop()
        return html.Pre("Stop-Signal gesendet...")
    
    elif ctx.triggered_id == "start-btn":
        if not fahrmodus:
            return html.Pre("Kein Fahrmodus ausgewählt.")
        
        stop_driving = False
        
        # Determine which car instance to use
        if fahrmodus == 'fahrmodus1' or fahrmodus == 'fahrmodus2':
            car_instance = bcar
        elif fahrmodus == 'fahrmodus3' or fahrmodus == 'fahrmodus4':
            car_instance = socar
        else:
            car_instance = secar
        
        try:
            methode = getattr(car_instance, fahrmodus)
            
            def run_driving_mode():
                try:
                    result = methode()
                    return result
                except Exception as e:
                    return f"Fehler: {str(e)}"
            
            current_driving_thread = threading.Thread(target=run_driving_mode)
            current_driving_thread.start()
            
            return html.Pre(f"{fahrmodus} gestartet...")
            
        except Exception as e:
            return html.Pre(f"Fehler: {str(e)}")
    
    return html.Pre("Unbekannte Aktion.")

"""Stops the current executed driving mode"""
@app.callback(
    Output("stop-btn", "children"),
    Input("stop-btn", "n_clicks"),
    prevent_initial_call=True
)
def stop_driving_mode(n_clicks):
    global stop_driving
    stop_driving = True
    return "Stop"

"""Resets the flag"""
@app.callback(
    Output("start-btn", "children"),
    Input("start-btn", "n_clicks"),
    prevent_initial_call=True
)
def reset_stop_flag(n_clicks):
    global stop_driving
    stop_driving = False
    return "Start"

"""Updates the KPI cards based on the selected trip from the logbook"""
@app.callback(
    Output("kpi-max-speed", "children"),
    Output("kpi-avg-speed", "children"),
    Output("kpi-min-speed", "children"),
    Output("kpi-total-duration", "children"),
    Output("kpi-total-distance", "children"),
    Input("fahrt-auswahl", "value"),
    prevent_initial_call=False 
)
def update_dashboard_data(selected_fahrt_id): 
    if selected_fahrt_id == None:
        return (
        f"--- cm/s",
        f"--- cm/s",
        f"--- cm/s",
        f"--- sec.",
        f"--- cm"
        )
    else:
        print(logdata)
        df=pd.DataFrame(logdata[selected_fahrt_id]) 
        print(df["Geschwindigkeit"].mean())
        print(df)
        max_speed = df["Geschwindigkeit"].max()
        min_speed = df["Geschwindigkeit"].min()
        avg_speed = df["Geschwindigkeit"].mean()
        total_duration = df['Zeit'].max()-df['Zeit'].min()
        total_distance = total_duration * avg_speed
        return (
        f"{max_speed:.2f} cm/s",
        f"{avg_speed:.2f} cm/s",
        f"{min_speed:.2f} cm/s",
        f"{total_duration:.2f} sec.",
        f"{total_distance:.2f} cm"
        )

"""Creates and updates the graph based on the selected trip. Default graph to display when no data is available"""
@app.callback(
    Output("fahrt-graph", "figure"),
    Input("fahrt-auswahl", "value"),
    prevent_initial_call=False
)
def update_graph(selected_fahrt_id):
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
