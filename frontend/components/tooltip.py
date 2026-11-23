"""Accessible Tooltip Component for Dash Applications - WCAG 2.2."""

from typing import Literal

import dash_bootstrap_components as dbc
from dash import html

Placement = Literal['top', 'bottom', 'left', 'right']


def create_tooltip(text: str, target_id: str, placement: Placement = 'top') -> dbc.Tooltip:
    """Create an accessible tooltip component.

    Args:
        text: Tooltip content text
        target_id: ID of the element to attach tooltip to
        placement: Tooltip placement ('top', 'bottom', 'left', 'right')

    Returns:
        dbc.Tooltip: Accessible tooltip component
    """
    return dbc.Tooltip(
        text,
        target=target_id,
        placement=placement,
    )


def tooltip_icon(text: str, tooltip_id: str) -> html.I | None:
    """Create a label with an accessible info icon and tooltip."""
    if text:
        icon = html.I(
            className='fa fa-circle-question ms-2',
            id=tooltip_id,
            style={'color': '#94a3b8', 'cursor': 'pointer', 'fontSize': '0.875rem'},
        )
        create_tooltip(text, tooltip_id, placement='top')
        return icon

    return None
