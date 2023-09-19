import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import numpy as np
from sympy import symbols, Eq, solve

app = dash.Dash(__name__)

# Agrega estilos CSS personalizados
app.css.append_css({
    'external_url': '/assets/custom.css'  # Ruta a tu archivo custom.css en la carpeta "assets"
})

# Diseño de la aplicación
app.layout = html.Div([
    html.H1("Calculadora de Solución General de Sistemas de Ecuaciones", className="title"),
    html.Div([
        dcc.Textarea(id="input-matrix", placeholder="Ingresa la matriz del sistema (ejemplo: [[2, 3, 4], [1, -1, 2], [3, 2, -1]])", 
                     style={'width': '100%', 'height': 100}),
        html.Button('Calcular Solución', id='calculate-button', n_clicks=0),
    ]),
    html.Div(id='solution-output', className='small-note'),
])

# Lógica de la aplicación
@app.callback(
    Output('solution-output', 'children'),
    [Input('calculate-button', 'n_clicks')],
    [dash.dependencies.State('input-matrix', 'value')]
)
def calcular_solucion(n_clicks, matrix_text):
    if n_clicks > 0:
        try:
            # Parsea la matriz ingresada como una matriz numpy
            matrix = np.array(eval(matrix_text))
            
            # Convierte la matriz a símbolos
            symbols_list = [symbols(f'x{i}') for i in range(len(matrix))]
            
            # Crea un sistema de ecuaciones
            equations = [Eq(np.dot(matrix[i, :], symbols_list), 0) for i in range(len(matrix))]
            
            # Resuelve el sistema de ecuaciones
            solution = solve(equations, symbols_list)
            
            # Formatea la solución como una cadena
            solution_str = ', '.join([f'{symbol} = {value}' for symbol, value in solution.items()])
            
            return f'Solución general: {solution_str}'
        except Exception as e:
            return f'Error al calcular la solución: {str(e)}'

if __name__ == '__main__':
    app.run_server(debug=True)










