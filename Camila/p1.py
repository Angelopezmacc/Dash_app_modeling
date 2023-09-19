import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import numpy as np

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Ingresar una Matriz"),
    dcc.Input(id="num_rows", type="number", placeholder="Número de filas"),
    dcc.Input(id="num_cols", type="number", placeholder="Número de columnas"),
    html.Button("Ingresar Matriz", id="submit-button"),
    dcc.Input(id="matrix-input", type="text", placeholder="Ingrese la matriz (fila por fila)"),
    html.Div(id="matrix-output")
])

@app.callback(
    Output("matrix-output", "children"),
    Input("submit-button", "n_clicks"),
    Input("num_rows", "value"),
    Input("num_cols", "value"),
    Input("matrix-input", "value"),
)
def update_matrix(n_clicks, num_rows, num_cols, matrix_str):
    if n_clicks is None:
        return ""
    
    try:
        matrix = np.array(matrix_str.split()).astype(float).reshape(num_rows, num_cols)
        return f"Matriz ingresada:\n{matrix}"
    except Exception as e:
        return "Error al procesar la matriz. Asegúrese de que los valores sean números válidos y coincidan con las dimensiones especificadas."

if __name__ == "__main__":
    app.run_server(debug=True, port=8060)

