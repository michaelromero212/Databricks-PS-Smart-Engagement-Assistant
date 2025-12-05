import dash
from dash import html, callback, Input, Output, State
import dash_bootstrap_components as dbc

from src.dashboard.layout import create_layout
from src.dashboard.pages import executive, engagement, sentiment, automation, capacity, adoption

app = dash.Dash(
    __name__, 
    external_stylesheets=[
        dbc.themes.BOOTSTRAP, 
        dbc.icons.BOOTSTRAP,
        "https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap"
    ], 
    suppress_callback_exceptions=True
)
app.title = "Databricks PS Smart Engagement Assistant"

app.layout = create_layout(app)


# ============================================================================
# Page Routing
# ============================================================================

@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname == "/":
        return executive.layout
    elif pathname == "/engagement":
        return engagement.layout
    elif pathname == "/sentiment":
        return sentiment.layout
    elif pathname == "/automation":
        return automation.layout
    elif pathname == "/capacity":
        return capacity.layout
    elif pathname == "/adoption":
        return adoption.layout
    return html.Div(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ],
        className="p-3 bg-light rounded-3",
    )


# ============================================================================
# Navbar Toggle
# ============================================================================

@app.callback(
    Output("navbar-collapse", "is_open"),
    [Input("navbar-toggler", "n_clicks")],
    [State("navbar-collapse", "is_open")],
)
def toggle_navbar_collapse(n, is_open):
    if n:
        return not is_open
    return is_open


if __name__ == "__main__":
    app.run(debug=True, port=8050)
