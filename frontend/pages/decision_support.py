"""Decision Support Page for Loc-ABS Application."""

import uuid

import dash_bootstrap_components as dbc
from dash import dcc, html, register_page

from components.bayesian_network import DashBNGraph
from components.tooltip import create_tooltip

register_page(__name__, path='/decision-support', name='Decision Support', title='Loc-ABS Decision Support')


def layout() -> html.Div:
    """Layout for the Decision Support page."""
    session_id = str(uuid.uuid4())
    return html.Div(
        [
            dbc.Row(
                [
                    # LEFT SIDEBAR
                    dbc.Col(
                        [
                            html.H5('Decision Support'),
                            html.P(
                                'Construct a new Bayesian Network from runs or load decision support for analysis.',
                                className='dv-sidebar-description',
                            ),
                            html.Div(
                                [
                                    html.Div(
                                        [
                                            dcc.Dropdown(
                                                id='dv-run-dropdown',
                                                options=[],
                                                placeholder='Select decision support',
                                                clearable=True,
                                            ),
                                        ],
                                        className='dv-sidebar-section',
                                    ),
                                    html.H5('Create new Bayesian Network', className='fw-bold'),
                                    html.Div(
                                        [
                                            dbc.Label(
                                                'Name', html_for='dv-name-input', className='dv-sidebar-form-label'
                                            ),
                                            html.I(
                                                className='fa fa-circle-question dv-tooltip-icon',
                                                id='dv-name-tooltip',
                                            ),
                                        ],
                                        className='dv-label-container',
                                    ),
                                    create_tooltip(
                                        'Give your decision support a unique name for easy identification',
                                        'dv-name-tooltip',
                                        placement='top',
                                    ),
                                    html.P(
                                        'Unique identifier for this decision support',
                                        className='dv-helper-text',
                                    ),
                                    dbc.Input(
                                        id='dv-name-input',
                                        type='text',
                                        placeholder='Decision Support Name',
                                        className='form-control',
                                    ),
                                    html.Div(
                                        [
                                            html.Div(
                                                [
                                                    dbc.Label(
                                                        'Run Selection',
                                                        html_for='dv-agent-dropdown',
                                                        className='dv-sidebar-form-label',
                                                    ),
                                                    html.I(
                                                        className='fa fa-circle-question dv-tooltip-icon',
                                                        id='dv-agent-tooltip',
                                                    ),
                                                ],
                                                className='dv-label-container',
                                            ),
                                            create_tooltip(
                                                'Select one or more runs to include in the Bayesian Network parameter learning',
                                                'dv-agent-tooltip',
                                                placement='top',
                                            ),
                                            html.P(
                                                'Data used to learn the parameters of the Bayesian Network',
                                                className='dv-helper-text',
                                            ),
                                            dcc.Dropdown(
                                                id='dv-agent-dropdown',
                                                options=[],
                                                placeholder='Select run(s)',
                                                multi=True,
                                            ),
                                        ],
                                        className='dv-sidebar-input-section',
                                    ),
                                    dbc.Button(
                                        'Learn Parameters',
                                        id='dv-run-btn',
                                        color='primary',
                                        className='dv-sidebar-run-btn',
                                    ),
                                ],
                                id='dv-run-form',
                            ),
                            html.Hr(),
                        ],
                        width=3,
                        className='dv-sidebar',
                    ),
                    # MAIN VISUALISATION AREA
                    dbc.Col(
                        DashBNGraph(session_id=session_id),
                        width=9,
                    ),
                ],
                className='g-4',
            ),
            # hidden store and init interval
        ],
        className='data-viz-page-container',
    )
