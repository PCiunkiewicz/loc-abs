"""Decision Support Page for LocABS Application."""

from dash import html, register_page
import dash_bootstrap_components as dbc

register_page(__name__, path='/decision-support', name='Decision Support', title='LocABS Aú Decision Support')

layout = html.Div(
    [
        html.Div(
            [
                html.H1('Decision Support', className='page-title'),
                html.P(
                    'Review scenario outputs and guide next steps. This area can be expanded with insights, actions, '
                    'and reporting tailored to your current run.',
                    className='text-muted',
                ),
                dbc.Alert('Decision support content coming soon.', color='info', className='decision-support-alert'),
            ],
            className='page-header',
        )
    ],
    className='page-container',
)
