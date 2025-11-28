from dash import html, dcc
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
from src.dashboard.styles import COLORS, CARD_STYLE, SECTION_TITLE_STYLE, CARD_HEADER_STYLE, KPI_CARD_STYLE

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
    html.H2("Engagement Metrics", className="mb-4", style=SECTION_TITLE_STYLE),
    
    dbc.Row([
        dbc.Col([
            dbc.Card([
                html.H3("Request Volume Over Time", style=CARD_HEADER_STYLE),
                dbc.CardBody([
                    html.P("Daily count of incoming requests across all channels.", className="text-muted small mb-4"),
                    dcc.Graph(
                        figure=px.line(df_time, x="Date", y="Requests", template="plotly_white", color_discrete_sequence=[COLORS['primary']])
                        .update_layout(
                            xaxis_title="Date", 
                            yaxis_title="Number of Requests", 
                            margin=dict(l=50, r=20, t=20, b=50),
                            height=350,
                            xaxis=dict(title_font=dict(size=12), tickfont=dict(size=10)),
                            yaxis=dict(title_font=dict(size=12), tickfont=dict(size=10))
                        ),
                        config={'responsive': True, 'displayModeBar': False},
                        style={'width': '100%', 'height': '350px'}
                    )
                ], style={"padding": "0"})
            ], style=KPI_CARD_STYLE)
        ], width=12, lg=8),
        
        dbc.Col([
            dbc.Card([
                html.H3("Topic Distribution", style=CARD_HEADER_STYLE),
                dbc.CardBody([
                    html.P("Breakdown of request categories.", className="text-muted small mb-4"),
                    dcc.Graph(
                        figure=px.bar(df_topics, x="Topic", y="Count", template="plotly_white", color_discrete_sequence=[COLORS['secondary']])
                        .update_layout(
                            xaxis_title="Topic Category", 
                            yaxis_title="Count", 
                            margin=dict(l=50, r=20, t=20, b=50),
                            height=350,
                            xaxis=dict(title_font=dict(size=12), tickfont=dict(size=10)),
                            yaxis=dict(title_font=dict(size=12), tickfont=dict(size=10))
                        ),
                        config={'responsive': True, 'displayModeBar': False},
                        style={'width': '100%', 'height': '350px'}
                    )
                ], style={"padding": "0"})
            ], style=KPI_CARD_STYLE)
        ], width=12, lg=4)
    ], className="g-4 mb-4"),
    
    dbc.Row([
        dbc.Col([
            dbc.Card([
                html.H3("Response Time Analysis", style=CARD_HEADER_STYLE),
                dbc.CardBody([
                    html.P("Distribution of response times in hours. The box shows the interquartile range.", className="text-muted small mb-4"),
                    dcc.Graph(
                        figure=px.box(y=[2, 3, 2, 5, 8, 3, 4, 2, 1, 5, 6, 3], template="plotly_white", color_discrete_sequence=[COLORS['accent']])
                        .update_layout(
                            yaxis_title="Hours", 
                            xaxis_title="", 
                            margin=dict(l=50, r=20, t=20, b=50),
                            height=350,
                            xaxis=dict(title_font=dict(size=12), tickfont=dict(size=10)),
                            yaxis=dict(title_font=dict(size=12), tickfont=dict(size=10))
                        ),
                        config={'responsive': True, 'displayModeBar': False},
                        style={'width': '100%', 'height': '350px'}
                    )
                ], style={"padding": "0"})
            ], style=KPI_CARD_STYLE)
        ], width=12)
    ], className="g-4")
], fluid=True)
