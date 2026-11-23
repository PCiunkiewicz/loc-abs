"""Resource Form Component for Loc-ABS Application."""

from dash import dcc, html

from components.tooltip import create_tooltip
from utilities.types.forms import Field


def render_resource_form(
    resource: str, fields: list[Field], values: dict | None = None, readonly: bool = True
) -> html.Div:
    """Render a resource form with given fields and values.

    Args:
        resource (str): The type of resource (e.g., "location", "user").
        fields (list): List of field definitions. Each field is a dict with keys
        values (dict, optional): Dictionary of field values. Defaults to None.
        readonly (bool, optional): If True, fields are read-only. Defaults to True.

    Returns:
        html.Div: A Dash HTML Div containing the form.
    """
    values = values or {}
    form_items = []
    for field in fields:
        key = field['id'].get('field') if isinstance(field['id'], dict) else field['id']
        value = values.get(key, None)

        # If a custom component function is provided, use it
        if (component := field.get('component')) and callable(component):
            form_items.append(component(readonly=readonly, value=value))
            continue

        label = field.get('label', '')
        field_type = field.get('type', 'text')
        class_name = field.get('css_class', 'form-input')
        tooltip_text = field.get('tooltip', '')

        if field_type == 'dropdown':
            form_items.append(
                html.Div(
                    [
                        html.Div(
                            [
                                html.Label(label, className='form-label'),
                                html.I(
                                    className='fa fa-circle-question ms-2',
                                    id=f'{resource}-{key}-tooltip',
                                    style={'color': '#94a3b8', 'cursor': 'pointer', 'fontSize': '0.875rem'},
                                )
                                if tooltip_text
                                else None,
                            ],
                            style={'display': 'flex', 'alignItems': 'center'},
                        ),
                        create_tooltip(
                            tooltip_text,
                            f'{resource}-{key}-tooltip',
                            placement='top',
                        )
                        if tooltip_text
                        else None,
                        dcc.Dropdown(
                            id=field['id'],
                            options=field.get('options', []),
                            value=value,
                            className=class_name,
                            disabled=readonly,
                        ),
                    ]
                )
            )
        elif field_type == 'radio':
            form_items.append(
                html.Div(
                    [
                        html.Div(
                            [
                                html.Label(label, className='form-label'),
                                html.I(
                                    className='fa fa-circle-question ms-2',
                                    id=f'{resource}-{key}-tooltip',
                                    style={'color': '#94a3b8', 'cursor': 'pointer', 'fontSize': '0.875rem'},
                                )
                                if tooltip_text
                                else None,
                            ],
                            style={'display': 'flex', 'alignItems': 'center'},
                        ),
                        create_tooltip(
                            tooltip_text,
                            f'{resource}-{key}-tooltip',
                            placement='top',
                        )
                        if tooltip_text
                        else None,
                        dcc.RadioItems(
                            id=field['id'],
                            options=field.get('options', []),
                            value=value,
                            className='form-radio-items',
                            inline=True,
                        ),
                    ]
                )
            )
        else:
            input_props = {
                'id': field['id'],
                'type': field_type,
                'value': value,
                'className': class_name,
                'disabled': readonly,
            }
            for prop in ['min', 'max', 'step']:
                if prop in field:
                    input_props[prop] = field[prop]

            form_items.append(
                html.Div(
                    [
                        html.Div(
                            [
                                html.Label(label, className='form-label'),
                                html.I(
                                    className='fa fa-circle-question ms-2',
                                    id=f'{resource}-{key}-tooltip',
                                    style={'color': '#94a3b8', 'cursor': 'pointer', 'fontSize': '0.875rem'},
                                )
                                if tooltip_text
                                else None,
                            ],
                            style={'display': 'flex', 'alignItems': 'center'},
                        ),
                        create_tooltip(
                            tooltip_text,
                            f'{resource}-{key}-tooltip',
                            placement='top',
                        )
                        if tooltip_text
                        else None,
                        dcc.Input(**input_props),
                    ]
                ),
            )

    return html.Div(form_items, className='resource-form-container')
