from dash import html, dcc
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
from src.dashboard.styles import COLORS, CARD_STYLE

# Mock data for visualization
df_topics = pd.DataFrame({
    "Topic": ["Technical Issue", "Feature Request", "Documentation", "Process", "Training"],
    "Count": [45, 32, 28, 15, 12]
})

df_time = pd.DataFrame({
    "Date": pd.date_range(start="2023-01-01", periods=30),
    "Requests": [10, 12, 15, 14, 18, 22, 20, 25, 28, 30, 25, 22, 20, 18, 15, 12, 10, 8, 12, 15, 18, 22, 25, 28, 30, 32, 35, 38, 40, 42]
})

layout = dbc.Container([
    html.H2("Engagement Metrics", className="mb-4"),
    
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Request Volume Over Time"),
                dbc.CardBody([
                    html.P("Daily count of incoming requests across all channels.", className="text-muted small"),
                    dcc.Graph(
                        figure=px.line(df_time, x="Date", y="Requests", title="Daily Request Volume", template="plotly_white", color_discrete_sequence=[COLORS['primary']])
                        .update_layout(xaxis_title="Date", yaxis_title="Number of Requests", margin=dict(l=40, r=20, t=40, b=40)),
                        config={'responsive': True}
                    )
                ])
            ], style=CARD_STYLE)
        ], width=12, lg=8),
        
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Topic Distribution"),
                dbc.CardBody([
                    html.P("Breakdown of request categories.", className="text-muted small"),
                    dcc.Graph(
                        figure=px.bar(df_topics, x="Topic", y="Count", title="Requests by Topic", template="plotly_white", color_discrete_sequence=[COLORS['secondary']])
                        .update_layout(xaxis_title="Topic Category", yaxis_title="Count", margin=dict(l=40, r=20, t=40, b=40)),
                        config={'responsive': True}
                    )
                ])
            ], style=CARD_STYLE)
        ], width=12, lg=4)
    ]),
    
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Response Time Analysis"),
                dbc.CardBody([
                    html.P("Distribution of response times in hours. The box shows the interquartile range.", className="text-muted small"),
                    dcc.Graph(
                        figure=px.box(y=[2, 3, 2, 5, 8, 3, 4, 2, 1, 5, 6, 3], title="Response Time Distribution", template="plotly_white", color_discrete_sequence=[COLORS['accent']])
                        .update_layout(yaxis_title="Hours", xaxis_title="", margin=dict(l=40, r=20, t=40, b=40)),
                        config={'responsive': True}
                    )
                ])
            ], style=CARD_STYLE)
        ], width=12)
    ])
], fluid=True)
