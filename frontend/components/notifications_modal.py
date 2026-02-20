"""Notification Modal Component for LocABS Application - WCAG 2.2 Accessible."""

import dash_bootstrap_components as dbc
from dash import html


def create_notification_modal(_message='', is_error=False, is_open=False):
    """Create an accessible notification modal component.

    Args:
        message (str): The notification message to display.
        is_error (bool): Whether this is an error notification (affects styling).
        is_open (bool): Whether the modal should be open by default.

    Returns:
        dbc.Modal: An accessible Bootstrap modal component for notifications.
    """
    return dbc.Modal(
        [
            dbc.ModalHeader(
                html.Div(
                    [
                        html.Div(
                            [
                                html.I(
                                    id='notification-modal-icon',
                                    style={'fontSize': '2.5rem', 'marginBottom': '0.75rem'},
                                ),
                                html.H2(
                                    id='notification-modal-title',
                                    style={
                                        'fontSize': '1.35rem',
                                        'fontWeight': '600',
                                        'margin': '0',
                                        'marginTop': '0.25rem',
                                    },
                                ),
                            ],
                            style={'textAlign': 'center', 'padding': '0.75rem 0 0.5rem 0'},
                        ),
                    ],
                    style={'width': '100%'},
                    id='notification-modal-header',
                ),
                close_button=True,
                style={'border': 'none', 'paddingBottom': '0'},
            ),
            dbc.ModalBody(
                html.Div(
                    id='notification-modal-body',
                    style={
                        'fontSize': '1rem',
                        'textAlign': 'center',
                        'padding': '0.75rem 1.5rem 1.25rem 1.5rem',
                        'lineHeight': '1.6',
                        'color': '#475569',
                    },
                ),
                style={'paddingTop': '0'},
                id='notification-modal-description',
            ),
            dbc.ModalFooter(
                dbc.Button(
                    'Got it!',
                    id='close-notification-modal',
                    className='btn-primary',
                    n_clicks=0,
                    style={
                        'minWidth': '110px',
                        'fontWeight': '600',
                        'padding': '0.5rem 1.75rem',
                        'fontSize': '0.95rem',
                    },
                    title='Close notification',
                ),
                style={'border': 'none', 'justifyContent': 'center', 'padding': '0.75rem'},
            ),
        ],
        id='notification-modal',
        is_open=is_open,
        centered=True,
        className='notification-error' if is_error else 'notification-success',
        style={'borderRadius': '12px'},
        size='sm',
    )
