"""Run Builder Page for LocABS Application."""

import copy
import json

import dash_bootstrap_components as dbc
from dash import ALL, Input, Output, State, callback, ctx, dcc, html, no_update, register_page
from dash.exceptions import PreventUpdate
from loguru import logger

from components.input_components import create_mask_input, create_vaccine_type
from components.resource_form import render_resource_form
from utilities import api
from utilities.logging import configure_logger
from utilities.normalizers import normalize_values

configure_logger(level='DEBUG')


register_page(__name__, path='/scenario-builder', name='Run Builder', title='LocABS · Run Builder')
# Child resources that should stay read-only until a scenario is being created/edited
SCENARIO_CHILD_RESOURCES = ['virus', 'prevention', 'simulation']

virus_fields = [
    {
        'id': {'type': 'form-input', 'resource': 'virus', 'field': 'name'},
        'label': 'Name',
        'type': 'text',
        'className': 'form-input',
    },
    {
        'id': {'type': 'form-input', 'resource': 'virus', 'field': 'attack_rate'},
        'label': 'Attack Rate',
        'type': 'number',
        'min': 0,
        'max': 1,
        'step': 0.001,
        'className': 'form-input',
    },
    {
        'id': {'type': 'form-input', 'resource': 'virus', 'field': 'infection_rate'},
        'label': 'Infection Rate',
        'type': 'number',
        'min': 0,
        'max': 1,
        'step': 0.001,
        'className': 'form-input',
    },
    {
        'id': {'type': 'form-input', 'resource': 'virus', 'field': 'fatality_rate'},
        'label': 'Fatality Rate',
        'type': 'number',
        'min': 0,
        'max': 1,
        'step': 0.001,
        'className': 'form-input',
    },
]

# TODO: Remove terrain and mapfile fields, - configure using defaults values - work on this !!!!!
simulation_fields = [
    {
        'id': {'type': 'form-input', 'resource': 'simulation', 'field': 'name'},
        'label': 'Name',
        'type': 'text',
        'className': 'form-input',
    },
    {
        'id': {'type': 'form-input', 'resource': 'simulation', 'field': 'mapfile'},
        'label': 'Map File',
        'type': 'dropdown',
        'options': [],
        'className': 'dropdown-standard',
    },
    {
        'id': {'type': 'form-input', 'resource': 'simulation', 'field': 'xy_scale'},
        'label': 'XY Scale',
        'type': 'number',
        'min': 1.0,
        'max': 1000000.0,
        'step': 0.01,
        'className': 'form-input',
    },
    {
        'id': {'type': 'form-input', 'resource': 'simulation', 'field': 't_step'},
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
        'id': {'type': 'form-input', 'resource': 'simulation', 'field': 'save_resolution'},
        'label': 'Save Resolution',
        'type': 'number',
        'min': 1,
        'max': 2147483647,
        'step': 1,
        'className': 'form-input',
    },
    {
        'id': {'type': 'form-input', 'resource': 'simulation', 'field': 'max_iter'},
        'label': 'Max Iterations',
        'type': 'number',
        'min': 1,
        'max': 2147483647,
        'step': 1,
        'className': 'form-input',
    },
    {
        'id': {'type': 'form-input', 'resource': 'simulation', 'field': 'terrain'},
        'label': 'Terrain',
        'type': 'dropdown',
        'options': [],
        'className': 'dropdown-standard',
        'multi': True,
    },
]

prevention_fields = [
    {
        'id': {'type': 'form-input', 'resource': 'prevention', 'field': 'name'},
        'label': 'Name',
        'type': 'text',
        'className': 'form-input',
    },
    {'id': 'mask_group_label', 'section_label': 'Mask Information'},
    {
        'id': {'type': 'form-input', 'resource': 'prevention', 'field': 'mask_n95'},
        'component': lambda readonly, value: create_mask_input('N95', 'N95', default_value=value, is_disabled=readonly),
    },
    {
        'id': {'type': 'form-input', 'resource': 'prevention', 'field': 'mask_home'},
        'component': lambda readonly, value: create_mask_input(
            'HOME', 'Home/Cloth', default_value=value, is_disabled=readonly
        ),
    },
    {
        'id': {'type': 'form-input', 'resource': 'prevention', 'field': 'mask_cloth'},
        'component': lambda readonly, value: create_mask_input(
            'CLOTH', 'Cloth', default_value=value, is_disabled=readonly
        ),
    },
    {
        'id': {'type': 'form-input', 'resource': 'prevention', 'field': 'mask_surgical'},
        'component': lambda readonly, value: create_mask_input(
            'SURGICAL', 'Surgical', default_value=value, is_disabled=readonly
        ),
    },
    {'id': 'mask_group_label', 'section_label': 'Vaccines'},
    {
        'id': {'type': 'form-input', 'resource': 'prevention', 'field': 'vaccine_mrna'},
        'component': lambda readonly, value: create_vaccine_type(
            'MRNA',
            'MRNA (Moderna)',
            default_doses=value,
            is_disabled=readonly,
        ),
    },
    {
        'id': {'type': 'form-input', 'resource': 'prevention', 'field': 'vaccine_astra'},
        'component': lambda readonly, value: create_vaccine_type(
            'ASTRA',
            'ASTRA (AstraZeneca)',
            default_doses=value,
            is_disabled=readonly,
        ),
    },
]

scenario_fields = [
    {
        'id': {'type': 'form-input', 'resource': 'scenario', 'field': 'name'},
        'label': 'Name',
        'type': 'text',
        'className': 'form-input',
    },
]

agentconfig_fields = [
    {
        'id': {'type': 'form-input', 'resource': 'agent_config', 'field': 'name'},
        'label': 'Name',
        'type': 'text',
        'className': 'form-input',
    },
    {'id': 'mask_group_label', 'section_label': 'Agent Population'},
    {
        'id': {'type': 'form-input', 'resource': 'agent_config', 'field': 'random_agents'},
        'label': 'Random Agents',
        'type': 'number',
        'min': 0,
        'max': 10000,
        'className': 'form-input-number',
    },
    {
        'id': {'type': 'form-input', 'resource': 'agent_config', 'field': 'random_infected'},
        'label': 'Random Infected',
        'type': 'number',
        'min': 0,
        'max': 10000,
        'className': 'form-input-number',
    },
    # Add more fields as needed for default/custom agent config
]

AGENT_LOCKED_FIELDS = {
    'default': {
        'info': {
            'mask_type': '',
            'vax_type': '',
            'vax_doses': 0,
            'age': None,
            'start_zone': None,
            'work_zone': None,
            'home_zone': None,
            'schedule': {},
            'access_level': 0,
            'urgency': 1.0,
        },
        'state': {'dt': None, 'status': 'UNKNOWN', 'pos': (0, 0, 0), 'path': []},
    },
    'custom': [],
}


def build_payload(resource, form_data, original=None, extras=None):
    """Minimal, resource-aware payload builder."""
    data = dict(form_data)
    extras = extras or {}

    if resource == 'agent_config':
        locked = original or {}
        data['default'] = copy.deepcopy(locked.get('default', AGENT_LOCKED_FIELDS['default']))
        data['custom'] = copy.deepcopy(locked.get('custom', AGENT_LOCKED_FIELDS['custom']))

    elif resource == 'prevention':
        data['mask'] = extras.get('mask', {})
        data['vax'] = extras.get('vax', {})
        for key in list(data.keys()):
            if key.startswith('mask_') or key.startswith('vaccine_'):
                data.pop(key, None)

    elif resource == 'simulation':
        terrain = data.get('terrain')
        if isinstance(terrain, list):
            data['terrain'] = [t['id'] if isinstance(t, dict) else t for t in terrain]
        mapfile = data.get('mapfile')
        if isinstance(mapfile, dict):
            data['mapfile'] = mapfile.get('id') or mapfile.get('name')

    return data


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


def create_resource_tab(resource_type, label=None):
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
            dcc.Store(id={'type': 'modal-suppress', 'resource': resource_type}, data=False),
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
                                html.Div(id='scenario-editable-fields', className='form-editable-fields'),
                                dbc.Tabs(
                                    [
                                        create_resource_tab('virus', 'Virus Configuration'),
                                        create_resource_tab('prevention', 'Prevention Configuration'),
                                        create_resource_tab('simulation', 'Simulation Configuration'),
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
                create_resource_tab('agent_config', 'Agent Configuration'),
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
        [
            Input({'type': 'form-mode', 'resource': resource_type}, 'data'),
            Input({'type': 'original-data', 'resource': resource_type}, 'data'),
        ],
        prevent_initial_call=False,
    )
    def render_form(mode_data, values_data):
        readonly = not (mode_data and mode_data.get('mode') == 'edit')
        logger.debug(
            f'RENDERING {resource_type} form - readonly={readonly}, has_data={values_data is not None}'
        )  # Debug
        clean = normalize_values(resource_type, values_data)
        return render_resource_form(resource_type, fields, values=clean, readonly=readonly)


# Register all form renderers
register_form_renderer('agent_config', agentconfig_fields)
register_form_renderer('virus', virus_fields)
register_form_renderer('prevention', prevention_fields)
register_form_renderer('simulation', simulation_fields)
register_form_renderer('scenario', scenario_fields)


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
    Output({'type': 'form-input', 'resource': 'simulation', 'field': 'mapfile'}, 'options'),
    Input({'type': 'form-input', 'resource': 'simulation', 'field': 'mapfile'}, 'id'),
    prevent_initial_call=False,
)
def load_simulation_mapfiles(_):
    """Load mapfile options for simulation form."""
    success, mapfiles, _ = api.get_map_files()
    if not success:
        return []

    return [{'label': m, 'value': m} for m in mapfiles]


@callback(
    Output({'type': 'form-input', 'resource': 'simulation', 'field': 'terrain'}, 'options'),
    Input({'type': 'form-input', 'resource': 'simulation', 'field': 'terrain'}, 'id'),
    prevent_initial_call=False,
)
def load_simulation_terrain(_):
    """Load terrain options for simulation form."""
    success, terrains, _ = api.get_all('terrain')
    if not success:
        return []

    return [{'label': t['name'], 'value': t['id']} for t in terrains]


def register_modal_loader(resource):
    """Register a modal loader callback for a resource."""

    @callback(
        Output({'type': 'action-modal', 'resource': resource}, 'is_open', allow_duplicate=True),
        Output({'type': 'action-modal-title', 'resource': resource}, 'children', allow_duplicate=True),
        Output({'type': 'action-modal-summary', 'resource': resource}, 'children', allow_duplicate=True),
        Output({'type': 'action-modal-details', 'resource': resource}, 'children', allow_duplicate=True),
        Output({'type': 'resource-store', 'resource': resource}, 'data', allow_duplicate=True),
        Output({'type': 'original-data', 'resource': resource}, 'data', allow_duplicate=True),
        Output({'type': 'form-mode', 'resource': resource}, 'data', allow_duplicate=True),
        Output({'type': 'modal-suppress', 'resource': resource}, 'data', allow_duplicate=True),
        Input({'type': 'dropdown', 'resource': resource}, 'value'),
        Input({'type': 'modal-suppress', 'resource': resource}, 'data'),
        prevent_initial_call=True,
    )
    def _modal_loader(selected_id, suppress):
        if suppress:
            # Reset suppress flag and skip reopening
            return False, no_update, no_update, no_update, no_update, no_update, no_update, False

        if not selected_id:
            raise PreventUpdate

        success, item, _ = api.get_by_id(resource, selected_id)
        if not success:
            raise PreventUpdate

        summary = html.Div(
            [html.P([html.Strong(f'{k.title().replace("_", " ")}: '), str(v)]) for k, v in item.items() if k != 'id']
        )

        return (
            True,
            item.get('name', resource.title()),
            summary,
            json.dumps(item, indent=2),
            selected_id,
            item,
            {'mode': 'readonly', 'resource_id': selected_id},
            False,
        )


def register_create(resource):
    """Register a create callback for a resource."""

    @callback(
        Output({'type': 'form-mode', 'resource': resource}, 'data', allow_duplicate=True),
        Output({'type': 'original-data', 'resource': resource}, 'data', allow_duplicate=True),
        Output({'type': 'form-button-group', 'resource': resource}, 'style', allow_duplicate=True),
        Input({'type': 'create-btn', 'resource': resource}, 'n_clicks'),
        prevent_initial_call=True,
    )
    def _create(_n):
        return {'mode': 'edit', 'resource_id': None}, {}, {'display': 'flex'}


def register_edit_clone(resource):
    """Register an edit and clone callback for a resource."""

    @callback(
        Output({'type': 'original-data', 'resource': resource}, 'data', allow_duplicate=True),
        Output({'type': 'form-mode', 'resource': resource}, 'data', allow_duplicate=True),
        Output({'type': 'form-button-group', 'resource': resource}, 'style', allow_duplicate=True),
        Output({'type': 'action-modal', 'resource': resource}, 'is_open', allow_duplicate=True),
        Output({'type': 'resource-store', 'resource': resource}, 'data', allow_duplicate=True),
        Input({'type': 'edit-btn', 'resource': resource}, 'n_clicks'),
        Input({'type': 'clone-btn', 'resource': resource}, 'n_clicks'),
        State({'type': 'resource-store', 'resource': resource}, 'data'),
        prevent_initial_call=True,
    )
    def _edit_clone(_edit, _clone, stored_id):
        if not ctx.triggered_id:
            raise PreventUpdate

        is_clone = ctx.triggered_id['type'] == 'clone-btn'
        success, item, _ = api.get_by_id(resource, stored_id)

        if not success:
            raise PreventUpdate

        item = copy.deepcopy(item)
        if is_clone:
            item.pop('id', None)
            item['name'] = f'{item["name"]}-copy'
            stored_id = None

        return item, {'mode': 'edit', 'resource_id': stored_id}, {'display': 'flex'}, False, stored_id


def register_delete(resource):
    """Register a delete callback for a resource."""

    @callback(
        Output({'type': 'dropdown', 'resource': resource}, 'value', allow_duplicate=True),
        Output({'type': 'dropdown', 'resource': resource}, 'options', allow_duplicate=True),
        Output({'type': 'resource-store', 'resource': resource}, 'data', allow_duplicate=True),
        Output({'type': 'action-modal', 'resource': resource}, 'is_open', allow_duplicate=True),
        Output('notification-area', 'children', allow_duplicate=True),
        Input({'type': 'delete-btn', 'resource': resource}, 'n_clicks'),
        State({'type': 'resource-store', 'resource': resource}, 'data'),
        prevent_initial_call=True,
    )
    def _delete(n, stored_id):
        if not n:
            raise PreventUpdate

        success, _, err = api.delete(resource, stored_id)

        alert = dbc.Alert(
            f'{"Deleted" if success else f"Delete failed {err}"} {resource}',
            color='success' if success else 'danger',
            duration=3000,
        )

        opts = []
        if success:
            success_all, resources, _ = api.get_all(resource)
            if success_all and resources:
                opts = [{'label': r['name'], 'value': r['id']} for r in resources]

        return None, opts, None, False, alert


def register_confirm(resource):
    """Register a confirm/select callback for a resource modal."""

    @callback(
        Output({'type': 'dropdown', 'resource': resource}, 'value', allow_duplicate=True),
        Output({'type': 'action-modal', 'resource': resource}, 'is_open', allow_duplicate=True),
        Output({'type': 'modal-suppress', 'resource': resource}, 'data', allow_duplicate=True),
        Input({'type': 'select-btn', 'resource': resource}, 'n_clicks'),
        State({'type': 'resource-store', 'resource': resource}, 'data'),
        prevent_initial_call=True,
    )
    def _confirm(n, stored_id):
        if not n:
            raise PreventUpdate
        # Set selection, close modal, and suppress reopen for this cycle
        return stored_id, False, True


def register_cancel(resource):
    """Register a cancel callback for a resource form."""

    @callback(
        Output({'type': 'form-mode', 'resource': resource}, 'data', allow_duplicate=True),
        Output({'type': 'form-button-group', 'resource': resource}, 'style', allow_duplicate=True),
        Input(f'{resource}-cancel-btn-bottom', 'n_clicks'),
        State({'type': 'resource-store', 'resource': resource}, 'data'),
        prevent_initial_call=True,
    )
    def _cancel(n, stored_id):
        if not n:
            raise PreventUpdate
        # Return to readonly; keep current selection
        return {'mode': 'readonly', 'resource_id': stored_id}, {'display': 'none'}


def register_save(resource):
    """Register a save callback for a resource."""
    extra_states = []
    if resource == 'prevention':
        extra_states = [
            State({'type': 'mask-effectiveness-slider', 'mask': ALL}, 'value'),
            State({'type': 'mask-effectiveness-slider', 'mask': ALL}, 'id'),
            State({'type': 'mask-checkbox', 'mask': ALL}, 'value'),
            State({'type': 'mask-checkbox', 'mask': ALL}, 'id'),
            State({'type': 'vaccine-dose', 'vaccine': ALL, 'dose': ALL}, 'value'),
            State({'type': 'vaccine-dose', 'vaccine': ALL, 'dose': ALL}, 'id'),
            State({'type': 'vaccine-checkbox', 'vaccine': ALL}, 'value'),
            State({'type': 'vaccine-checkbox', 'vaccine': ALL}, 'id'),
        ]
    if resource == 'scenario':
        extra_states = [
            State({'type': 'dropdown', 'resource': 'virus'}, 'value'),
            State({'type': 'dropdown', 'resource': 'prevention'}, 'value'),
            State({'type': 'dropdown', 'resource': 'simulation'}, 'value'),
        ]

    @callback(
        Output({'type': 'form-mode', 'resource': resource}, 'data', allow_duplicate=True),
        Output({'type': 'form-button-group', 'resource': resource}, 'style', allow_duplicate=True),
        Output({'type': 'dropdown', 'resource': resource}, 'value', allow_duplicate=True),
        Output({'type': 'dropdown', 'resource': resource}, 'options', allow_duplicate=True),
        Output({'type': 'resource-store', 'resource': resource}, 'data', allow_duplicate=True),
        Output('notification-area', 'children', allow_duplicate=True),
        Input(f'{resource}-save-btn', 'n_clicks'),
        State({'type': 'form-input', 'resource': resource, 'field': ALL}, 'value'),
        State({'type': 'form-input', 'resource': resource, 'field': ALL}, 'id'),
        # Current mode store
        State({'type': 'form-mode', 'resource': resource}, 'data'),
        State({'type': 'original-data', 'resource': resource}, 'data'),
        *extra_states,
        prevent_initial_call=True,
    )
    def _save(n, values, ids, mode, original, *extras):
        if not n:
            raise PreventUpdate
        form_data = {input_id['field']: value for input_id, value in zip(ids, values)}

        extras_map = {}
        if resource == 'prevention' and extras:
            (
                mask_values,
                mask_ids,
                mask_checks,
                mask_check_ids,
                vaccine_dose_values,
                vaccine_dose_ids,
                vaccine_checks,
                vaccine_check_ids,
            ) = extras

            selected_masks = {
                chk_id.get('mask')
                for chk_id, chk_val in zip(mask_check_ids, mask_checks)
                if chk_val and chk_id.get('mask') in chk_val
            }
            mask_payload = {
                m_id.get('mask'): (float(m_val) if m_id.get('mask') in selected_masks else 0.0)
                for m_id, m_val in zip(mask_ids, mask_values)
                if isinstance(m_id, dict)
            }

            selected_vax = {
                chk_id.get('vaccine')
                for chk_id, chk_val in zip(vaccine_check_ids, vaccine_checks)
                if chk_val and chk_id.get('vaccine') in chk_val
            }
            vax_payload = {}
            for v_id, v_val in zip(vaccine_dose_ids, vaccine_dose_values):
                if not isinstance(v_id, dict):
                    continue
                v_type, dose_idx = v_id.get('vaccine'), (v_id.get('dose') or 1) - 1
                doses = vax_payload.setdefault(v_type, [0.0, 0.0, 0.0])
                if v_type and 0 <= dose_idx < 3:
                    doses[dose_idx] = float(v_val) if v_type in selected_vax else 0.0

            for v_type in selected_vax:
                vax_payload.setdefault(v_type, [0.0, 0.0, 0.0])

            extras_map = {'mask': mask_payload, 'vax': vax_payload}
        elif resource == 'scenario' and extras:
            virus_id, prevention_id, simulation_id = extras
            form_data['virus'] = virus_id
            form_data['prevention'] = prevention_id
            form_data['sim'] = simulation_id

        payload = build_payload(resource, form_data, original, extras_map)

        logger.debug(f'\n=== SAVE {resource.upper()} ===')
        logger.debug('Payload:', form_data)
        logger.debug(f'Final Payload Sent to API: {payload}')

        rid = mode.get('resource_id')

        if rid:
            success, item, err = api.update(resource, rid, payload)
        else:
            success, item, err = api.create(resource, payload)

        if not success:
            alert = dbc.Alert(f'Save failed: {err}', color='danger', duration=5000)
            return no_update, no_update, no_update, no_update, no_update, alert

        new_id = item['id']
        alert = dbc.Alert(f'Saved {resource}', color='success', duration=5000)

        success_all, resources, _ = api.get_all(resource)
        opts = [{'label': r['name'], 'value': r['id']} for r in resources] if success_all and resources else []

        return {'mode': 'readonly', 'resource_id': new_id}, {'display': 'none'}, new_id, opts, new_id, alert


# Register create, edit/clone, delete, and save callbacks for all resources
for res in RESOURCES:
    register_create(res)
    register_edit_clone(res)
    register_delete(res)
    register_confirm(res)
    register_cancel(res)
    register_save(res)
    register_modal_loader(res)
