# Importar las bibliotecas necesarias
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import numpy as np

# Crear una instancia de la aplicación Dash
app = dash.Dash(__name__)

# Definir el diseño de la aplicación
app.layout = html.Div([
    html.H1("Ingresar una Matriz"),  # Encabezado de la página
    dcc.Input(id="num_rows", type="number", placeholder="Número de filas"),  # Campo de entrada para el número de filas
    dcc.Input(id="num_cols", type="number", placeholder="Número de columnas"),  # Campo de entrada para el número de columnas
    html.Button("Ingresar Matriz", id="submit-button"),  # Botón para ingresar la matriz
    dcc.Input(id="matrix-input", type="text", placeholder="Ingrese la matriz (fila por fila)"),  # Campo de entrada para la matriz
    html.Div(id="matrix-output")  # Div para mostrar la salida de la matriz
])

# Definir una función de callback para actualizar la salida de la matriz
@app.callback(
    Output("matrix-output", "children"),
    Input("submit-button", "n_clicks"),
    Input("num_rows", "value"),
    Input("num_cols", "value"),
    Input("matrix-input", "value"),
)
def update_matrix(n_clicks, num_rows, num_cols, matrix_str):
    if n_clicks is None:
        return ""  # No mostrar nada si no se ha hecho clic en el botón

    try:
        # Convertir la cadena de entrada en una matriz NumPy de números flotantes
        matrix = np.array(matrix_str.split()).astype(float).reshape(num_rows, num_cols)
        return f"Matriz ingresada:\n{matrix}"  # Mostrar la matriz ingresada
    except Exception as e:
        return "Error al procesar la matriz. Asegúrese de que los valores sean números válidos y coincidan con las dimensiones especificadas."

# Ejecutar la aplicación si este archivo es el punto de entrada
if __name__ == "__main__":
    app.run_server(debug=True, port=8070)  # Ejecutar la aplicación en modo de depuración en el puerto 8060
