from dash import html, dcc
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
from src.dashboard.styles import KPI_CARD_STYLE, COLORS, SECTION_TITLE_STYLE, CARD_HEADER_STYLE

def create_kpi_card(title, value, trend, trend_color):
    return dbc.Card(
        [
            html.H4(title, className="card-title", style={"fontSize": "0.9rem", "color": "#666", "marginBottom": "8px", "textTransform": "uppercase", "letterSpacing": "0.5px"}),
            html.H2(value, className="card-text", style={"fontWeight": "700", "fontSize": "2.5rem", "marginBottom": "8px"}),
            html.Span(
                [f"{trend}"],
                style={"color": COLORS["success"] if trend_color == "up" else COLORS["danger"], "fontWeight": "600", "fontSize": "1rem"}
            )
        ],
        style=KPI_CARD_STYLE
    )

layout = dbc.Container([
    html.H2("Executive Summary", className="mb-4", style=SECTION_TITLE_STYLE),
    
    dbc.Row([
        dbc.Col(create_kpi_card("Total Engagements", "124", "+12%", "up"), width=12, sm=6, lg=3),
        dbc.Col(create_kpi_card("Avg Response Time", "4.2h", "-15%", "down"), width=12, sm=6, lg=3), # Down is good here, but using red/green logic needs care. Let's assume green is good.
        dbc.Col(create_kpi_card("Automation Potential", "$45k", "+8%", "up"), width=12, sm=6, lg=3),
        dbc.Col(create_kpi_card("Client Satisfaction", "4.8/5", "+0.2", "up"), width=12, sm=6, lg=3),
    ], className="mb-4 g-4"),
    
    dbc.Row([
        dbc.Col([
            dbc.Card([
                html.H3("Engagement Trends", style=CARD_HEADER_STYLE),
                dbc.CardBody([
                    html.P("Weekly active engagement count over the last quarter.", className="text-muted small mb-4"),
                    dcc.Graph(
                        figure=go.Figure(
                            data=[go.Scatter(y=[10, 15, 13, 17, 22, 25, 28], mode='lines+markers', line=dict(color=COLORS['primary'], width=3), name="Engagements")],
                            layout=dict(
                                template="plotly_white", 
                                height=350, 
                                autosize=True,
                                margin=dict(l=50, r=20, t=20, b=50), # Increased margins
                                xaxis=dict(title="Week", showgrid=False, title_font=dict(size=12), tickfont=dict(size=10)),
                                yaxis=dict(title="Count", showgrid=True, gridcolor="#f0f0f0", title_font=dict(size=12), tickfont=dict(size=10))
                            )
                        ),
                        config={'responsive': True, 'displayModeBar': False},
                        style={'width': '100%', 'height': '350px'}
                    )
                ], style={"padding": "0"}) # Remove inner padding to let chart fill
            ], style=KPI_CARD_STYLE)
        ], width=12, lg=8),
        
        dbc.Col([
            dbc.Card([
                html.H3("Project Health Distribution", style=CARD_HEADER_STYLE),
                dbc.CardBody([
                    html.P("Current status of active projects.", className="text-muted small mb-4"),
                    dcc.Graph(
                        figure=go.Figure(
                            data=[go.Pie(labels=["On Track", "At Risk", "Delayed"], values=[65, 25, 10], hole=.6, marker=dict(colors=[COLORS['success'], COLORS['warning'], COLORS['danger']]))],
                            layout=dict(
                                template="plotly_white", 
                                height=350, 
                                autosize=True,
                                margin=dict(l=20, r=20, t=20, b=20),
                                showlegend=True,
                                legend=dict(orientation="h", yanchor="bottom", y=-0.1, xanchor="center", x=0.5)
                            )
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
                html.H3("Top Risks & Alerts", style=CARD_HEADER_STYLE),
                dbc.CardBody([
                    html.P("Critical items requiring immediate attention.", className="text-muted small mb-3"),
                    dbc.ListGroup([
                        dbc.ListGroupItem([
                            html.Div([
                                html.H6("Project Alpha - Budget Overrun", className="mb-1 text-danger", style={"fontWeight": "600"}),
                                html.P("Projected to exceed budget by 15% next week based on current burn rate.", className="mb-1 small text-muted"),
                                html.Small("Detected: 2 hours ago", className="text-muted", style={"fontSize": "0.75rem"})
                            ])
                        ], style={"border": "none", "borderBottom": "1px solid #eee", "padding": "16px 0"}),
                        dbc.ListGroupItem([
                            html.Div([
                                html.H6("Project Gamma - Resource Shortage", className="mb-1 text-warning", style={"fontWeight": "600"}),
                                html.P("Key architect unavailable for 2 weeks. Impact on milestone delivery.", className="mb-1 small text-muted"),
                                html.Small("Detected: 1 day ago", className="text-muted", style={"fontSize": "0.75rem"})
                            ])
                        ], style={"border": "none", "borderBottom": "1px solid #eee", "padding": "16px 0"}),
                         dbc.ListGroupItem([
                            html.Div([
                                html.H6("Client Sentiment Drop - Beta Corp", className="mb-1 text-warning", style={"fontWeight": "600"}),
                                html.P("Negative sentiment detected in last 3 email threads.", className="mb-1 small text-muted"),
                                html.Small("Detected: 4 hours ago", className="text-muted", style={"fontSize": "0.75rem"})
                            ])
                        ], style={"border": "none", "padding": "16px 0"}),
                    ], flush=True)
                ], style={"padding": "0"})
            ], style=KPI_CARD_STYLE)
        ], width=12)
    ], className="g-4")
], fluid=True)
