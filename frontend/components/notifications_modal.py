"""Notification Modal Component for LocABS Application."""

import dash_bootstrap_components as dbc
from dash import html


def create_notification_modal(_message='', is_error=False, is_open=False):
    """Create a notification modal component.

    Args:
        message (str): The notification message to display.
        is_error (bool): Whether this is an error notification (affects styling).
        is_open (bool): Whether the modal should be open by default.

    Returns:
        dbc.Modal: A Bootstrap modal component for notifications.
    """
    return dbc.Modal(
        [
            dbc.ModalHeader(
                html.Div(
                    [
                        html.Span(id='notification-modal-title', style={'fontSize': '1.3rem', 'fontWeight': 'bold'}),
                    ],
                    style={'width': '100%', 'textAlign': 'center'},
                ),
                close_button=True,
                style={'border': 'none', 'paddingBottom': '0'},
            ),
            dbc.ModalBody(
                html.Div(
                    id='notification-modal-body',
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
                dbc.Button(
                    'OK',
                    id='close-notification-modal',
                    className='btn-primary',
                    n_clicks=0,
                    style={
                        'minWidth': '100px',
                        'fontWeight': '500',
                    },
                ),
                style={'border': 'none', 'justifyContent': 'center'},
            ),
        ],
        id='notification-modal',
        is_open=is_open,
        centered=True,
        className='notification-error' if is_error else 'notification-success',
        style={'borderRadius': '10px'},
        size='md',
    )
