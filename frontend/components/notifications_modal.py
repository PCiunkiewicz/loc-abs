"""Notification Modal Component for LocABS Application."""
import dash_bootstrap_components as dbc

def create_notification_modal(message="", is_error=False, is_open=False):
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
                    dbc.ModalTitle(
                        "Error" if is_error else "Success",
                        id="notification-modal-title" 
                    ),
                    close_button=True,
                ),
                dbc.ModalBody(
                    message,
                    id="notification-modal-body"  
                ),
                dbc.ModalFooter(
                    dbc.Button(
                        "Close",
                        id="close-notification-modal",
                        className="ms-auto",
                        n_clicks=0,
                    )
                ),
            ],
            id="notification-modal",
            is_open=is_open,
            centered=True,
            className="notification-error" if is_error else "notification-success",
        )