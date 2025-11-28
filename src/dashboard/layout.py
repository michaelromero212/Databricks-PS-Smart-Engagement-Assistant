from dash import html, dcc
import dash_bootstrap_components as dbc
from src.dashboard.styles import HEADER_STYLE, NAV_LINK_STYLE

def create_layout(app):
    navbar = dbc.Navbar(
        dbc.Container(
            [
                html.A(
                    dbc.Row(
                        [
                            dbc.Col(html.Img(src="/assets/logo.png", height="30px")), # Placeholder
                            dbc.Col(dbc.NavbarBrand("PS Smart Engagement Assistant", className="ms-2")),
                        ],
                        align="center",
                        className="g-0",
                    ),
                    href="/",
                    style={"textDecoration": "none"},
                ),
                dbc.NavbarToggler(id="navbar-toggler", n_clicks=0),
                dbc.Collapse(
                    dbc.Nav(
                        [
                            dbc.NavItem(dbc.NavLink("Executive Summary", href="/", active="exact")),
                            dbc.NavItem(dbc.NavLink("Engagement Metrics", href="/engagement", active="exact")),
                            dbc.NavItem(dbc.NavLink("Sentiment Analysis", href="/sentiment", active="exact")),
                            dbc.NavItem(dbc.NavLink("Automation Ops", href="/automation", active="exact")),
                            dbc.NavItem(dbc.NavLink("Team Capacity", href="/capacity", active="exact")),
                            dbc.NavItem(dbc.NavLink("Adoption", href="/adoption", active="exact")),
                        ],
                        className="ms-auto",
                        navbar=True,
                    ),
                    id="navbar-collapse",
                    navbar=True,
                ),
            ]
        ),
        color="dark",
        dark=True,
        className="mb-4",
    )

    content = dbc.Container(id="page-content", fluid=True)

    return html.Div([
        dcc.Location(id="url", refresh=False),
        navbar,
        content
    ])
