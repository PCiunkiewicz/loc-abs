"""Tooltip Component for Dash Applications."""
import dash_bootstrap_components as dbc

def create_tooltip(text: str, target_id: str) -> dbc.Tooltip:
    """Create a tooltip component."""
    return dbc.Tooltip(
        text,
        target=target_id,
        placement="top",
    )