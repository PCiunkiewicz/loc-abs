"""Run Builder Page for LocABS Application."""

from dash import html, dcc, register_page, callback, Output, Input, State, ctx, ALL, no_update
from dash.exceptions import PreventUpdate
import json
import dash_bootstrap_components as dbc
from components.resource_form import render_resource_form
from components.input_components import create_mask_input, create_vaccine_type

# from components.notifications_modal import create_notification_modal
from utilities import api

register_page(__name__, path='/run-builder', name='Run Builder', title='LocABS · Run Builder')

virus_fields = [
    {'id': 'virus-name', 'label': 'Name', 'type': 'text', 'className': 'form-input'},
    {
        'id': 'virus-attack-rate',
        'label': 'Attack Rate',
        'type': 'number',
        'min': 0,
        'max': 1,
        'step': 0.001,
        'className': 'form-input',
    },
    {
        'id': 'virus-infection-rate',
        'label': 'Infection Rate',
        'type': 'number',
        'min': 0,
        'max': 1,
        'step': 0.001,
        'className': 'form-input',
    },
    {
        'id': 'virus-fatality-rate',
        'label': 'Fatality Rate',
        'type': 'number',
        'min': 0,
        'max': 1,
        'step': 0.001,
        'className': 'form-input',
    },
]

simulation_fields = [
    {'id': 'simulation-name', 'label': 'Name', 'type': 'text', 'className': 'form-input'},
    {
        'id': 'map-file-dropdown',
        'label': 'Map File',
        'type': 'dropdown',
        'options': [],
        'className': 'dropdown-standard',
    },
    {
        'id': 'xy-scale-input',
        'label': 'XY Scale',
        'type': 'number',
        'min': 1.0,
        'max': 1000000.0,
        'step': 0.01,
        'className': 'form-input',
    },
    {
        'id': 'time-step-input',
        'label': 'Time Step (s)',
        'type': 'dropdown',
        'options': [
            {'label': '1 second', 'value': 1},
            {'label': '5 seconds', 'value': 5},
            {'label': '10 seconds', 'value': 10},
            {'label': '30 seconds', 'value': 30},
            {'label': '1 minute (60s)', 'value': 60},
            {'label': '5 minutes (300s)', 'value': 300},
            {'label': '10 minutes (600s)', 'value': 600},
            {'label': '30 minutes (1800s)', 'value': 1800},
            {'label': '1 hour (3600s)', 'value': 3600},
        ],
        'className': 'dropdown-standard',
    },
    {
        'id': 'save-resolution-input',
        'label': 'Save Resolution',
        'type': 'number',
        'min': 1,
        'max': 2147483647,
        'step': 1,
        'className': 'form-input',
    },
    {
        'id': 'max-iterations-input',
        'label': 'Max Iterations',
        'type': 'number',
        'min': 1,
        'max': 2147483647,
        'step': 1,
        'className': 'form-input',
    },
    {
        'id': 'terrain-dropdown',
        'label': 'Terrain',
        'type': 'dropdown',
        'options': [],
        'className': 'dropdown-standard',
        'multi': True,
    },
]

prevention_fields = [
    {'id': 'prevention-name', 'label': 'Name', 'type': 'text', 'className': 'form-input'},
    {
        'id': 'mask-n95',
        'component': lambda readonly, value: create_mask_input(
            'N95', 'N95', default_value=value or 0.85, is_checked=not readonly, is_disabled=readonly
        ),
    },
    {
        'id': 'mask-home',
        'component': lambda readonly, value: create_mask_input(
            'HOME', 'Home/Cloth', default_value=value or 0.0, is_checked=not readonly, is_disabled=readonly
        ),
    },
    {
        'id': 'mask-cloth',
        'component': lambda readonly, value: create_mask_input(
            'CLOTH', 'Cloth', default_value=value or 0.83, is_checked=not readonly, is_disabled=readonly
        ),
    },
    {
        'id': 'mask-surgical',
        'component': lambda readonly, value: create_mask_input(
            'SURGICAL', 'Surgical', default_value=value or 0.85, is_checked=not readonly, is_disabled=readonly
        ),
    },
    {
        'id': 'vaccine-mrna',
        'component': lambda readonly, value: create_vaccine_type(
            'MRNA',
            'MRNA (Moderna)',
            default_doses=value or [0.0, 0.31, 0.88],
            is_checked=not readonly,
            is_disabled=readonly,
        ),
    },
    {
        'id': 'vaccine-astra',
        'component': lambda readonly, value: create_vaccine_type(
            'ASTRA',
            'ASTRA (AstraZeneca)',
            default_doses=value or [0.0, 0.31, 0.67],
            is_checked=not readonly,
            is_disabled=readonly,
        ),
    },
]

agentconfig_fields = [
    {'id': 'agent-config-name', 'label': 'Name', 'type': 'text', 'className': 'form-input'},
    {
        'id': 'random-agents-input',
        'label': 'Random Agents',
        'type': 'number',
        'min': 0,
        'max': 10000,
        'className': 'form-input-number',
    },
    {
        'id': 'random-infected-input',
        'label': 'Random Infected',
        'type': 'number',
        'min': 0,
        'max': 10000,
        'className': 'form-input-number',
    },
    # Add more fields as needed for default/custom agent config
]


def create_resource_modal(resource_type, title):
    """Create a modal for viewing and managing any resource."""
    return dbc.Modal(
        [
            dbc.ModalHeader(
                dbc.ModalTitle(id={'type': 'action-modal-title', 'resource': resource_type}, children=title)
            ),
            dbc.ModalBody(
                [
                    html.Div(
                        id={'type': 'action-modal-summary', 'resource': resource_type}, className='resource-summary'
                    ),
                    html.Details(
                        [
                            html.Summary('View Full Details'),
                            html.Pre(
                                id={'type': 'action-modal-details', 'resource': resource_type}, className='json-display'
                            ),
                        ],
                        className='details-expandable',
                    ),
                ]
            ),
            dbc.ModalFooter(
                [
                    html.Button(
                        'Confirm', id={'type': 'select-btn', 'resource': resource_type}, className='btn btn-success '
                    ),
                    html.Button(
                        'Edit', id={'type': 'edit-btn', 'resource': resource_type}, className='btn btn-primary '
                    ),
                    html.Button(
                        'Clone', id={'type': 'clone-btn', 'resource': resource_type}, className='btn btn-info '
                    ),
                    html.Button(
                        'Delete', id={'type': 'delete-btn', 'resource': resource_type}, className='btn btn-danger'
                    ),
                ]
            ),
        ],
        id={'type': 'action-modal', 'resource': resource_type},
        size='lg',
        is_open=False,
    )


def create_resource_tab(resource_type, form_fields, label=None):
    """Create a tab with dropdown, create button, and editable form area."""
    label = label or resource_type.replace('_', ' ').title()
    return dbc.Tab(
        label=label,
        tab_id=f'{resource_type}-tab',
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
                    html.Div(
                        [
                            html.Button('Save', id=f'{resource_type}-save-btn', className='btn btn-primary'),
                            html.Button(
                                'Cancel', id=f'{resource_type}-cancel-btn-bottom', className='btn btn-secondary'
                            ),
                        ],
                        id={'type': 'form-button-group', 'resource': resource_type},
                        className='form-button-group',
                        style={'display': 'none'},
                    ),
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
            dcc.Store(
                id={'type': 'form-mode', 'resource': resource_type}, data={'mode': 'readonly', 'resource_id': None}
            ),
        ]
    )


RESOURCES = ['scenario', 'agent_config', 'virus', 'prevention', 'simulation']

layout = html.Div(
    [
        html.Div(
            [
                html.H1('Run Builder', className='page-title'),
                html.P('Create and manage simulation runs', className='page-subtitle'),
            ],
            className='page-header',
        ),
        dbc.Tabs(
            [
                dbc.Tab(
                    label='Scenario',
                    tab_id='scenario-tab',
                    children=[
                        html.Div(
                            [
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            [
                                                dcc.Dropdown(
                                                    id={'type': 'dropdown', 'resource': 'scenario'},
                                                    options=[],
                                                    placeholder='Select Scenario',
                                                    className='dropdown-standard',
                                                )
                                            ],
                                            width=10,
                                            className='dropdown-col',
                                        ),
                                        dbc.Col(
                                            [
                                                html.Button(
                                                    'Create',
                                                    id={'type': 'create-btn', 'resource': 'scenario'},
                                                    className='btn btn-primary',
                                                )
                                            ],
                                            width=1,
                                            className='dropdown-col',
                                        ),
                                    ],
                                    className='dropdown-row',
                                ),
                                dbc.Tabs(
                                    [
                                        create_resource_tab('virus', virus_fields, 'Virus Configuration'),
                                        create_resource_tab(
                                            'prevention', prevention_fields, 'Prevention Configuration'
                                        ),
                                        create_resource_tab(
                                            'simulation', simulation_fields, 'Simulation Configuration'
                                        ),
                                    ]
                                ),
                                html.Div(
                                    [
                                        html.Button('Save', id='scenario-save-btn', className='btn btn-primary'),
                                        html.Button(
                                            'Cancel', id='scenario-cancel-btn-bottom', className='btn btn-secondary'
                                        ),
                                    ],
                                    id={'type': 'form-button-group', 'resource': 'scenario'},
                                    style={'display': 'none'},
                                ),
                            ],
                            className='p-3',
                        ),
                    ],
                ),
                create_resource_tab('agent_config', agentconfig_fields, 'Agent Configuration'),
            ],
            id='main-tabs',
            active_tab='scenario-tab',
        ),
        # Modals for all resources
        *[create_resource_modal(r, r.replace('_', ' ').title()) for r in RESOURCES],
        # Stores for all resources
        *[create_stores_for_resource(r) for r in RESOURCES],
        html.Div(id='notification-area'),
    ],
    className='page-container',
)


def register_form_renderer(resource_type, fields):
    """Register a form rendering callback for a resource."""

    @callback(
        Output(f'{resource_type}-editable-fields', 'children'),
        [Input({'type': 'form-mode', 'resource': resource_type}, 'data')],
        [State({'type': 'original-data', 'resource': resource_type}, 'data')],
        prevent_initial_call=False,
    )
    def render_form(mode_data, values_data):
        readonly = not (mode_data and mode_data.get('mode') == 'edit')
        return render_resource_form(fields, values=values_data, readonly=readonly)


# Register all form renderers
register_form_renderer('agent_config', agentconfig_fields)
register_form_renderer('virus', virus_fields)
register_form_renderer('prevention', prevention_fields)
register_form_renderer('simulation', simulation_fields)


@callback(
    [Output({'type': 'dropdown', 'resource': ALL}, 'options')], [Input({'type': 'dropdown', 'resource': ALL}, 'id')]
)
def populate_dropdowns(dropdown_ids):
    """Populate all dropdowns from API."""
    return [
        [
            [{'label': r['name'], 'value': r['id']} for r in resources]
            if (success := api.get_all(d['resource']))[0] and (resources := success[1])
            else []
            for d in dropdown_ids
        ]
    ]


@callback(
    [
        Output({'type': 'action-modal', 'resource': ALL}, 'is_open'),
        Output({'type': 'action-modal-title', 'resource': ALL}, 'children'),
        Output({'type': 'action-modal-summary', 'resource': ALL}, 'children'),
        Output({'type': 'action-modal-details', 'resource': ALL}, 'children'),
        Output({'type': 'resource-store', 'resource': ALL}, 'data'),
    ],
    [Input({'type': 'dropdown', 'resource': ALL}, 'value')],
    [State({'type': 'dropdown', 'resource': ALL}, 'id')],
    prevent_initial_call=True,
)
def update_modal(selected_ids, dropdown_ids):
    """Open modal when dropdown selection changes."""
    triggered = ctx.triggered_id
    if not triggered:
        raise PreventUpdate

    triggered_resource = triggered['resource']
    outputs = [[], [], [], [], []]  # modals_open, titles, summaries, details, stores

    for idx, dropdown_id in enumerate(dropdown_ids):
        resource_type = dropdown_id['resource']
        resource_id = selected_ids[idx]

        if resource_type == triggered_resource and resource_id:
            success, resource, _ = api.get_by_id(resource_type, resource_id)
            if success and resource:
                outputs[0].append(True)  # open modal
                outputs[1].append(resource.get('name', 'Details'))
                outputs[2].append(
                    html.Div(
                        [
                            html.P([html.Strong(f'{k.replace("_", " ").title()}: '), str(v)])
                            for k, v in resource.items()
                            if k != 'id'
                        ]
                    )
                )
                outputs[3].append(json.dumps(resource, indent=2))
                outputs[4].append(resource_id)
                continue

        # No update for other resources
        for out in outputs:
            out.append(no_update)

    return outputs


@callback(
    [
        Output({'type': 'form-mode', 'resource': ALL}, 'data', allow_duplicate=True),
        Output({'type': 'original-data', 'resource': ALL}, 'data', allow_duplicate=True),
        Output({'type': 'form-button-group', 'resource': ALL}, 'style', allow_duplicate=True),
    ],
    [Input({'type': 'create-btn', 'resource': ALL}, 'n_clicks')],
    [State({'type': 'form-mode', 'resource': ALL}, 'id')],
    prevent_initial_call=True,
)
def handle_create(_, mode_ids):
    """Create: clear form, enable editing."""
    triggered_resource = ctx.triggered_id['resource']
    return [
        [{'mode': 'edit', 'resource_id': None} if m['resource'] == triggered_resource else no_update for m in mode_ids],
        [{} if m['resource'] == triggered_resource else no_update for m in mode_ids],
        [{'display': 'flex'} if m['resource'] == triggered_resource else no_update for m in mode_ids],
    ]


@callback(
    [
        Output({'type': 'original-data', 'resource': ALL}, 'data', allow_duplicate=True),
        Output({'type': 'form-mode', 'resource': ALL}, 'data', allow_duplicate=True),
        Output({'type': 'form-button-group', 'resource': ALL}, 'style', allow_duplicate=True),
        Output({'type': 'action-modal', 'resource': ALL}, 'is_open', allow_duplicate=True),
    ],
    [
        Input({'type': 'edit-btn', 'resource': ALL}, 'n_clicks'),
        Input({'type': 'clone-btn', 'resource': ALL}, 'n_clicks'),
    ],
    [
        State({'type': 'resource-store', 'resource': ALL}, 'data'),
        State({'type': 'resource-store', 'resource': ALL}, 'id'),
        State({'type': 'original-data', 'resource': ALL}, 'id'),
        State({'type': 'form-mode', 'resource': ALL}, 'id'),
    ],
    prevent_initial_call=True,
)
def handle_edit_clone(edit_clicks, clone_clicks, store_data, store_ids, data_ids, mode_ids):
    """Edit/Clone: fetch resource, populate form."""
    triggered = ctx.triggered_id
    if not triggered:
        raise PreventUpdate

    triggered_resource = triggered['resource']
    is_clone = triggered['type'] == 'clone-btn'

    print(f'EDIT/CLONE triggered for resource: {triggered_resource}, button type: {triggered["type"]}')

    # Get resource ID using proper index mapping
    idx = next((i for i, s in enumerate(store_ids) if s['resource'] == triggered_resource), None)
    if idx is None or not store_data[idx]:
        print(f'ERROR: No data found for {triggered_resource} at index {idx}')
        raise PreventUpdate

    resource_id = store_data[idx]
    print(f'Fetching {triggered_resource} with ID {resource_id}')

    success, resource, err = api.get_by_id(triggered_resource, resource_id)
    if not success or not resource:
        print(f'ERROR: API failed - {err}')
        raise PreventUpdate

    if is_clone:
        resource = dict(resource)
        resource.pop('id', None)
        resource['name'] = f'{resource.get("name", "")} (copy)'
        resource_id = None  # Clear ID for clone

    # Build outputs using ID matching (not index)
    return [
        [resource if d['resource'] == triggered_resource else no_update for d in data_ids],
        [
            {'mode': 'edit', 'resource_id': resource_id} if m['resource'] == triggered_resource else no_update
            for m in mode_ids
        ],
        [{'display': 'flex'} if m['resource'] == triggered_resource else no_update for m in mode_ids],
        [False if m['resource'] == triggered_resource else no_update for m in mode_ids],
    ]


@callback(
    [
        Output({'type': 'dropdown', 'resource': ALL}, 'value', allow_duplicate=True),
        Output({'type': 'resource-store', 'resource': ALL}, 'data', allow_duplicate=True),
        Output({'type': 'action-modal', 'resource': ALL}, 'is_open', allow_duplicate=True),
        Output('notification-area', 'children', allow_duplicate=True),
    ],
    [Input({'type': 'delete-btn', 'resource': ALL}, 'n_clicks')],
    [
        State({'type': 'resource-store', 'resource': ALL}, 'data'),
        State({'type': 'resource-store', 'resource': ALL}, 'id'),
        State({'type': 'dropdown', 'resource': ALL}, 'id'),
        State({'type': 'action-modal', 'resource': ALL}, 'id'),
        State({'type': 'delete-btn', 'resource': ALL}, 'id'),  # <-- ADD THIS
    ],
    prevent_initial_call=True,
)
def handle_delete(delete_clicks, store_data, store_ids, dropdown_ids, modal_ids, delete_btn_ids):  # <-- ADD PARAM
    """Delete: remove resource from DB."""
    triggered = ctx.triggered_id
    if not triggered:
        raise PreventUpdate

    triggered_resource = triggered['resource']

    print(f'DELETE triggered for resource: {triggered_resource}')
    print(f'Delete button IDs order: {[b["resource"] for b in delete_btn_ids]}')
    print(f'Store IDs order: {[s["resource"] for s in store_ids]}')
    print(f'Dropdown IDs order: {[d["resource"] for d in dropdown_ids]}')
    print(f'Modal IDs order: {[m["resource"] for m in modal_ids]}')
    # print(f"Store data: {store_data}")

    # Get resource ID using proper index mapping
    idx = next((i for i, s in enumerate(store_ids) if s['resource'] == triggered_resource), None)

    if idx is None or not store_data[idx]:
        print(f'ERROR: No data found for {triggered_resource} at index {idx}')
        raise PreventUpdate

    resource_id = store_data[idx]
    print(f'Deleting {triggered_resource} with ID {resource_id}')

    success, _, err = api.delete(triggered_resource, resource_id)

    # Build outputs using ID matching (not index)
    return [
        [None if d['resource'] == triggered_resource else no_update for d in dropdown_ids],
        [None if s['resource'] == triggered_resource else no_update for s in store_ids],
        [False if m['resource'] == triggered_resource else no_update for m in modal_ids],
        dbc.Alert(
            f'Successfully deleted {triggered_resource}' if success else f'Failed to delete: {err}',
            color='success' if success else 'danger',
            duration=3000,
        ),
    ]


@callback(
    [
        Output({'type': 'form-mode', 'resource': ALL}, 'data', allow_duplicate=True),
        Output({'type': 'form-button-group', 'resource': ALL}, 'style', allow_duplicate=True),
        Output({'type': 'original-data', 'resource': ALL}, 'data', allow_duplicate=True),
    ],
    [
        Input(f'{r}-cancel-btn-bottom', 'n_clicks')
        for r in ['scenario', 'agent_config', 'virus', 'prevention', 'simulation']
    ],
    [State({'type': 'form-mode', 'resource': ALL}, 'id')],
    prevent_initial_call=True,
)
def handle_cancel(*args):
    """Cancel: revert to readonly."""
    triggered_resource = ctx.triggered_id.split('-cancel-btn')[0]
    mode_ids = args[-1]

    return [
        [
            {'mode': 'readonly', 'resource_id': None} if m['resource'] == triggered_resource else no_update
            for m in mode_ids
        ],
        [{'display': 'none'} if m['resource'] == triggered_resource else no_update for m in mode_ids],
        [None if m['resource'] == triggered_resource else no_update for m in mode_ids],
    ]
