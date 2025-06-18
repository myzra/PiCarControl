import dash
from dash import html, dcc, Output, Input, State, ctx
import subprocess
import pandas as pd

# App init
app = dash.Dash(__name__, external_stylesheets=["/assets/styles.css"])

# the py files needs to be adjusted -> currently its acting more as a template for further usecase
script_files = [
    ("Fahrmodus 1", "testing.py"),
    ("Fahrmodus 2", "test2.py"),
    ("Fahrmodus 3", "test3.py"),
    ("Fahrmodus 4", "test4.py"),
    ("Fahrmodus 5", "test5.py"),
    ("Fahrmodus 6", "test6.py"),
    ("Fahrmodus 7", "test7.py"),
]

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
        html.Button(name, id={"type": "script-button", "index": idx}, n_clicks=0, className="run-btn")
        for idx, (name, _) in enumerate(script_files)
    ], className="button-box"),

    html.Div(id="script-output", className="output-box"),
    html.Footer("Project 1 • PiCarControl", className="footer")
])

@app.callback(
    Output("script-output", "children"),
    Input({"type": "script-button", "index": dash.dependencies.ALL}, "n_clicks"),
    prevent_initial_call=True
)
def run_script(n_clicks):
    triggered = ctx.triggered_id
    if triggered is None:
        return "Fehler: Kein Button erkannt."

    idx = triggered["index"]
    script_name = script_files[idx][1]
    script_path = f"software/driving_modes/{script_name}"

    try:
        result = subprocess.check_output(["python3", script_path], stderr=subprocess.STDOUT, text=True)
        return html.Pre(result)
    except subprocess.CalledProcessError as e:
        return html.Pre(f"Fehler beim Ausführen von {script_name}:\n{e.output}")
    except Exception as e:
        return html.Pre(f"Unerwarteter Fehler: {str(e)}")

if __name__ == "__main__":
    app.run_server(debug=True, host="0.0.0.0", port=4200)
