"""Reports Page for LocABS Application."""

from dash import html, register_page
import dash_bootstrap_components as dbc

register_page(__name__, path="/reports", name="Reports", title="LocABS · Reports")

layout = html.Div(
    [
        html.Div(
            [
                html.I(className='fa fa-file-alt', style={'fontSize': '4rem', 'color': '#000000', 'marginBottom': '1rem'}),
                html.H1('Reports', style={'fontSize': '2.5rem', 'fontWeight': 'bold', 'color': '#000000', 'marginBottom': '1rem'}),
                html.P(
                    'Generate comprehensive reports and analytics from your simulation data.',
                    style={'fontSize': '1.1rem', 'color': '#555555', 'marginBottom': '2rem'},
                ),
                dbc.Alert(
                    [
                        html.I(className='fa fa-info-circle me-2'),
                        'This page is under development. Report generation features will be available soon.',
                    ],
                    color='info',
                    className='d-flex align-items-center',
                    style={'maxWidth': '600px', 'margin': '0 auto'},
                ),
            ],
            style={
                'textAlign': 'center',
                'padding': '4rem 2rem',
                'backgroundColor': '#ffffff',
                'borderRadius': '8px',
                'boxShadow': '0 2px 8px rgba(0, 0, 0, 0.1)',
                'maxWidth': '800px',
                'margin': '0 auto',
            },
        ),
    ],
    style={
        'minHeight': 'calc(100vh - 150px)',
        'backgroundColor': '#f9f9f9',
        'padding': '4rem 2rem',
        'display': 'flex',
        'alignItems': 'center',
        'justifyContent': 'center',
    },
)
