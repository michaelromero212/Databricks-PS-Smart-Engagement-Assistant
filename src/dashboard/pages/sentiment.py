from dash import html, dcc
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import plotly.express as px
from src.dashboard.styles import COLORS, CARD_STYLE, SECTION_TITLE_STYLE, CARD_HEADER_STYLE, KPI_CARD_STYLE
from src.dashboard.components import create_data_freshness_indicator, create_sample_size_badge

# Mock sentiment data
sentiment_distribution = {
    'Positive': 350,
    'Neutral': 180,
    'Negative': 70
}
total_messages = sum(sentiment_distribution.values())

layout = dbc.Container([
    html.H2("Sentiment Analysis", className="mb-3", style=SECTION_TITLE_STYLE),
    create_data_freshness_indicator(),
    
    dbc.Row([
        dbc.Col([
            dbc.Card([
                html.H3([
                    "Sentiment Distribution",
                    create_sample_size_badge(total_messages, "messages")
                ], style=CARD_HEADER_STYLE),
                dbc.CardBody([
                    html.P("Classification of message sentiment using DistilBERT-SST2 (avg. confidence: 0.84)", 
                           className="text-muted small mb-4"),
                    dcc.Graph(
                        figure=go.Figure(data=[
                            go.Bar(
                                x=['Positive', 'Neutral', 'Negative'],
                                y=[sentiment_distribution['Positive'], 
                                   sentiment_distribution['Neutral'], 
                                   sentiment_distribution['Negative']],
                                marker_color=[COLORS['success'], COLORS['warning'], COLORS['danger']],
                                text=[f"{sentiment_distribution['Positive']} ({sentiment_distribution['Positive']/total_messages*100:.1f}%)",
                                      f"{sentiment_distribution['Neutral']} ({sentiment_distribution['Neutral']/total_messages*100:.1f}%)",
                                      f"{sentiment_distribution['Negative']} ({sentiment_distribution['Negative']/total_messages*100:.1f}%)"],
                                textposition='outside'
                            )
                        ])
                        .update_layout(
                            template="plotly_white",
                            yaxis_title="Number of Messages",
                            xaxis_title="Sentiment Category",
                            margin=dict(l=50, r=20, t=40, b=50),
                            height=300,
                            showlegend=False,
                            yaxis=dict(title_font=dict(size=12), tickfont=dict(size=10)),
                            xaxis=dict(title_font=dict(size=12), tickfont=dict(size=10))
                        ),
                        config={'responsive': True, 'displayModeBar': False},
                        style={'width': '100%', 'height': '300px'}
                    )
                ], style={"padding": "0"})
            ], style=KPI_CARD_STYLE)
        ], width=12, md=6),
        
        dbc.Col([
            dbc.Card([
                html.H3([
                    "Sentiment by Project",
                    create_sample_size_badge(12, "projects")
                ], style=CARD_HEADER_STYLE),
                dbc.CardBody([
                    html.P("Project health based on average sentiment score (scale: 0-100)", 
                           className="text-muted small mb-4"),
                    dcc.Graph(
                        figure=go.Figure(
                            data=[
                                go.Bar(
                                    x=["PROJ-ALPHA", "PROJ-BETA", "PROJ-GAMMA", "PROJ-DELTA"], 
                                    y=[85, 62, 45, 90], 
                                    marker_color=[COLORS['success'], COLORS['warning'], COLORS['danger'], COLORS['success']],
                                    text=["85 (Good)", "62 (Moderate)", "45 (At Risk)", "90 (Excellent)"],
                                    textposition='outside'
                                )
                            ]
                        )
                        .update_layout(
                            template="plotly_white",
                            yaxis_title="Sentiment Score",
                            xaxis_title="Project",
                            margin=dict(l=50, r=20, t=20, b=50),
                            height=300,
                            yaxis=dict(range=[0, 100], title_font=dict(size=12), tickfont=dict(size=10)),
                            xaxis=dict(title_font=dict(size=12), tickfont=dict(size=10))
                        ),
                        config={'responsive': True, 'displayModeBar': False},
                        style={'width': '100%', 'height': '300px'}
                    )
                ], style={"padding": "0"})
            ], style=KPI_CARD_STYLE)
        ], width=12, md=6)
    ], className="g-4 mb-4"),
    
    dbc.Row([
        dbc.Col([
            dbc.Card([
                html.H3([
                    "30-Day Sentiment Trend",
                    create_sample_size_badge(360, "daily aggregates")
                ], style=CARD_HEADER_STYLE),
                dbc.CardBody([
                    html.P("Rolling 7-day average sentiment score with 95% confidence band", 
                           className="text-muted small mb-4"),
                    dcc.Graph(
                        figure=go.Figure(
                            data=[
                                # Confidence band (upper bound)
                                go.Scatter(
                                    x=list(range(0, 12)),
                                    y=[72, 74, 70, 67, 62, 57, 60, 64, 67, 72, 77, 80],
                                    mode='lines',
                                    name='Upper CI',
                                    line=dict(width=0),
                                    showlegend=False,
                                    hoverinfo='skip'
                                ),
                                # Confidence band (lower bound)
                                go.Scatter(
                                    x=list(range(0, 12)),
                                    y=[68, 70, 66, 63, 58, 53, 56, 60, 63, 68, 73, 76],
                                    mode='lines',
                                    name='Lower CI',
                                    line=dict(width=0),
                                    fillcolor='rgba(15, 98, 254, 0.2)',
                                    fill='tonexty',
                                    showlegend=True,
                                    hoverinfo='skip'
                                ),
                                # Main trend line
                                go.Scatter(
                                    x=list(range(0, 12)),
                                    y=[70, 72, 68, 65, 60, 55, 58, 62, 65, 70, 75, 78], 
                                    mode='lines+markers', 
                                    name='Avg Sentiment',
                                    line=dict(color=COLORS['primary'], width=3),
                                    marker=dict(size=8)
                                )
                            ]
                        )
                        .update_layout(
                            template="plotly_white",
                            yaxis_title="Sentiment Score",
                            xaxis_title="Days Ago",
                            margin=dict(l=50, r=20, t=20, b=50),
                            height=300,
                            yaxis=dict(range=[40, 90], title_font=dict(size=12), tickfont=dict(size=10)),
                            xaxis=dict(title_font=dict(size=12), tickfont=dict(size=10)),
                            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
                        ),
                        config={'responsive': True, 'displayModeBar': False},
                        style={'width': '100%', 'height': '300px'}
                    )
                ], style={"padding": "0"})
            ], style=KPI_CARD_STYLE)
        ], width=12)
    ], className="g-4")
], fluid=True)
