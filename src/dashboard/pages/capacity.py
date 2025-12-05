from dash import html, dcc
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
from src.dashboard.styles import COLORS, CARD_STYLE, SECTION_TITLE_STYLE, CARD_HEADER_STYLE, KPI_CARD_STYLE
from src.dashboard.data_loader import get_team_capacity
from src.dashboard.components import create_data_freshness_indicator


def get_initial_layout():
    """Generate initial layout with data from database"""
    df_capacity = get_team_capacity()
    
    # Calculate summary stats
    avg_util = df_capacity['Utilization'].mean()
    overloaded = df_capacity[df_capacity['Utilization'] > 85]
    available = df_capacity[df_capacity['Utilization'] < 60]
    
    return dbc.Container([
        html.H2("Team Capacity", className="mb-3", style=SECTION_TITLE_STYLE),
        create_data_freshness_indicator(),
        
        # Summary KPIs
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4("Team Size", className="text-muted", style={"fontSize": "0.9rem"}),
                        html.H2(str(len(df_capacity)), style={"fontWeight": "700", "fontSize": "2.5rem"}),
                        html.Span("Active team members", className="text-muted")
                    ])
                ], style=KPI_CARD_STYLE)
            ], width=6, lg=3),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4("Avg Utilization", className="text-muted", style={"fontSize": "0.9rem"}),
                        html.H2(f"{avg_util:.0f}%", style={
                            "fontWeight": "700", 
                            "fontSize": "2.5rem",
                            "color": COLORS['warning'] if avg_util > 80 else COLORS['success']
                        }),
                        html.Span("Target: 75-85%", className="text-muted")
                    ])
                ], style=KPI_CARD_STYLE)
            ], width=6, lg=3),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4("Overloaded", className="text-muted", style={"fontSize": "0.9rem"}),
                        html.H2(str(len(overloaded)), style={
                            "fontWeight": "700", 
                            "fontSize": "2.5rem",
                            "color": COLORS['danger'] if len(overloaded) > 0 else COLORS['success']
                        }),
                        html.Span("Above 85% utilization", className="text-danger" if len(overloaded) > 0 else "text-muted")
                    ])
                ], style=KPI_CARD_STYLE)
            ], width=6, lg=3),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4("Available", className="text-muted", style={"fontSize": "0.9rem"}),
                        html.H2(str(len(available)), style={
                            "fontWeight": "700", 
                            "fontSize": "2.5rem",
                            "color": COLORS['success']
                        }),
                        html.Span("Below 60% utilization", className="text-success")
                    ])
                ], style=KPI_CARD_STYLE)
            ], width=6, lg=3),
        ], className="g-3 mb-4"),
        
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    html.H3("Current Utilization", style=CARD_HEADER_STYLE),
                    dbc.CardBody([
                        html.P("Team member workload distribution. Red indicates risk of burnout.", 
                               className="text-muted small mb-4"),
                        dcc.Graph(
                            id="capacity-chart",
                            figure=px.bar(
                                df_capacity.sort_values('Utilization', ascending=True), 
                                x="Utilization", 
                                y="Person", 
                                orientation='h',
                                template="plotly_white",
                                color="Utilization",
                                color_continuous_scale=[
                                    [0, COLORS['success']],
                                    [0.6, COLORS['success']],
                                    [0.75, COLORS['warning']],
                                    [0.85, COLORS['danger']],
                                    [1.0, COLORS['danger']]
                                ],
                                range_color=[0, 100]
                            ).update_layout(
                                xaxis_title="Utilization %",
                                yaxis_title="",
                                margin=dict(l=100, r=20, t=20, b=50),
                                height=400,
                                coloraxis_showscale=False,
                                xaxis=dict(range=[0, 100])
                            ).update_traces(
                                text=df_capacity.sort_values('Utilization', ascending=True)['Utilization'].astype(str) + '%',
                                textposition='outside'
                            ),
                            config={'responsive': True, 'displayModeBar': False},
                            style={'width': '100%', 'height': '400px'}
                        )
                    ], style={"padding": "0"})
                ], style=KPI_CARD_STYLE)
            ], width=12, lg=8),
            
            dbc.Col([
                dbc.Card([
                    html.H3("Workload Alerts", style=CARD_HEADER_STYLE),
                    dbc.CardBody([
                        html.P("Team members requiring attention.", className="text-muted small mb-3"),
                        
                        # Overloaded section
                        html.Div([
                            html.H6([
                                html.I(className="bi bi-exclamation-triangle-fill text-danger me-2"),
                                "Overloaded"
                            ], className="text-danger mb-2"),
                            dbc.ListGroup([
                                dbc.ListGroupItem([
                                    html.Div([
                                        html.Strong(row['Person']),
                                        html.Span(f" ({row['Utilization']}%)", className="text-danger")
                                    ]),
                                    html.Small("Risk of burnout", className="text-muted")
                                ], style={"border": "none", "padding": "8px 0"})
                                for _, row in overloaded.iterrows()
                            ] if len(overloaded) > 0 else [
                                dbc.ListGroupItem("No overloaded team members", 
                                                  className="text-success", 
                                                  style={"border": "none"})
                            ], flush=True)
                        ], className="mb-4"),
                        
                        html.Hr(),
                        
                        # Available section
                        html.Div([
                            html.H6([
                                html.I(className="bi bi-check-circle-fill text-success me-2"),
                                "Available for New Work"
                            ], className="text-success mb-2"),
                            dbc.ListGroup([
                                dbc.ListGroupItem([
                                    html.Div([
                                        html.Strong(row['Person']),
                                        html.Span(f" ({row['Utilization']}%)", className="text-success")
                                    ]),
                                    html.Small(f"Role: {row['Role']}", className="text-muted")
                                ], style={"border": "none", "padding": "8px 0"})
                                for _, row in available.iterrows()
                            ] if len(available) > 0 else [
                                dbc.ListGroupItem("Team at healthy capacity", 
                                                  className="text-muted", 
                                                  style={"border": "none"})
                            ], flush=True)
                        ])
                    ], style={"padding": "0"})
                ], style=KPI_CARD_STYLE)
            ], width=12, lg=4)
        ])
    ], fluid=True)


# Generate initial layout
layout = get_initial_layout()

