import dash
from dash import dcc, html, Input, Output
import plotly.graph_objs as go
import numpy as np
import random

# Inicializa o aplicativo
app = dash.Dash(__name__)
app.title = "Plotly Training"

# Layout do aplicativo
app.layout = html.Div(
    style={"display": "flex", "flex-direction": "row", "height": "100vh"},
    children=[
        # Menu lateral
        html.Div(
            style={
                "width": "20%",
                "padding": "20px",
                "background-color": "#1e1e1e",
                "border-right": "1px solid #333",
            },
            children=[
                html.H2("Menu de Controle", style={"text-align": "center"}),
                html.Label("Escolha o Gráfico:", style={"margin-bottom": "10px"}),
            dcc.Dropdown(
                id="grafico-dropdown",
                options=[
                    {"label": "Linha", "value": "line"},
                    {"label": "Barra", "value": "bar"},
                    {"label": "Dispersão", "value": "scatter"},
                    {"label": "Indicador", "value": "indicator"},
                    {"label": "Segundo Indicador", "value": "indicatortwo"},

                ],
                value="line",
                className="dash-dropdown",
                style={
                    "backgroundColor": "white",  
                },
            ),


                html.Br(),
                html.Label("Ajuste o Valor Máximo Aleatório:"),
                dcc.Slider(
                    id="valor-slider",
                    min=10,
                    max=1000,
                    value=50,
                    className="dash-slider",
                ),
            ],
        ),
        # Área do gráfico
        html.Div(
            style={"flex-grow": "1", "padding": "20px"},
            children=[
                html.Div(
                    id="grafico-container",
                    className="graph-container",
                    children=[dcc.Graph(id="grafico")],
                )
            ],
        ),
    ],
)

# Função para atualizar o gráfico
@app.callback(
    Output("grafico", "figure"),
    [Input("grafico-dropdown", "value"), Input("valor-slider", "value")],
)
def atualizar_grafico(tipo_grafico, max_valor):
    # Dados aleatórios
    x = np.arange(1, random.randint(1, max_valor))
    y = np.random.randint(1, max_valor, random.randint(1, max_valor))

    # Seleção do tipo de gráfico
    if tipo_grafico == "line":
        fig = go.Figure(data=go.Scatter(x=x, y=y, mode="lines", line=dict(color="#ffc547")))
    elif tipo_grafico == "bar":
        fig = go.Figure(data=go.Bar(x=x, y=y, marker=dict(color="#ffc547")))
    elif tipo_grafico == "scatter":
        fig = go.Figure(data=go.Scatter(x=x, y=y, mode="markers", marker=dict(color="#ffc547", size=10)))
    elif tipo_grafico =='indicator':
        fig = go.Figure(go.Indicator(mode="gauge+number",value= random.uniform(1, max_valor),title={'text': "Indicador"},gauge={'axis': {'range': [0, max_valor]},'bar': {'color': "#ffc547"}}))
    elif tipo_grafico =='indicatortwo':
        fig = go.Figure(go.Indicator(mode="number+gauge+delta", gauge={'shape': "bullet", 'axis': {'range': [0, max_valor]}, 'bar': {'color': "#ffc547"}},delta={'reference': 300,'increasing':{'color': "#ffc547"},'decreasing':{'color': "#FF6347"}},value=random.uniform(0, max_valor)))
    else:
        fig = go.Figure()

    # Configuração de tema escuro
    fig.update_layout(
        paper_bgcolor="#121212",
        plot_bgcolor="#1e1e1e",
        font_color="#ffffff",
        title="Gráfico Dinâmico",
        xaxis=dict(title="Eixo X"),
        yaxis=dict(title="Eixo Y"),
    )
    return fig


# Executa o servidor
if __name__ == "__main__":
    app.run_server(debug=True)
