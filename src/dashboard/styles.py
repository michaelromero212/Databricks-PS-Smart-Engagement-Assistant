# Colorblind-friendly palettes (IBM Carbon / Okabe-Ito)
COLORS = {
    "primary": "#0F62FE",    # Blue
    "secondary": "#007D79",  # Teal
    "accent": "#D02670",     # Magenta
    "warning": "#FF832B",    # Orange
    "danger": "#DA1E28",     # Red
    "success": "#24A148",    # Green
    "background": "#F4F4F4",
    "text": "#161616",
    "card_bg": "#FFFFFF"
}

# Plotly Template
PLOTLY_TEMPLATE = "plotly_white"

# Common Styles
# Common Styles
CARD_STYLE = {
    "boxShadow": "0 2px 4px rgba(0,0,0,0.05)", # Softer shadow
    "borderRadius": "12px", # Modern rounded corners
    "padding": "24px", # Increased padding
    "marginBottom": "24px",
    "backgroundColor": COLORS["card_bg"],
    "border": "1px solid #E0E0E0" # Subtle border definition
}

HEADER_STYLE = {
    "backgroundColor": "#161616",
    "color": "#FFFFFF",
    "padding": "16px 32px",
    "marginBottom": "32px"
}

NAV_LINK_STYLE = {
    "color": "#FFFFFF",
    "marginRight": "32px",
    "textDecoration": "none",
    "fontSize": "1rem",
    "fontWeight": "500"
}

KPI_CARD_STYLE = {
    **CARD_STYLE,
    "textAlign": "center",
    "height": "100%",
    "display": "flex",
    "flexDirection": "column",
    "justifyContent": "center"
}

# Typography
SECTION_TITLE_STYLE = {
    "fontSize": "1.75rem",
    "fontWeight": "600",
    "color": "#161616",
    "marginBottom": "24px"
}

CARD_HEADER_STYLE = {
    "fontSize": "1.1rem",
    "fontWeight": "600",
    "marginBottom": "16px",
    "color": "#333"
}
