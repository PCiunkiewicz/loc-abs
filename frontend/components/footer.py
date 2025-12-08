"""Footer component for the Dash app."""

from dash import html
import dash_bootstrap_components as dbc


def create_footer() -> html.Div:
    """Create the footer component for the Dash app."""
    return dbc.Container(
        dbc.Row(
            dbc.Col(
                html.P(
                    '© 2025 LocABS. All rights reserved.',
                    className='text-center color-black',
                    style={'padding': '10px 0', 'font-size': '14px'},
                )
            )
        ),
        fluid=True,
        className='app-footer',
        style={'backgroundColor': '#f8f9fa', 'marginTop': '40px'},
    )
