"""Resource Form Component for LocABS Application."""

from dash import html, dcc


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
        pm_id = field['id']
        dom_id = pm_id['field']

        # If a custom component function is provided, use it
        if 'component' in field and callable(field['component']):
            # Pass readonly and value to the component
            form_items.append(field['component'](readonly=readonly, value=values.get(dom_id, None)))
            continue

        label = field.get('label', '')
        field_type = field.get('type', 'text')
        class_name = field.get('className', 'form-input')

        if field_type == 'dropdown':
            form_items.append(
                html.Div(
                    [
                        html.Label(label, className='form-label'),
                        dcc.Dropdown(
                            id=pm_id,
                            options=field.get('options', []),
                            value=values.get(dom_id, None),
                            placeholder=field.get('placeholder', ''),
                            className=class_name,
                            disabled=readonly,
                        ),
                    ]
                )
            )
        else:
            input_props = {
                'id': pm_id,
                'type': field_type,
                'value': values.get(dom_id, ''),
                'placeholder': field.get('placeholder', ''),
                'className': class_name,
                'disabled': readonly,
            }
            for prop in ['min', 'max', 'step', 'pattern']:
                if prop in field:
                    input_props[prop] = field[prop]

            form_items.append(html.Div([html.Label(label, className='form-label'), dcc.Input(**input_props)]))

    return html.Div(form_items, className='resource-form-container')
