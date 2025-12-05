from dash import html
import dash_bootstrap_components as dbc
from src.dashboard.styles import COLORS, SECTION_TITLE_STYLE, KPI_CARD_STYLE
from src.dashboard.data_loader import get_automation_opportunities
from src.dashboard.components import create_data_freshness_indicator


def create_opportunity_card(opportunity):
    """Create a card for an automation opportunity"""
    impact = opportunity.get('impact', 'Medium')
    priority_badge = "danger" if impact == "High" else "warning"
    
    return dbc.Card([
        dbc.CardBody([
            html.Div([
                html.H5(opportunity['title'], className="card-title mb-2", style={"fontWeight": "600"}),
                dbc.Badge(f"{impact} Impact", color=priority_badge, className="ms-auto"),
            ], className="d-flex align-items-start mb-2"),
            html.P(opportunity['description'], className="card-text text-muted small mb-3"),
            html.Div([
                html.I(className="bi bi-clock me-2", style={"color": COLORS['success']}),
                html.Span(f"Est. Savings: ", className="text-muted"),
                html.Span(opportunity['savings'], className="text-success fw-bold"),
            ])
        ])
    ], style={**KPI_CARD_STYLE, "marginBottom": "16px"})


def get_initial_layout():
    """Generate initial layout with data"""
    opportunities = get_automation_opportunities()
    
    # Split by priority
    high_priority = [o for o in opportunities if o.get('priority') == 'high']
    medium_priority = [o for o in opportunities if o.get('priority') == 'medium']
    
    # Calculate total savings
    total_hours = 0
    for o in opportunities:
        savings_str = o.get('savings', '0 hours/month')
        try:
            hours = int(savings_str.split()[0])
            total_hours += hours
        except:
            pass
    
    return dbc.Container([
        html.H2("Automation Opportunities", className="mb-3", style=SECTION_TITLE_STYLE),
        create_data_freshness_indicator(),
        
        # Summary Cards
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4("Total Opportunities", className="text-muted", style={"fontSize": "0.9rem"}),
                        html.H2(str(len(opportunities)), style={"fontWeight": "700", "fontSize": "2.5rem"}),
                        html.Span(f"{len(high_priority)} high priority", className="text-danger")
                    ])
                ], style=KPI_CARD_STYLE)
            ], width=6, lg=3),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4("Est. Monthly Savings", className="text-muted", style={"fontSize": "0.9rem"}),
                        html.H2(f"{total_hours}h", style={"fontWeight": "700", "fontSize": "2.5rem", "color": COLORS['success']}),
                        html.Span(f"${total_hours * 150:,} value", className="text-success")
                    ])
                ], style=KPI_CARD_STYLE)
            ], width=6, lg=3),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4("Automation Rate", className="text-muted", style={"fontSize": "0.9rem"}),
                        html.H2("12%", style={"fontWeight": "700", "fontSize": "2.5rem", "color": COLORS['primary']}),
                        html.Span("Target: 25%", className="text-muted")
                    ])
                ], style=KPI_CARD_STYLE)
            ], width=6, lg=3),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4("Detection Source", className="text-muted", style={"fontSize": "0.9rem"}),
                        html.H2("ML", style={"fontWeight": "700", "fontSize": "2.5rem", "color": COLORS['secondary']}),
                        html.Span("Pattern-based clustering", className="text-muted")
                    ])
                ], style=KPI_CARD_STYLE)
            ], width=6, lg=3),
        ], className="g-3 mb-4"),
        
        # Opportunity Cards
        dbc.Row([
            dbc.Col([
                html.H4([
                    html.I(className="bi bi-exclamation-triangle-fill text-danger me-2"),
                    "High Priority"
                ], className="mb-3"),
                *[create_opportunity_card(o) for o in high_priority]
            ], width=12, md=6),
            
            dbc.Col([
                html.H4([
                    html.I(className="bi bi-info-circle-fill text-warning me-2"),
                    "Medium Priority"
                ], className="mb-3"),
                *[create_opportunity_card(o) for o in medium_priority]
            ], width=12, md=6)
        ])
    ], fluid=True)


# Generate layout
layout = get_initial_layout()
