import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import numpy as np
from scipy.linalg import eig
import plotly.express as px

app = dash.Dash(__name__)

# Diseño de la aplicación
app.layout = html.Div([
    html.H1("Clasificador y Espacio de Fase de Sistemas", className="title"),
    html.Div([
        dcc.Textarea(id="input-matrix", placeholder="Ingresa la matriz del sistema (ejemplo: [[2, 1], [1, 2]])", 
                     style={'width': '100%', 'height': 100}),
        html.Button('Procesar Sistema', id='process-button', n_clicks=0),
    ]),
    html.Div(id='classification-result', className='small-note'),
    dcc.Graph(id='phase-space-plot')
])

# Función para calcular la clasificación del sistema
def clasificar_sistema(matrix):
    try:
        # Calcular los valores propios de la matriz
        eigenvalues, eigenvectors = eig(matrix)

        # Clasificar el sistema en función de los valores propios
        if all(np.real(eigenvalues) < 0):
            return "El sistema es estable."
        elif all(np.real(eigenvalues) > 0):
            return "El sistema es inestable."
        else:
            return "El sistema es un punto de silla."
    except Exception as e:
        return f'Error al clasificar el sistema: {str(e)}'

# Lógica de la aplicación
@app.callback(
    [Output('classification-result', 'children'), Output('phase-space-plot', 'figure')],
    [Input('process-button', 'n_clicks')],
    [dash.dependencies.State('input-matrix', 'value')]
)
def procesar_sistema(n_clicks, matrix_text):
    if n_clicks > 0:
        try:
            # Parsea la matriz ingresada como una matriz numpy
            matrix = np.array(eval(matrix_text))
            
            # Calcula la clasificación del sistema
            classification_result = clasificar_sistema(matrix)
            
            # Calcula el espacio de fase del sistema
            eigenvalues, eigenvectors = eig(matrix)
            x, y = eigenvectors[:, 0].real, eigenvectors[:, 1].real  # Usamos los vectores propios correspondientes a los valores propios reales
            
            # Crea el gráfico de espacio de fase
            fig = px.scatter(x=[0], y=[0], title="Espacio de Fase", labels={'x': 'Eje X', 'y': 'Eje Y'})
            fig.add_scatter(x=x, y=y, mode='markers', text=classification_result, 
                            marker=dict(size=10, color='blue'), name='Puntos de Equilibrio')
            
            return f"Clasificación del sistema: {classification_result}", fig
        except Exception as e:
            return f'Error al procesar el sistema: {str(e)}', None
    return '', None

if __name__ == '__main__':
    app.run_server(debug=True)
