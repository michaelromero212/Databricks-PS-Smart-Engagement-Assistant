from dash import html
import dash_bootstrap_components as dbc
from datetime import datetime

def create_data_freshness_indicator():
    """Create a timestamp indicator showing when data was last updated"""
    return dbc.Alert([
        html.I(className="bi bi-clock me-2"),
        html.Small([
            "Data as of: ",
            html.Strong(datetime.now().strftime("%B %d, %Y at %I:%M %p")),
            " | ",
            html.Span("Data refreshed hourly", className="text-muted")
        ])
    ], color="light", className="mb-3", style={
        "fontSize": "0.85rem",
        "padding": "8px 16px",
        "borderLeft": "3px solid #0F62FE"
    })

def create_sample_size_badge(n, label="samples"):
    """Create a badge showing sample size"""
    return html.Span([
        html.I(className="bi bi-database me-1"),
        f"n={n:,} {label}"
    ], className="badge bg-secondary", style={
        "fontSize": "0.75rem",
        "fontWeight": "normal",
        "marginLeft": "8px"
    })

def create_confidence_interval_text(value, ci_lower, ci_upper, unit=""):
    """Format value with confidence interval"""
    return html.Span([
        html.Strong(f"{value}{unit}"),
        html.Small(f" ±{abs(value - ci_lower):.1f}{unit}", className="text-muted ms-1"),
        html.Small(" (95% CI)", className="text-muted ms-1", style={"fontSize": "0.7rem"})
    ])
