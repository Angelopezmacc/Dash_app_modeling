from math import sqrt
import dash
import dash as dcc
import dash as html
from dash import Dash, html, dcc, Input, Output, State
import numpy as np
from sympy import symbols,Eq

app = dash.Dash(__name__,external_stylesheets=['/assets/custom.css'])
last_clicked= None

# Diseño de la aplicación
app.layout = html.Div([
    html.H1("Calculadora de autovalores", className="title"),
    html.Div([
        dcc.Textarea(id="input-matrix", placeholder="Ingresa la matriz del sistema de 2x2 (ejemplo: [[2,3], [1,-1]])", 
                     style={'width': '100%', 'height': 100}),
        html.Button('Calcular autovalores y Forma Canonica', id='calculate-button', n_clicks=0),
        html.Button('Forma Canonica', id='canonical-button', n_clicks=0),

    ]),
    html.Div(id='output-area', className='small-note')  # Área de salida única
])

# ...

@app.callback(
    Output('output-area', 'children'),  # Actualiza el área de salida única
    [Input('calculate-button', 'n_clicks'), Input('canonical-button', 'n_clicks')],
    [dash.dependencies.State('input-matrix', 'value')]
)
def actualizar_salida(n_clicks_calculate, n_clicks_canonical, matrix_text):
    if n_clicks_calculate > 0:
        try:
           
            # Parsea la matriz ingresada como una matriz numpy
            matrix = np.array(eval(matrix_text))
            
            a = matrix[0,0]
            b = matrix[0,1]
            c = matrix[1,0]
            d = matrix[1,1]

            trM= a+d
            detM = a*d-b*c


            lambda1 = (-1*trM + sqrt(pow(trM,2)-4*detM)) * 0.5
            lambda2 = (-1*trM - sqrt(pow(trM,2)-4*detM)) * 0.5

            equations = html.Div([f'Eigenvalue 1: {lambda1}', html.Br(), f'Eigenvalue 2: {lambda2}'])
            solution = f'Solución general: {lambda1, lambda2}'

            return equations, solution
        except Exception as e:
            return f'Error al calcular la solución: {str(e)}'

    elif n_clicks_canonical > 0:
        try:
             # Parsea la matriz ingresada como una matriz numpy
            matrix = np.array(eval(matrix_text))

            a = matrix[0,0]
            b = matrix[0,1]
            c = matrix[1,0]
            d = matrix[1,1]
            
            x,y= symbols('x y')
            
            ecuacion1 = Eq( a*x+b*y,0)
            ecuacion2 = Eq(c*x+d*y,0)

            ecuacion1_str = str(ecuacion1.lhs)
            ecuacion2_str = str(ecuacion2.lhs)
            return dcc.Markdown(f'Forma Canónica: ${ecuacion1_str}$ , ${ecuacion2_str}$' )
   
        except Exception as e:
            return f'Error al calcular la Forma Canonica: {str(e)}'

    return ''

if __name__ == '__main__':
    app.run_server(debug=True,port=8090)
