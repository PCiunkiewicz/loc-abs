"""Accessible Tooltip Component for Dash Applications - WCAG 2.2."""

import dash_bootstrap_components as dbc
from dash import html


def create_tooltip(text: str, target_id: str, placement='top') -> dbc.Tooltip:
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


def create_info_icon_with_tooltip(label_text: str, tooltip_text: str, field_id: str):
    """Create a label with an accessible info icon and tooltip.

    Args:
        label_text: The visible label text
        tooltip_text: The tooltip help text
        field_id: Unique identifier for the field (used for ARIA and tooltip targeting)

    Returns:
        html.Div: Label with info icon and tooltip
    """
    tooltip_id = f'{field_id}-tooltip-icon'
    tooltip_content_id = f'{field_id}-tooltip-content'

    return html.Div(
        [
            html.Label(
                [
                    html.Span(label_text),
                    html.Span(
                        html.I(className='fa fa-info-circle'),
                        id=tooltip_id,
                        className='tooltip-icon',
                        tabIndex='0',
                        title=f'Help for {label_text}',
                    ),
                ],
                htmlFor=field_id,
                style={'display': 'flex', 'alignItems': 'center', 'gap': '4px'},
            ),
            # Hidden content for screen readers
            html.Span(tooltip_text, id=tooltip_content_id, className='sr-only'),
            # Visual tooltip for sighted users
            create_tooltip(tooltip_text, tooltip_id, placement='top'),
        ]
    )
