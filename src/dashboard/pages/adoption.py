from dash import html, dcc
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
from src.dashboard.styles import COLORS, CARD_STYLE

layout = dbc.Container([
    html.H2("Program Adoption & ROI", className="mb-4"),
    
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Adoption Curve"),
                dbc.CardBody(
                    dcc.Graph(
                        figure=go.Figure(
                            data=[
                                go.Scatter(y=[5, 12, 25, 45, 60, 75, 82, 88], mode='lines+markers', fill='tozeroy', name='Adoption %', line=dict(color=COLORS['secondary']))
                            ],
                            layout=dict(title="Tool Adoption Rate (Weeks)", template="plotly_white")
                        )
                    )
                )
            ], style=CARD_STYLE)
        ], width=12, lg=8),
        
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("ROI Calculator"),
                dbc.CardBody([
                    html.H4("Total Savings: $12,450", className="text-success mb-3"),
                    html.P("Based on 83 hours saved @ $150/hr"),
                    html.Hr(),
                    html.H6("Top Savers:"),
                    html.Ul([
                        html.Li("Report Automation: $4,500"),
                        html.Li("Doc Retrieval: $3,200"),
                        html.Li("Triage Bot: $2,100")
                    ])
                ])
            ], style=CARD_STYLE)
        ], width=12, lg=4)
    ])
], fluid=True)
