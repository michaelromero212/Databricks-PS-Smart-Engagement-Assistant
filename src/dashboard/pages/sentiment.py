from dash import html, dcc
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
from src.dashboard.styles import COLORS, CARD_STYLE

def create_gauge(value, title):
    return go.Figure(go.Indicator(
        mode = "gauge+number",
        value = value,
        title = {'text': title},
        gauge = {
            'axis': {'range': [None, 100]},
            'bar': {'color': COLORS['primary']},
            'steps': [
                {'range': [0, 50], 'color': "#f9f9f9"},
                {'range': [50, 80], 'color': "#e6e6e6"},
                {'range': [80, 100], 'color': "#d9d9d9"}
            ]
        }
    ))

layout = dbc.Container([
    html.H2("Sentiment Analysis", className="mb-4"),
    
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Overall Sentiment Score"),
                dbc.CardBody(
                    dcc.Graph(
                        figure=create_gauge(78, "Positive Sentiment %"),
                        style={"height": "300px"}
                    )
                )
            ], style=CARD_STYLE)
        ], width=12, md=6),
        
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Sentiment by Project"),
                dbc.CardBody(
                    dcc.Graph(
                        figure=go.Figure(
                            data=[
                                go.Bar(x=["Alpha", "Beta", "Gamma", "Delta"], y=[85, 62, 45, 90], marker_color=[COLORS['success'], COLORS['warning'], COLORS['danger'], COLORS['success']])
                            ],
                            layout=dict(title="Project Sentiment Health", template="plotly_white")
                        )
                    )
                )
            ], style=CARD_STYLE)
        ], width=12, md=6)
    ]),
    
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Sentiment Timeline"),
                dbc.CardBody(
                    dcc.Graph(
                        figure=go.Figure(
                            data=[
                                go.Scatter(y=[70, 72, 68, 65, 60, 55, 58, 62, 65, 70, 75, 78], mode='lines', name='Sentiment', line=dict(color=COLORS['primary'], width=3))
                            ],
                            layout=dict(title="30-Day Sentiment Trend", template="plotly_white")
                        )
                    )
                )
            ], style=CARD_STYLE)
        ], width=12)
    ])
], fluid=True)
