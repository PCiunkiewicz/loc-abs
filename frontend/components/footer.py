"""Footer component for the Dash app."""

import dash_bootstrap_components as dbc
from dash import html


def create_footer() -> html.Div:
    """Create the footer component for the Dash app."""
    return dbc.Container(
        dbc.Row(
            dbc.Col(
                html.P(
                    '© 2026 Biometric Technologies Laboratory. All rights reserved.',
                    className='text-center color-black',
                    style={'padding': '1rem 0', 'fontSize': '0.8rem'},
                )
            )
        ),
        fluid=True,
        className='app-footer',
        style={'backgroundColor': '#f8f9fa'},
    )
