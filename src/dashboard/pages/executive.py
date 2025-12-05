from dash import html, dcc
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
from src.dashboard.styles import KPI_CARD_STYLE, COLORS, SECTION_TITLE_STYLE, CARD_HEADER_STYLE
from src.dashboard.data_loader import (
    get_kpi_summary, 
    get_weekly_engagement_counts, 
    get_project_health_distribution
)
from src.analysis.health_score import calculate_health_score


def create_kpi_card(title, value, trend, trend_color, card_id=None):
    """Create a KPI card with value and trend indicator"""
    trend_class = "trend-up" if trend_color == "up" else "trend-down" if trend_color == "down" else "trend-stable"
    
    # Build H2 element - only add id if provided
    h2_props = {
        "className": "card-text",
        "style": {
            "fontWeight": "700", 
            "fontSize": "2.5rem", 
            "marginBottom": "8px"
        }
    }
    if card_id:
        h2_props["id"] = card_id
    
    return dbc.Card(
        [
            html.H4(title, className="card-title", style={
                "fontSize": "0.9rem", 
                "color": "#666", 
                "marginBottom": "8px", 
                "textTransform": "uppercase", 
                "letterSpacing": "0.5px"
            }),
            html.H2(value, **h2_props),
            html.Span(
                [f"{trend}"],
                className=trend_class,
                style={"fontWeight": "600", "fontSize": "1rem"}
            )
        ],
        style=KPI_CARD_STYLE
    )


def create_health_score_card():
    """Create health score card with gauge"""
    health = calculate_health_score()
    
    # Determine color based on score
    if health.score >= 85:
        color_class = "health-score-excellent"
        gauge_color = COLORS['success']
    elif health.score >= 70:
        color_class = "health-score-good"
        gauge_color = COLORS['secondary']
    elif health.score >= 50:
        color_class = "health-score-at-risk"
        gauge_color = COLORS['warning']
    else:
        color_class = "health-score-critical"
        gauge_color = COLORS['danger']
    
    trend_class = "trend-up" if health.trend == "↑" else "trend-down" if health.trend == "↓" else "trend-stable"
    
    return dbc.Card([
        html.H4("Engagement Health Score", className="card-title", style={
            "fontSize": "0.9rem", 
            "color": "#666", 
            "marginBottom": "8px", 
            "textTransform": "uppercase", 
            "letterSpacing": "0.5px"
        }),
        html.Div([
            html.Span(f"{health.score}", className=color_class, style={
                "fontWeight": "700", 
                "fontSize": "2.5rem"
            }),
            html.Span("/100", style={
                "fontSize": "1.2rem",
                "color": "#999",
                "marginLeft": "4px"
            })
        ]),
        html.Div([
            html.Span(health.trend, className=trend_class, style={"fontSize": "1.2rem", "marginRight": "8px"}),
            html.Span(health.status, style={
                "fontSize": "0.9rem",
                "color": gauge_color,
                "fontWeight": "600"
            })
        ], style={"marginTop": "4px"})
    ], style=KPI_CARD_STYLE)


def get_initial_layout():
    """Generate initial layout with data from database"""
    # Get KPIs
    kpis = get_kpi_summary()
    
    # Get weekly trends
    weekly_counts = get_weekly_engagement_counts()
    
    # Get health distribution
    health_dist = get_project_health_distribution()
    
    return dbc.Container([
        html.H2("Executive Summary", className="mb-4", style=SECTION_TITLE_STYLE),
        
        # KPI Row with Health Score
        dbc.Row([
            dbc.Col(create_health_score_card(), width=12, sm=6, lg=3),
            dbc.Col(create_kpi_card(
                "Total Engagements", 
                str(kpis['total_engagements']), 
                f"+{kpis['total_engagements'] // 10}%", 
                "up"
            ), width=12, sm=6, lg=3),
            dbc.Col(create_kpi_card(
                "Avg Response Time", 
                f"{kpis['avg_response_time']}h", 
                "-15%", 
                "up"  # Down is good for response time
            ), width=12, sm=6, lg=3),
            dbc.Col(create_kpi_card(
                "Resolution Rate", 
                f"{kpis['resolution_rate']}%", 
                "+3%", 
                "up"
            ), width=12, sm=6, lg=3),
        ], className="mb-4 g-4"),
        
        # Charts Row
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    html.H3("Engagement Trends", style=CARD_HEADER_STYLE),
                    dbc.CardBody([
                        html.P("Weekly active engagement count over the last 8 weeks.", 
                               className="text-muted small mb-4"),
                        dcc.Graph(
                            id="executive-trend-chart",
                            figure=go.Figure(
                                data=[go.Scatter(
                                    y=weekly_counts, 
                                    mode='lines+markers', 
                                    line=dict(color=COLORS['primary'], width=3), 
                                    marker=dict(size=8),
                                    name="Engagements"
                                )],
                                layout=dict(
                                    template="plotly_white", 
                                    height=350, 
                                    autosize=True,
                                    margin=dict(l=50, r=20, t=20, b=50),
                                    xaxis=dict(
                                        title="Week", 
                                        showgrid=False, 
                                        title_font=dict(size=12), 
                                        tickfont=dict(size=10)
                                    ),
                                    yaxis=dict(
                                        title="Count", 
                                        showgrid=True, 
                                        gridcolor="#f0f0f0", 
                                        title_font=dict(size=12), 
                                        tickfont=dict(size=10)
                                    )
                                )
                            ),
                            config={'responsive': True, 'displayModeBar': False},
                            style={'width': '100%', 'height': '350px'}
                        )
                    ], style={"padding": "0"})
                ], style=KPI_CARD_STYLE)
            ], width=12, lg=8),
            
            dbc.Col([
                dbc.Card([
                    html.H3("Project Health Distribution", style=CARD_HEADER_STYLE),
                    dbc.CardBody([
                        html.P("Current status of active projects.", className="text-muted small mb-4"),
                        dcc.Graph(
                            id="executive-health-pie",
                            figure=go.Figure(
                                data=[go.Pie(
                                    labels=list(health_dist.keys()), 
                                    values=list(health_dist.values()), 
                                    hole=.6, 
                                    marker=dict(colors=[
                                        COLORS['success'], 
                                        COLORS['warning'], 
                                        COLORS['danger']
                                    ])
                                )],
                                layout=dict(
                                    template="plotly_white", 
                                    height=350, 
                                    autosize=True,
                                    margin=dict(l=20, r=20, t=20, b=20),
                                    showlegend=True,
                                    legend=dict(
                                        orientation="h", 
                                        yanchor="bottom", 
                                        y=-0.1, 
                                        xanchor="center", 
                                        x=0.5
                                    )
                                )
                            ),
                            config={'responsive': True, 'displayModeBar': False},
                            style={'width': '100%', 'height': '350px'}
                        )
                    ], style={"padding": "0"})
                ], style=KPI_CARD_STYLE)
            ], width=12, lg=4)
        ], className="g-4 mb-4"),

        # Risks & Alerts Row
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    html.H3("Top Risks & Alerts", style=CARD_HEADER_STYLE),
                    dbc.CardBody([
                        html.P("Critical items requiring immediate attention.", 
                               className="text-muted small mb-3"),
                        dbc.ListGroup([
                            dbc.ListGroupItem([
                                html.Div([
                                    html.H6(f"High Priority Tickets: {kpis['high_priority_tickets']}", 
                                            className="mb-1 text-danger", style={"fontWeight": "600"}),
                                    html.P("Critical and high priority tickets requiring attention.", 
                                           className="mb-1 small text-muted"),
                                    html.Small("Based on current Jira data", 
                                              className="text-muted", style={"fontSize": "0.75rem"})
                                ])
                            ], style={"border": "none", "borderBottom": "1px solid #eee", "padding": "16px 0"}),
                            dbc.ListGroupItem([
                                html.Div([
                                    html.H6(f"Open Tickets: {kpis['open_tickets']}", 
                                            className="mb-1 text-warning", style={"fontWeight": "600"}),
                                    html.P("Tickets currently in progress or awaiting action.", 
                                           className="mb-1 small text-muted"),
                                    html.Small("Refresh to see latest status", 
                                              className="text-muted", style={"fontSize": "0.75rem"})
                                ])
                            ], style={"border": "none", "borderBottom": "1px solid #eee", "padding": "16px 0"}),
                            dbc.ListGroupItem([
                                html.Div([
                                    html.H6(f"Total Messages: {kpis['total_messages']:,}", 
                                            className="mb-1", style={"fontWeight": "600", "color": COLORS['primary']}),
                                    html.P("Slack messages analyzed across all projects.", 
                                           className="mb-1 small text-muted"),
                                    html.Small("From engagement data", 
                                              className="text-muted", style={"fontSize": "0.75rem"})
                                ])
                            ], style={"border": "none", "padding": "16px 0"}),
                        ], flush=True)
                    ], style={"padding": "0"})
                ], style=KPI_CARD_STYLE)
            ], width=12)
        ], className="g-4")
    ], fluid=True)


# Generate initial layout
layout = get_initial_layout()

