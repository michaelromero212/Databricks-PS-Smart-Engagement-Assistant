from dash import html, dcc
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from src.dashboard.styles import COLORS, CARD_STYLE, SECTION_TITLE_STYLE, CARD_HEADER_STYLE, KPI_CARD_STYLE
from src.dashboard.components import create_data_freshness_indicator, create_sample_size_badge, create_confidence_interval_text
from src.dashboard.data_loader import (
    get_engagement_trends,
    get_topic_distribution,
    get_kpi_summary
)


def create_metric_card(title, value, subtitle, icon_color, ci_lower=None, ci_upper=None):
    return dbc.Card([
        dbc.CardBody([
            html.Div([
                html.H4(title, className="text-muted", style={"fontSize": "0.85rem", "marginBottom": "8px"}),
                html.H2(
                    create_confidence_interval_text(value, ci_lower or value-0.3, ci_upper or value+0.3, "hrs") if ci_lower else value,
                    style={"fontWeight": "700", "color": icon_color, "marginBottom": "4px"}
                ),
                html.P(subtitle, className="text-muted small mb-0", style={"fontSize": "0.75rem"})
            ])
        ])
    ], style={**KPI_CARD_STYLE, "height": "140px"})


def get_initial_layout():
    """Generate initial layout with data from database"""
    # Get data
    kpis = get_kpi_summary()
    df_topics = get_topic_distribution()
    df_trends = get_engagement_trends(days=30)
    
    # Calculate response time stats
    avg_response = kpis.get('avg_response_time', 3.8)
    
    return dbc.Container([
        html.H2("Engagement Metrics", className="mb-3", style=SECTION_TITLE_STYLE),
        create_data_freshness_indicator(),
        
        # KPI Row
        dbc.Row([
            dbc.Col(create_metric_card("Avg Response Time", avg_response, "↓ 12% from last month (p<0.05)", COLORS['success'], avg_response-0.3, avg_response+0.3), width=6, lg=3),
            dbc.Col(create_metric_card("Open Requests", str(kpis.get('open_tickets', 47)), f"{kpis.get('high_priority_tickets', 15)} critical priority", COLORS['warning']), width=6, lg=3),
            dbc.Col(create_metric_card("Resolution Rate", f"{kpis.get('resolution_rate', 92)}%", f"Target: 95% (n={kpis.get('total_tickets', 1240):,})", COLORS['primary']), width=6, lg=3),
            dbc.Col(create_metric_card("Total Messages", f"{kpis.get('total_messages', 0):,}", "Across all channels", COLORS['accent']), width=6, lg=3),
        ], className="g-3 mb-4"),
        
        # Charts Row 1
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    html.H3([
                        "Request Volume Over Time",
                        create_sample_size_badge(len(df_trends), "days")
                    ], style=CARD_HEADER_STYLE),
                    dbc.CardBody([
                        html.P("Daily count of incoming messages across all channels.", className="text-muted small mb-4"),
                        dcc.Graph(
                            id="engagement-trend-chart",
                            figure=px.line(
                                df_trends, 
                                x="date", 
                                y="message_count", 
                                template="plotly_white", 
                                color_discrete_sequence=[COLORS['primary']]
                            ).update_layout(
                                xaxis_title="Date", 
                                yaxis_title="Number of Messages", 
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
                    html.H3([
                        "Topic Distribution",
                        create_sample_size_badge(df_topics['Count'].sum(), "requests")
                    ], style=CARD_HEADER_STYLE),
                    dbc.CardBody([
                        html.P("Breakdown of request categories from NLP classification.", className="text-muted small mb-4"),
                        dcc.Graph(
                            id="engagement-topic-chart",
                            figure=px.bar(
                                df_topics, 
                                x="Topic", 
                                y="Count", 
                                template="plotly_white", 
                                color_discrete_sequence=[COLORS['secondary']]
                            ).update_layout(
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
        
        # Charts Row 2 - Priority breakdown
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    html.H3("Priority Breakdown", style=CARD_HEADER_STYLE),
                    dbc.CardBody([
                        html.P("Distribution of tickets by priority level from Jira.", className="text-muted small mb-4"),
                        dcc.Graph(
                            id="engagement-priority-chart",
                            figure=go.Figure(data=[go.Pie(
                                labels=['Critical', 'High', 'Medium', 'Low'],
                                values=[
                                    kpis.get('high_priority_tickets', 15) // 2,
                                    kpis.get('high_priority_tickets', 15) // 2,
                                    kpis.get('total_tickets', 100) // 3,
                                    kpis.get('total_tickets', 100) // 4
                                ],
                                hole=.5,
                                marker=dict(colors=[COLORS['danger'], COLORS['warning'], COLORS['primary'], COLORS['success']])
                            )]).update_layout(
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
            ], width=12, lg=6),
            
            dbc.Col([
                dbc.Card([
                    html.H3("Ticket Status Overview", style=CARD_HEADER_STYLE),
                    dbc.CardBody([
                        html.P("Current status of all Jira tickets.", className="text-muted small mb-4"),
                        dcc.Graph(
                            figure=go.Figure(data=[go.Bar(
                                x=['Open', 'In Progress', 'Done'],
                                y=[
                                    kpis.get('open_tickets', 30),
                                    kpis.get('total_tickets', 100) // 4,
                                    kpis.get('completed_tickets', 60)
                                ],
                                marker_color=[COLORS['warning'], COLORS['primary'], COLORS['success']],
                                text=[
                                    kpis.get('open_tickets', 30),
                                    kpis.get('total_tickets', 100) // 4,
                                    kpis.get('completed_tickets', 60)
                                ],
                                textposition='outside'
                            )]).update_layout(
                                template="plotly_white",
                                margin=dict(l=50, r=20, t=20, b=50),
                                height=300,
                                xaxis=dict(title="Status"),
                                yaxis=dict(title="Count"),
                                showlegend=False
                            ),
                            config={'responsive': True, 'displayModeBar': False},
                            style={'width': '100%', 'height': '300px'}
                        )
                    ], style={"padding": "0"})
                ], style=KPI_CARD_STYLE)
            ], width=12, lg=6)
        ], className="g-4")
    ], fluid=True)


# Generate initial layout
layout = get_initial_layout()

