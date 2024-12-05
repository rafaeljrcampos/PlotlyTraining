import dash
from dash import dcc, html, Input, Output
import plotly.graph_objs as go
import numpy as np
import random
import pandas as pd
import re
from plotly.subplots import make_subplots

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
                    {"label": "Tabela", "value": "table"},
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
    if np.all(x < 2):
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
        fig = go.Figure(go.Indicator(mode="gauge+number",value= random.uniform(1, max_valor),title={'text': "Indicador"},gauge={'axis': {'range': [0, max_valor]},'bar': {'color': "#ffc547"}, 'threshold' : {'line': {'color': "#FF6347", 'width': 4}, 'thickness': 0.75, 'value':max_valor/2}}))
    elif tipo_grafico =='indicatortwo':
        fig = go.Figure(go.Indicator(mode="number+gauge+delta", gauge={'shape': "bullet", 'axis': {'range': [0, max_valor]}, 'bar': {'color': "#ffc547"}},delta={'reference': 300,'increasing':{'color': "#ffc547"},'decreasing':{'color': "#FF6347"}},value=random.uniform(0, max_valor)))
    elif tipo_grafico == 'table':
        df = pd.read_excel('dataset/RelatorioOrders-Handwerk-2511.xlsx', skiprows=3, sheet_name='Planilha1', decimal=',')
        # Criar a tabela
        df_filtred = df.loc[df['Tipo Venda'] == 'VENDA', ['Cliente (Nome Fantasia)', 'Data Entrega', 'Tipo Venda','R$ Total']]
        df_filtred['Data Entrega'] = pd.to_datetime(df_filtred['Data Entrega']).dt.strftime('%m/%Y')
        df_grouped = df_filtred.groupby('Data Entrega').agg({
            'Cliente (Nome Fantasia)': 'first',  # Mostra a primeira empresa para cada mês
            'Tipo Venda': 'first',  # Mostra o primeiro tipo de venda para cada mês
            'R$ Total': 'sum'  # Soma o R$ Total por mês
        }).reset_index()

        fig = go.Figure(data=[go.Table(
            header=dict(
                values=list(df_grouped.columns),
                fill_color='lightgrey',
                align='left',
                font=dict(size=12)
            ),
            cells=dict(
                values=[df_grouped[col] for col in df_grouped.columns],
                align='left',
                font=dict(size=10),
                height=25,
            )
        )])

    else:
        fig = go.Figure()
    if tipo_grafico == "table":
        fig.update_layout(
            paper_bgcolor="#121212",
            plot_bgcolor="#1e1e1e",
            autosize=True,
            margin=dict(l=20, r=20, t=20, b=20),
            xaxis=dict(
                automargin=True
            ),
        )
    else:
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
