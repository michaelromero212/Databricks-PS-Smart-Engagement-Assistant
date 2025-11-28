from dash import html, dcc
import dash_bootstrap_components as dbc
from src.dashboard.styles import COLORS, CARD_STYLE

def create_opportunity_card(title, description, impact, savings):
    color = COLORS['success'] if impact == "High" else COLORS['warning']
    return dbc.Card([
        dbc.CardBody([
            html.H5(title, className="card-title"),
            html.H6(f"Impact: {impact}", style={"color": color}),
            html.P(description, className="card-text"),
            html.P(f"Est. Savings: {savings}", className="text-muted small"),
            dbc.Button("Simulate Implementation", color="primary", size="sm", outline=True)
        ])
    ], style={**CARD_STYLE, "marginBottom": "10px"})

layout = dbc.Container([
    html.H2("Automation Opportunities", className="mb-4"),
    
    dbc.Row([
        dbc.Col([
            html.H4("High Priority", className="mb-3"),
            create_opportunity_card("Frequent 'Access Denied' Issues", "Detected 15 requests related to permission errors in Bronze layer.", "High", "12 hours/month"),
            create_opportunity_card("Manual Report Generation", "Weekly requests for status report generation.", "High", "8 hours/month"),
        ], width=12, md=6),
        
        dbc.Col([
            html.H4("Medium Priority", className="mb-3"),
            create_opportunity_card("Documentation Gaps: Delta Live Tables", "Multiple questions about DLT syntax.", "Medium", "4 hours/month"),
            create_opportunity_card("Meeting Scheduling", "High volume of scheduling coordination messages.", "Medium", "2 hours/month"),
        ], width=12, md=6)
    ])
], fluid=True)
