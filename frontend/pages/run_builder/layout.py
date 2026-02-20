"""Layout components for Run Builder page."""

import json
import dash_bootstrap_components as dbc
from dash import dcc, html

from components.notifications_modal import create_notification_modal
from components.tooltip import create_tooltip
from utilities.resource_helpers import render_summary

from pages.run_builder.config import RESOURCES


def render_summary_view(resource_type, item):
    """Render a readable summary block for a resource item."""
    if not item:
        return html.Div(
            [
                html.Div(
                    [
                        html.I(className='fa fa-inbox fa-3x', style={'color': '#cbd5e0', 'marginBottom': '1rem'}),
                        html.H5('No Item Selected', style={'color': '#64748b', 'marginBottom': '0.5rem'}),
                        html.P(
                            f'Select a {resource_type.replace("_", " ")} from the dropdown above to view details.',
                            style={'color': '#94a3b8', 'fontSize': '0.875rem'},
                        ),
                    ],
                    className='empty-state',
                )
            ],
            style={'padding': '3rem 1rem', 'textAlign': 'center'},
        )

    summary_rows = render_summary(resource_type, item)

    return html.Div(
        [
            dbc.Card(
                [
                    dbc.CardHeader(
                        html.Div(
                            [
                                html.H5(
                                    [
                                        html.I(className='fa fa-info-circle me-2', style={'color': '#3b82f6'}),
                                        'Summary',
                                    ],
                                    style={'marginBottom': '0', 'fontSize': '1.1rem', 'fontWeight': '600'},
                                ),
                                html.I(
                                    className='fa fa-circle-question',
                                    id=f'{resource_type}-summary-help-icon',
                                    style={'color': '#94a3b8', 'cursor': 'pointer', 'fontSize': '1rem'},
                                ),
                                create_tooltip(
                                    f'Quick overview of the selected {resource_type.replace("_", " ")} configuration.',
                                    f'{resource_type}-summary-help-icon',
                                    placement='top',
                                ),
                            ],
                            style={'display': 'flex', 'justifyContent': 'space-between', 'alignItems': 'center'},
                        ),
                        style={'backgroundColor': '#f8fafc', 'borderBottom': '2px solid #e2e8f0'},
                    ),
                    dbc.CardBody(
                        [
                            html.Div(summary_rows, className='resource-summary-grid'),
                            html.Details(
                                [
                                    html.Summary(
                                        [
                                            html.I(className='fa fa-chevron-right me-2', style={'fontSize': '0.75rem'}),
                                            'View Full Details',
                                        ],
                                        style={'cursor': 'pointer', 'color': '#3b82f6', 'fontWeight': '500'},
                                    ),
                                    dbc.Card(
                                        dbc.CardBody(
                                            html.Pre(
                                                json.dumps(item, indent=2),
                                                className='json-display',
                                                style={
                                                    'backgroundColor': '#1e293b',
                                                    'color': '#e2e8f0',
                                                    'padding': '1rem',
                                                    'borderRadius': '6px',
                                                    'fontSize': '0.875rem',
                                                    'overflowX': 'auto',
                                                },
                                            ),
                                        ),
                                        className='mt-2',
                                    ),
                                ],
                                className='details-expandable',
                                style={'marginTop': '1rem'},
                            ),
                        ],
                    ),
                ],
                className='resource-summary-card',
                style={'boxShadow': '0 1px 3px rgba(0,0,0,0.1)', 'border': '1px solid #e2e8f0'},
            ),
        ]
    )


def create_resource_tab(resource_type, label=None):
    """Create a tab with dropdown, create button, and editable form area."""
    label = label or resource_type.replace('_', ' ').title()
    return dbc.Tab(
        label=label,
        tab_id=f'{resource_type}-tab',
        className='dash-tab',
        active_tab_class_name='dash-tab--selected',
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


def create_scenario_learn_more_modal():
    """Create the scenario learn more modal."""
    return dbc.Modal(
        [
            dbc.ModalHeader(
                html.Div(
                    [
                        html.I(className='fa fa-circle-info me-2', style={'color': '#3b82f6'}),
                        'Scenario Settings Guide',
                    ],
                    style={'fontSize': '1.4rem', 'fontWeight': '600'},
                ),
                close_button=True,
            ),
            dbc.ModalBody(
                [
                    html.Div(
                        [
                            html.H5('Outbreak Settings', style={'color': '#3b82f6', 'marginBottom': '0.75rem'}),
                            html.Ul(
                                [
                                    html.Li(
                                        [
                                            'Transmission Rate: ',
                                            html.Span(
                                                'How easily the infection spreads between people',
                                                style={'color': '#64748b'},
                                            ),
                                        ]
                                    ),
                                    html.Li(
                                        [
                                            'Incubation Period: ',
                                            html.Span(
                                                'Time between exposure and showing symptoms', style={'color': '#64748b'}
                                            ),
                                        ]
                                    ),
                                    html.Li(
                                        [
                                            'Recovery Time: ',
                                            html.Span(
                                                'How long it takes for infected people to recover',
                                                style={'color': '#64748b'},
                                            ),
                                        ]
                                    ),
                                    html.Li(
                                        [
                                            'Symptom Severity: ',
                                            html.Span(
                                                'How serious the symptoms are for infected individuals',
                                                style={'color': '#64748b'},
                                            ),
                                        ]
                                    ),
                                ],
                                style={'lineHeight': '1.8', 'marginBottom': '1.5rem'},
                            ),
                            html.H5('Protective Measures', style={'color': '#3b82f6', 'marginBottom': '0.75rem'}),
                            html.Ul(
                                [
                                    html.Li(
                                        [
                                            'Mask Effectiveness: ',
                                            html.Span('How well masks reduce transmission', style={'color': '#64748b'}),
                                        ]
                                    ),
                                    html.Li(
                                        [
                                            'Social Distancing: ',
                                            html.Span(
                                                'Minimum distance maintained between people', style={'color': '#64748b'}
                                            ),
                                        ]
                                    ),
                                    html.Li(
                                        [
                                            'Sanitization Frequency: ',
                                            html.Span(
                                                'How often surfaces and areas are cleaned', style={'color': '#64748b'}
                                            ),
                                        ]
                                    ),
                                    html.Li(
                                        [
                                            'Vaccination Rate: ',
                                            html.Span(
                                                'Percentage of participants who are vaccinated',
                                                style={'color': '#64748b'},
                                            ),
                                        ]
                                    ),
                                ],
                                style={'lineHeight': '1.8', 'marginBottom': '1.5rem'},
                            ),
                            html.H5('Simulation Settings', style={'color': '#3b82f6', 'marginBottom': '0.75rem'}),
                            html.Ul(
                                [
                                    html.Li(
                                        [
                                            'Duration: ',
                                            html.Span(
                                                'How long the simulation runs (in days)', style={'color': '#64748b'}
                                            ),
                                        ]
                                    ),
                                    html.Li(
                                        [
                                            'Time Step: ',
                                            html.Span(
                                                'Granularity of the simulation updates', style={'color': '#64748b'}
                                            ),
                                        ]
                                    ),
                                    html.Li(
                                        [
                                            'Random Seed: ',
                                            html.Span(
                                                'For reproducible results across runs', style={'color': '#64748b'}
                                            ),
                                        ]
                                    ),
                                ],
                                style={'lineHeight': '1.8'},
                            ),
                        ],
                        style={'fontSize': '0.95rem'},
                    ),
                ],
                style={'maxHeight': '60vh', 'overflowY': 'auto'},
            ),
            dbc.ModalFooter(
                dbc.Button(
                    'Got it!',
                    id='close-scenario-learn-more',
                    className='btn-primary',
                    n_clicks=0,
                    style={'minWidth': '100px', 'fontWeight': '500'},
                ),
                style={'border': 'none', 'justifyContent': 'center'},
            ),
        ],
        id='scenario-learn-more-modal',
        is_open=False,
        centered=True,
        size='lg',
        style={'borderRadius': '10px'},
    )


def create_agent_config_learn_more_modal():
    """Create the agent config learn more modal."""
    return dbc.Modal(
        [
            dbc.ModalHeader(
                html.Div(
                    [
                        html.I(className='fa fa-circle-info me-2', style={'color': '#3b82f6'}),
                        'Participant Settings Guide',
                    ],
                    style={'fontSize': '1.4rem', 'fontWeight': '600'},
                ),
                close_button=True,
            ),
            dbc.ModalBody(
                [
                    html.Div(
                        [
                            html.H5('Basic Configuration', style={'color': '#3b82f6', 'marginBottom': '0.75rem'}),
                            html.Ul(
                                [
                                    html.Li(
                                        [
                                            'Number of Participants: ',
                                            html.Span('Total people in the facility', style={'color': '#64748b'}),
                                        ]
                                    ),
                                    html.Li(
                                        [
                                            'Initial Infected: ',
                                            html.Span('How many people start infected', style={'color': '#64748b'}),
                                        ]
                                    ),
                                    html.Li(
                                        [
                                            'Age Distribution: ',
                                            html.Span(
                                                'Age groups present in the population', style={'color': '#64748b'}
                                            ),
                                        ]
                                    ),
                                ],
                                style={'lineHeight': '1.8', 'marginBottom': '1.5rem'},
                            ),
                            html.H5('Movement & Behavior', style={'color': '#3b82f6', 'marginBottom': '0.75rem'}),
                            html.Ul(
                                [
                                    html.Li(
                                        [
                                            'Movement Speed: ',
                                            html.Span('How fast participants move around', style={'color': '#64748b'}),
                                        ]
                                    ),
                                    html.Li(
                                        [
                                            'Activity Patterns: ',
                                            html.Span('Daily routines and schedules', style={'color': '#64748b'}),
                                        ]
                                    ),
                                    html.Li(
                                        [
                                            'Social Interaction: ',
                                            html.Span(
                                                'Frequency and duration of contact with others',
                                                style={'color': '#64748b'},
                                            ),
                                        ]
                                    ),
                                    html.Li(
                                        [
                                            'Room Occupancy: ',
                                            html.Span('Time spent in different areas', style={'color': '#64748b'}),
                                        ]
                                    ),
                                ],
                                style={'lineHeight': '1.8', 'marginBottom': '1.5rem'},
                            ),
                            html.H5('Compliance Settings', style={'color': '#3b82f6', 'marginBottom': '0.75rem'}),
                            html.Ul(
                                [
                                    html.Li(
                                        [
                                            'Mask Compliance: ',
                                            html.Span(
                                                'Percentage who consistently wear masks', style={'color': '#64748b'}
                                            ),
                                        ]
                                    ),
                                    html.Li(
                                        [
                                            'Distance Compliance: ',
                                            html.Span(
                                                'How well people maintain social distance', style={'color': '#64748b'}
                                            ),
                                        ]
                                    ),
                                    html.Li(
                                        [
                                            'Hygiene Compliance: ',
                                            html.Span(
                                                'Frequency of handwashing and sanitization', style={'color': '#64748b'}
                                            ),
                                        ]
                                    ),
                                ],
                                style={'lineHeight': '1.8'},
                            ),
                        ],
                        style={'fontSize': '0.95rem'},
                    ),
                ],
                style={'maxHeight': '60vh', 'overflowY': 'auto'},
            ),
            dbc.ModalFooter(
                dbc.Button(
                    'Got it!',
                    id='close-agent-config-learn-more',
                    className='btn-primary',
                    n_clicks=0,
                    style={'minWidth': '100px', 'fontWeight': '500'},
                ),
                style={'border': 'none', 'justifyContent': 'center'},
            ),
        ],
        id='agent-config-learn-more-modal',
        is_open=False,
        centered=True,
        size='lg',
        style={'borderRadius': '10px'},
    )


# Main page layout
layout = html.Div(
    [
        # Page Title and Help Button
        html.Div(
            [
                html.Div(
                    [
                        html.H6('Scenario & Participant Builder', className='page-title'),
                        html.P(
                            'Create and configure simulation scenarios and participant behaviors for your facility simulations.',
                            className='page-subtitle',
                        ),
                    ],
                    style={'flex': '1'},
                ),
                html.Button(
                    [html.I(className='fa fa-question-circle me-2'), 'How to Use'],
                    id='scenario-builder-how-to-btn',
                    className='btn btn-outline-primary',
                ),
            ],
            style={
                'display': 'flex',
                'alignItems': 'center',
                'justifyContent': 'space-between',
                'marginBottom': '.5rem',
            },
        ),
        # How-to Modal
        dbc.Modal(
            [
                dbc.ModalHeader(dbc.ModalTitle('How to Use the Scenario & Participant Builder')),
                dbc.ModalBody(
                    [
                        html.H5('Managing Resources', className='mt-3 mb-3'),
                        html.P(
                            'This builder helps you create, edit, and manage scenarios and participant configurations. Follow these steps to work with your resources:',
                            className='mb-4',
                        ),
                        # Create Resource
                        html.Div(
                            [
                                html.Div(
                                    [
                                        html.Div(
                                            '1',
                                            className='how-to-step-number',
                                        ),
                                        html.Div(
                                            [
                                                html.H6('Creating a New Resource', className='mb-2'),
                                                html.P(
                                                    [
                                                        html.I(className='fa fa-plus-circle me-2 text-success'),
                                                        'Click the ',
                                                        html.Strong('"Create New"'),
                                                        ' button next to the dropdown menu.',
                                                    ],
                                                    className='mb-2',
                                                ),
                                                html.P(
                                                    [
                                                        html.I(className='fa fa-edit me-2 text-success'),
                                                        'Fill in all required fields (marked with ',
                                                        html.Span(
                                                            '*', style={'color': '#dc3545', 'fontWeight': 'bold'}
                                                        ),
                                                        ').',
                                                    ],
                                                    className='mb-2',
                                                ),
                                                html.P(
                                                    [
                                                        html.I(className='fa fa-save me-2 text-success'),
                                                        'Click ',
                                                        html.Strong('"Save"'),
                                                        ' to create your resource, or ',
                                                        html.Strong('"Cancel"'),
                                                        ' to discard changes.',
                                                    ],
                                                    className='mb-0',
                                                ),
                                            ],
                                            style={'flex': '1'},
                                        ),
                                    ],
                                    className='how-to-step',
                                ),
                                # Edit Resource
                                html.Div(
                                    [
                                        html.Div(
                                            '2',
                                            className='how-to-step-number',
                                        ),
                                        html.Div(
                                            [
                                                html.H6('Editing an Existing Resource', className='mb-2'),
                                                html.P(
                                                    [
                                                        html.I(className='fa fa-list me-2 text-primary'),
                                                        'Select a resource from the dropdown menu.',
                                                    ],
                                                    className='mb-2',
                                                ),
                                                html.P(
                                                    [
                                                        html.I(className='fa fa-pencil me-2 text-primary'),
                                                        'Click the ',
                                                        html.Strong('"Edit"'),
                                                        ' button to modify the resource details.',
                                                    ],
                                                    className='mb-2',
                                                ),
                                                html.P(
                                                    [
                                                        html.I(className='fa fa-check me-2 text-primary'),
                                                        'Make your changes and click ',
                                                        html.Strong('"Save"'),
                                                        ' to update, or ',
                                                        html.Strong('"Cancel"'),
                                                        ' to revert.',
                                                    ],
                                                    className='mb-0',
                                                ),
                                            ],
                                            style={'flex': '1'},
                                        ),
                                    ],
                                    className='how-to-step',
                                ),
                                # Delete Resource
                                html.Div(
                                    [
                                        html.Div(
                                            '3',
                                            className='how-to-step-number',
                                        ),
                                        html.Div(
                                            [
                                                html.H6('Deleting a Resource', className='mb-2'),
                                                html.P(
                                                    [
                                                        html.I(className='fa fa-mouse-pointer me-2 text-danger'),
                                                        'Select the resource you want to delete from the dropdown.',
                                                    ],
                                                    className='mb-2',
                                                ),
                                                html.P(
                                                    [
                                                        html.I(className='fa fa-trash me-2 text-danger'),
                                                        'Click the ',
                                                        html.Strong('"Delete"'),
                                                        ' button.',
                                                    ],
                                                    className='mb-2',
                                                ),
                                                html.P(
                                                    [
                                                        html.I(className='fa fa-exclamation-triangle me-2 text-danger'),
                                                        'Confirm your action in the popup dialog. ',
                                                        html.Span(
                                                            'This cannot be undone!',
                                                            style={'fontWeight': 'bold', 'color': '#dc3545'},
                                                        ),
                                                    ],
                                                    className='mb-0',
                                                ),
                                            ],
                                            style={'flex': '1'},
                                        ),
                                    ],
                                    className='how-to-step',
                                ),
                                # Clone Resource
                                html.Div(
                                    [
                                        html.Div(
                                            '4',
                                            className='how-to-step-number',
                                        ),
                                        html.Div(
                                            [
                                                html.H6('Cloning a Resource', className='mb-2'),
                                                html.P(
                                                    [
                                                        html.I(className='fa fa-list me-2 text-info'),
                                                        'Select the resource you want to duplicate from the dropdown.',
                                                    ],
                                                    className='mb-2',
                                                ),
                                                html.P(
                                                    [
                                                        html.I(className='fa fa-copy me-2 text-info'),
                                                        'Click the ',
                                                        html.Strong('"Clone"'),
                                                        ' button to create a copy.',
                                                    ],
                                                    className='mb-2',
                                                ),
                                                html.P(
                                                    [
                                                        html.I(className='fa fa-edit me-2 text-info'),
                                                        'The cloned resource will open in edit mode with all the same settings. Give it a new name and modify as needed.',
                                                    ],
                                                    className='mb-2',
                                                ),
                                                html.P(
                                                    [
                                                        html.I(className='fa fa-save me-2 text-info'),
                                                        'Click ',
                                                        html.Strong('"Save"'),
                                                        ' to create the new resource based on the clone.',
                                                    ],
                                                    className='mb-0',
                                                ),
                                            ],
                                            style={'flex': '1'},
                                        ),
                                    ],
                                    className='how-to-step',
                                ),
                            ],
                            className='mb-3',
                        ),
                        html.Hr(),
                        html.Div(
                            [
                                html.I(className='fa fa-lightbulb text-warning me-2'),
                                html.Strong('Tips: '),
                                html.Ul(
                                    [
                                        html.Li(
                                            'Fields with green borders are valid, red borders indicate errors or missing information.'
                                        ),
                                        html.Li(
                                            'You can expand the "View Full Details" section to see the complete configuration in JSON format.'
                                        ),
                                        html.Li(
                                            'Start with STEP 1 to define your scenario, then move to STEP 2 to configure participants.'
                                        ),
                                    ],
                                    style={'marginTop': '0.5rem', 'marginBottom': '0'},
                                ),
                            ],
                            className='alert alert-info',
                        ),
                    ]
                ),
                dbc.ModalFooter(dbc.Button('Got it!', id='scenario-builder-how-to-close', className='btn-primary')),
            ],
            id='scenario-builder-how-to-modal',
            size='lg',
            is_open=False,
        ),
        dbc.Tabs(
            [
                dbc.Tab(
                    label='STEP 1: Define Your Scenario',
                    tab_id='scenario-tab',
                    label_style={
                        'padding': '1rem 2rem',
                        'fontSize': '0.95rem',
                        'color': '#64748b',
                        'borderBottom': 'none',
                    },
                    active_label_style={
                        'backgroundColor': '#3b82f6',
                        'color': '#ffffff',
                        'borderRadius': '8px 8px 0 0',
                        'fontWeight': '600',
                    },
                    children=[
                        html.Div(
                            [
                                html.Div(
                                    [
                                        html.P(
                                            'Set up your simulation scenario including outbreak conditions, protective measures, and simulation settings. '
                                            'Choose an existing scenario or create a new one to customize infection parameters, prevention strategies, and how the simulation runs.',
                                            className='step-description',
                                            style={
                                                'margin': '0 0 1rem 0',
                                                'color': '#64748b',
                                                'fontSize': '0.95rem',
                                                'lineHeight': '1.6',
                                            },
                                        ),
                                        html.Button(
                                            [
                                                html.I(className='fa fa-circle-info me-2'),
                                                'Learn More About Scenario Settings',
                                            ],
                                            id='scenario-learn-more-btn',
                                            className='btn btn-link learn-more-btn',
                                            style={
                                                'padding': '0.25rem 0.5rem',
                                                'fontSize': '0.9rem',
                                                'textDecoration': 'none',
                                                'marginBottom': '1rem',
                                            },
                                        ),
                                    ],
                                ),
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            [
                                                dcc.Dropdown(
                                                    id={'type': 'dropdown', 'resource': 'scenario'},
                                                    options=[],
                                                    placeholder='Choose an existing scenario or create a new one',
                                                    className='dropdown-standard',
                                                )
                                            ],
                                            width=9,
                                            className='dropdown-col',
                                        ),
                                        dbc.Col(
                                            [
                                                html.Button(
                                                    'Create New',
                                                    id={'type': 'create-btn', 'resource': 'scenario'},
                                                    className='btn btn-primary',
                                                )
                                            ],
                                            width=2,
                                            className='dropdown-col',
                                        ),
                                    ],
                                    className='dropdown-row',
                                ),
                                html.Div(id='scenario-editable-fields', className='form-editable-fields'),
                                html.Div(
                                    dbc.Tabs(
                                        [
                                            create_resource_tab('virus', 'Outbreak Settings'),
                                            create_resource_tab('prevention', 'Protective Measures'),
                                            create_resource_tab('simulation', 'Simulation Settings'),
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
                dbc.Tab(
                    label='STEP 2: Configure Your Participants',
                    tab_id='agent_config-tab',
                    label_style={
                        'padding': '1rem 2rem',
                        'fontSize': '0.95rem',
                        'color': '#64748b',
                        'borderBottom': 'none',
                    },
                    active_label_style={
                        'backgroundColor': '#3b82f6',
                        'color': '#ffffff',
                        'borderRadius': '8px 8px 0 0',
                        'fontWeight': '600',
                    },
                    children=[
                        html.Div(
                            [
                                html.Div(
                                    [
                                        html.P(
                                            'Define the people in your facility and how they behave. '
                                            'Configure the number of participants, their movement patterns, social interactions, and compliance with protective measures. '
                                            'Select an existing configuration or create a new one to customize participant behavior.',
                                            className='step-description',
                                            style={
                                                'margin': '0 0 1rem 0',
                                                'color': '#64748b',
                                                'fontSize': '0.95rem',
                                                'lineHeight': '1.6',
                                            },
                                        ),
                                        html.Button(
                                            [
                                                html.I(className='fa fa-circle-info me-2'),
                                                'Learn More About Participant Settings',
                                            ],
                                            id='agent-config-learn-more-btn',
                                            className='btn btn-link learn-more-btn',
                                            style={
                                                'padding': '0.25rem 0.5rem',
                                                'fontSize': '0.9rem',
                                                'textDecoration': 'none',
                                                'marginBottom': '1rem',
                                            },
                                        ),
                                    ],
                                ),
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            [
                                                dcc.Dropdown(
                                                    id={'type': 'dropdown', 'resource': 'agent_config'},
                                                    options=[],
                                                    placeholder='Choose an existing participant setup or create a new one',
                                                    className='dropdown-standard',
                                                ),
                                            ],
                                            width=9,
                                            className='dropdown-col',
                                        ),
                                        dbc.Col(
                                            [
                                                html.Button(
                                                    'Create New',
                                                    id={'type': 'create-btn', 'resource': 'agent_config'},
                                                    className='btn btn-primary',
                                                ),
                                            ],
                                            width=2,
                                            className='dropdown-col',
                                        ),
                                    ],
                                    className='dropdown-row',
                                ),
                                html.Div(id='agent_config-editable-fields', className='form-editable-fields'),
                            ],
                            className='p-3',
                        ),
                    ],
                ),
            ],
            id='main-tabs',
            active_tab='scenario-tab',
            style={'width': '100%'},
        ),
        # Stores for all resources
        *[create_stores_for_resource(r) for r in RESOURCES],
        create_notification_modal(),
        dcc.Store(id='notification-message-store'),
        dcc.Store(id='notification-type-store'),
        create_delete_confirmation_modal(),
        dcc.Store(id='delete-pending-resource'),
        dcc.Store(id='delete-pending-id'),
        create_scenario_learn_more_modal(),
        create_agent_config_learn_more_modal(),
        # Completion tracking
        dcc.Store(id='scenario-agent-completion-store', data={'scenario_ready': False, 'agent_ready': False}),
        # Completion Modal
        dbc.Modal(
            [
                dbc.ModalHeader(
                    html.Div(
                        [
                            html.I(
                                className='fa fa-check-circle me-2', style={'color': '#28a745', 'fontSize': '1.5rem'}
                            ),
                            'Setup Complete!',
                        ],
                        style={'display': 'flex', 'alignItems': 'center'},
                    ),
                    close_button=True,
                ),
                dbc.ModalBody(
                    [
                        html.Div(
                            [
                                html.P(
                                    'You have successfully configured both your scenario and participant settings. '
                                    'Your simulation is ready to run!',
                                    style={
                                        'color': '#6c757d',
                                        'fontSize': '1rem',
                                        'lineHeight': '1.6',
                                        'marginBottom': '0.75rem',
                                    },
                                ),
                                html.H6(
                                    'What would you like to do next?',
                                    style={'color': '#495057', 'marginBottom': '0.5rem'},
                                ),
                            ],
                            style={'textAlign': 'center'},
                        ),
                    ]
                ),
                dbc.ModalFooter(
                    [
                        dbc.Button(
                            [
                                html.I(className='fa fa-edit me-2'),
                                'Keep Editing',
                            ],
                            id='completion-keep-editing-btn',
                            className='btn-secondary',
                            style={'minWidth': '150px'},
                        ),
                        dbc.Button(
                            [
                                html.I(className='fa fa-chart-line me-2'),
                                'Visualise Results',
                            ],
                            id='completion-go-to-viz-btn',
                            href='/data-viz',
                            className='btn-primary',
                            style={'minWidth': '150px'},
                        ),
                    ],
                    style={'justifyContent': 'center', 'gap': '1rem'},
                ),
            ],
            id='scenario-agent-completion-modal',
            is_open=False,
            centered=True,
            size='md',
        ),
    ],
    className='page-container',
)
