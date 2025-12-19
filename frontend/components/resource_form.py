"""Resource Form Component for LocABS Application."""

from dash import html, dcc
from components.tooltip import create_tooltip


def render_resource_form(resource_type, fields, values=None, readonly=True):
    """Render a resource form with given fields and values.

    Args:
        resource_type (str): The type of resource (e.g., "location", "user").
        fields (list): List of field definitions. Each field is a dict with keys:
                       'id', 'label', 'type', 'placeholder', 'minLength', 'maxLength', 'pattern'.
        values (dict, optional): Dictionary of field values. Defaults to None.
        readonly (bool, optional): If True, fields are read-only. Defaults to True.

    Returns:
        html.Div: A Dash HTML Div containing the form.
    """
    values = values or {}
    form_items = []
    for field in fields:
        if 'section_label' in field:
            form_items.append(html.H5(field['section_label'], className='form-section-label'))
            continue

        field_id = field.get('id')
        if isinstance(field_id, dict):
            field_key = field_id.get('field')
        else:
            field_key = field_id  # simple id (rare)

        field_value = values.get(field_key, None)

        # If a custom component function is provided, use it
        if 'component' in field and callable(field['component']):
            # Pass readonly and value to the component
            form_items.append(field['component'](readonly=readonly, value=field_value))
            continue

        label = field.get('label', '')
        field_type = field.get('type', 'text')
        class_name = field.get('className', 'form-input')
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
                                    id=f'{resource_type}-{field_key}-tooltip',
                                    style={'color': '#94a3b8', 'cursor': 'pointer', 'fontSize': '0.875rem'},
                                )
                                if tooltip_text
                                else None,
                            ],
                            style={'display': 'flex', 'alignItems': 'center'},
                        ),
                        create_tooltip(
                            tooltip_text,
                            f'{resource_type}-{field_key}-tooltip',
                            placement='top',
                        )
                        if tooltip_text
                        else None,
                        dcc.Dropdown(
                            id=field_id,
                            options=field.get('options', []),
                            value=field_value,
                            placeholder=field.get('placeholder', ''),
                            className=class_name,
                            disabled=readonly,
                            multi=field.get('multi', False),
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
                                    id=f'{resource_type}-{field_key}-tooltip',
                                    style={'color': '#94a3b8', 'cursor': 'pointer', 'fontSize': '0.875rem'},
                                )
                                if tooltip_text
                                else None,
                            ],
                            style={'display': 'flex', 'alignItems': 'center'},
                        ),
                        create_tooltip(
                            tooltip_text,
                            f'{resource_type}-{field_key}-tooltip',
                            placement='top',
                        )
                        if tooltip_text
                        else None,
                        dcc.RadioItems(
                            id=field_id,
                            options=field.get('options', []),
                            value=field_value,
                            className='form-radio-items',
                            inline=field.get('inline', True),
                        ),
                    ]
                )
            )
        else:
            input_props = {
                'id': field_id,
                'type': field_type,
                'value': field_value,
                'placeholder': field.get('placeholder', ''),
                'className': class_name,
                'disabled': readonly,
            }
            for prop in ['min', 'max', 'step', 'pattern']:
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
                                    id=f'{resource_type}-{field_key}-tooltip',
                                    style={'color': '#94a3b8', 'cursor': 'pointer', 'fontSize': '0.875rem'},
                                )
                                if tooltip_text
                                else None,
                            ],
                            style={'display': 'flex', 'alignItems': 'center'},
                        ),
                        create_tooltip(
                            tooltip_text,
                            f'{resource_type}-{field_key}-tooltip',
                            placement='top',
                        )
                        if tooltip_text
                        else None,
                        dcc.Input(**input_props),
                    ]
                ),
            )

    return html.Div(form_items, className='resource-form-container')
