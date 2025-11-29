from dash import html, dcc
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
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

# Response time data with more realistic distribution
response_times = [2, 3, 2, 5, 8, 3, 4, 2, 1, 5, 6, 3, 4, 2, 3, 5, 7, 4, 3, 2, 6, 4, 3, 5, 8, 3, 2, 4, 5, 3]

def create_metric_card(title, value, subtitle, icon_color):
    return dbc.Card([
        dbc.CardBody([
            html.Div([
                html.H4(title, className="text-muted", style={"fontSize": "0.85rem", "marginBottom": "8px"}),
                html.H2(value, style={"fontWeight": "700", "color": icon_color, "marginBottom": "4px"}),
                html.P(subtitle, className="text-muted small mb-0", style={"fontSize": "0.75rem"})
            ])
        ])
    ], style={**KPI_CARD_STYLE, "height": "140px"})

layout = dbc.Container([
    html.H2("Engagement Metrics", className="mb-4", style=SECTION_TITLE_STYLE),
    
    # KPI Row
    dbc.Row([
        dbc.Col(create_metric_card("Avg Response Time", "3.8hrs", "↓ 12% from last month", COLORS['success']), width=6, lg=3),
        dbc.Col(create_metric_card("Open Requests", "47", "15 critical priority", COLORS['warning']), width=6, lg=3),
        dbc.Col(create_metric_card("Resolution Rate", "92%", "Target: 95%", COLORS['primary']), width=6, lg=3),
        dbc.Col(create_metric_card("SLA Compliance", "88%", "↑ 3% this quarter", COLORS['accent']), width=6, lg=3),
    ], className="g-3 mb-4"),
    
    # Charts Row 1
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
        ], width=12, lg=7),
        
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
        ], width=12, lg=5)
    ], className="g-4 mb-4"),
    
    # Charts Row 2
    dbc.Row([
        dbc.Col([
            dbc.Card([
                html.H3("Response Time Distribution", style=CARD_HEADER_STYLE),
                dbc.CardBody([
                    html.P("Histogram showing frequency of response times. Most tickets resolved in 2-4 hours.", className="text-muted small mb-4"),
                    dcc.Graph(
                        figure=go.Figure(data=[go.Histogram(
                            x=response_times,
                            nbinsx=8,
                            marker_color=COLORS['accent'],
                            opacity=0.8,
                            name='Response Time'
                        )])
                        .update_layout(
                            template="plotly_white",
                            xaxis_title="Response Time (hours)", 
                            yaxis_title="Number of Tickets", 
                            margin=dict(l=50, r=20, t=20, b=50),
                            height=300,
                            bargap=0.1,
                            xaxis=dict(title_font=dict(size=12), tickfont=dict(size=10)),
                            yaxis=dict(title_font=dict(size=12), tickfont=dict(size=10))
                        ),
                        config={'responsive': True, 'displayModeBar': False},
                        style={'width': '100%', 'height': '300px'}
                    )
                ], style={"padding": "0"})
            ], style=KPI_CARD_STYLE)
        ], width=12, lg=6),
        
        dbc.Col([
            dbc.Card([
                html.H3("Priority Breakdown", style=CARD_HEADER_STYLE),
                dbc.CardBody([
                    html.P("Distribution of requests by priority level.", className="text-muted small mb-4"),
                    dcc.Graph(
                        figure=go.Figure(data=[go.Pie(
                            labels=['Critical', 'High', 'Medium', 'Low'],
                            values=[15, 32, 45, 20],
                            hole=.5,
                            marker=dict(colors=[COLORS['danger'], COLORS['warning'], COLORS['primary'], COLORS['success']])
                        )])
                        .update_layout(
                            template="plotly_white",
                            margin=dict(l=20, r=20, t=20, b=20),
                            height=300,
                            showlegend=True,
                            legend=dict(orientation="v", yanchor="middle", y=0.5, xanchor="left", x=1.05)
                        ),
                        config={'responsive': True, 'displayModeBar': False},
                        style={'width': '100%', 'height': '300px'}
                    )
                ], style={"padding": "0"})
            ], style=KPI_CARD_STYLE)
        ], width=12, lg=6)
    ], className="g-4")
], fluid=True)
