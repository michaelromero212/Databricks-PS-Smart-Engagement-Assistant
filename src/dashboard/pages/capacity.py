from dash import html, dcc
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
from src.dashboard.styles import COLORS, CARD_STYLE

# Mock data
df_capacity = pd.DataFrame({
    "Person": ["Alice", "Bob", "Charlie", "Diana", "Eve"],
    "Utilization": [85, 92, 45, 78, 60],
    "Role": ["Architect", "Engineer", "Data Scientist", "Engineer", "PM"]
})

layout = dbc.Container([
    html.H2("Team Capacity", className="mb-4"),
    
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Current Utilization"),
                dbc.CardBody(
                    dcc.Graph(
                        figure=px.bar(df_capacity, x="Utilization", y="Person", orientation='h', 
                                      title="Team Utilization (%)", template="plotly_white",
                                      color="Utilization", color_continuous_scale=[COLORS['success'], COLORS['warning'], COLORS['danger']])
                    )
                )
            ], style=CARD_STYLE)
        ], width=12, lg=8),
        
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Workload Balance"),
                dbc.CardBody([
                    html.H5("Overloaded", className="text-danger"),
                    html.Ul([html.Li("Bob (92%) - Risk of burnout")]),
                    html.Hr(),
                    html.H5("Available", className="text-success"),
                    html.Ul([html.Li("Charlie (45%) - Open for new projects")])
                ])
            ], style=CARD_STYLE)
        ], width=12, lg=4)
    ])
], fluid=True)
