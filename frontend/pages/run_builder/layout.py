"""Layout components for Run Builder page."""

import json
import dash_bootstrap_components as dbc
from dash import dcc, html

from components.notifications_modal import create_notification_modal
from utilities.resource_helpers import render_summary

from pages.run_builder.config import RESOURCES


def render_summary_view(resource_type, item):
    """Render a readable summary block for a resource item."""
    if not item:
        return html.Div()

    summary_rows = render_summary(resource_type, item)

    return dbc.Card(
        [
            html.Div(summary_rows, className='resource-summary'),
            html.Details(
                [
                    html.Summary('View Full Details'),
                    html.Pre(json.dumps(item, indent=2), className='json-display'),
                ],
                className='details-expandable',
            ),
        ],
        body=True,
        className='resource-summary-card',
    )


def create_resource_tab(resource_type, label=None):
    """Create a tab with dropdown, create button, and editable form area."""
    label = label or resource_type.replace('_', ' ').title()
    return dbc.Tab(
        label=label,
        tab_id=f'{resource_type}-tab',
        children=[
            html.Div(
                [
                    dbc.Row(
                        [
                            dbc.Col(
                                [
                                    dcc.Dropdown(
                                        id={'type': 'dropdown', 'resource': resource_type},
                                        options=[],
                                        placeholder=f'Select {label}',
                                        className='dropdown-standard',
                                    ),
                                ],
                                width=10,
                                className='dropdown-col',
                            ),
                            dbc.Col(
                                [
                                    html.Button(
                                        'Create',
                                        id={'type': 'create-btn', 'resource': resource_type},
                                        className='btn btn-primary',
                                    ),
                                ],
                                width=1,
                                className='dropdown-col',
                            ),
                        ],
                        className='dropdown-row',
                    ),
                    html.Div(id=f'{resource_type}-editable-fields', className='form-editable-fields'),
                ],
                className='p-3',
            )
        ],
    )


def create_stores_for_resource(resource_type):
    """Create all stores needed for a resource."""
    return html.Div(
        [
            dcc.Store(id={'type': 'resource-store', 'resource': resource_type}),
            dcc.Store(id={'type': 'original-data', 'resource': resource_type}),
            dcc.Store(id={'type': 'form-mode', 'resource': resource_type}, data={'mode': 'idle', 'resource_id': None}),
        ]
    )


def create_delete_confirmation_modal():
    """Create the delete confirmation modal."""
    return dbc.Modal(
        [
            dbc.ModalHeader(
                html.Div(
                    'Confirm Delete',
                    style={'fontSize': '1.3rem', 'fontWeight': 'bold', 'color': '#c62828'},
                ),
                close_button=True,
                style={'border': 'none', 'paddingBottom': '0'},
            ),
            dbc.ModalBody(
                html.Div(
                    id='delete-confirmation-message',
                    style={
                        'fontSize': '1.1rem',
                        'textAlign': 'center',
                        'padding': '1.5rem 1rem',
                        'lineHeight': '1.6',
                    },
                ),
                style={'paddingTop': '0.5rem'},
            ),
            dbc.ModalFooter(
                [
                    dbc.Button(
                        'Cancel',
                        id='cancel-delete-btn',
                        className='btn-secondary',
                        n_clicks=0,
                        style={'minWidth': '100px', 'fontWeight': '500', 'marginRight': '10px'},
                    ),
                    dbc.Button(
                        'Delete',
                        id='confirm-delete-btn',
                        className='btn-danger',
                        n_clicks=0,
                        style={'minWidth': '100px', 'fontWeight': '500'},
                    ),
                ],
                style={'border': 'none', 'justifyContent': 'center'},
            ),
        ],
        id='delete-confirmation-modal',
        is_open=False,
        centered=True,
        style={'borderRadius': '10px'},
        size='md',
    )


# Main page layout
layout = html.Div(
    [
        html.Div(
            [
                html.H1('Run Builder', className='page-title'),
                html.P('Create and manage simulation runs', className='page-subtitle'),
            ],
            className='page-header',
        ),
        dbc.Tabs(
            [
                dbc.Tab(
                    label='Scenario',
                    tab_id='scenario-tab',
                    children=[
                        html.Div(
                            [
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            [
                                                dcc.Dropdown(
                                                    id={'type': 'dropdown', 'resource': 'scenario'},
                                                    options=[],
                                                    placeholder='Select Scenario',
                                                    className='dropdown-standard',
                                                )
                                            ],
                                            width=10,
                                            className='dropdown-col',
                                        ),
                                        dbc.Col(
                                            [
                                                html.Button(
                                                    'Create',
                                                    id={'type': 'create-btn', 'resource': 'scenario'},
                                                    className='btn btn-primary',
                                                )
                                            ],
                                            width=1,
                                            className='dropdown-col',
                                        ),
                                    ],
                                    className='dropdown-row',
                                ),
                                html.Div(id='scenario-editable-fields', className='form-editable-fields'),
                                html.Div(
                                    dbc.Tabs(
                                        [
                                            create_resource_tab('virus', 'Virus Configuration'),
                                            create_resource_tab('prevention', 'Prevention Configuration'),
                                            create_resource_tab('simulation', 'Simulation Configuration'),
                                        ]
                                    ),
                                    id='scenario-child-tabs',
                                    style={'display': 'none'},
                                ),
                                html.Div(
                                    [
                                        html.Button('Save', id='scenario-save-btn', className='btn btn-primary'),
                                        html.Button(
                                            'Cancel', id='scenario-cancel-btn-bottom', className='btn btn-secondary'
                                        ),
                                    ],
                                    id='scenario-action-buttons',
                                    className='form-button-group',
                                    style={'display': 'none'},
                                ),
                            ],
                            className='p-3',
                        ),
                    ],
                ),
                create_resource_tab('agent_config', 'Agent Configuration'),
            ],
            id='main-tabs',
            active_tab='scenario-tab',
        ),
        # Stores for all resources
        *[create_stores_for_resource(r) for r in RESOURCES],
        create_notification_modal(),
        dcc.Store(id='notification-message-store'),
        dcc.Store(id='notification-type-store'),
        create_delete_confirmation_modal(),
        dcc.Store(id='delete-pending-resource'),
        dcc.Store(id='delete-pending-id'),
    ],
    className='page-container',
)
