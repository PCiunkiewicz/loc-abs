"""Data Visualisation Page for LocABS Application."""

from dash import html, dcc, register_page, callback, Output, Input, State, ctx, no_update
import dash_bootstrap_components as dbc
from utilities import api
from loguru import logger

register_page(__name__, path='/data-viz', name='Data Visualisation', title='LocABS · Data Visualisation')

layout = html.Div(
    [
        dbc.Row(
            [
                # LEFT SIDEBAR
                dbc.Col(
                    [
                        html.H5('RUN', className='mb-3'),
                        html.Div(
                            [
                                dbc.Label('Name', html_for='dv-name-input', className='form-label'),
                                dbc.Input(id='dv-name-input', placeholder='Enter run name'),
                            ],
                            className='mb-3',
                        ),
                        html.Div(
                            [
                                dbc.Label('Agent Configuration', html_for='dv-agent-dropdown', className='form-label'),
                                dcc.Dropdown(id='dv-agent-dropdown', options=[], placeholder='Choose an option here'),
                            ],
                            className='mb-3',
                        ),
                        html.Div(
                            [
                                dbc.Label('Scenarios', html_for='dv-scenario-dropdown'),
                                dcc.Dropdown(
                                    id='dv-scenario-dropdown', options=[], placeholder='Choose an option here'
                                ),
                            ]
                        ),
                        html.Div(
                            [
                                dbc.Label('Runs', html_for='dv-runs-input'),
                                dbc.Input(
                                    id='dv-runs-input',
                                    type='number',
                                    min=1,
                                    step=1,
                                    value=1,
                                    className='dv-runs-input w-100',
                                ),
                            ]
                        ),
                        dbc.Button('Run Simulation', id='dv-run-btn', color='primary', className='btn w-100'),
                        dbc.Button(
                            'Save Run', id='dv-save-scenario-btn', color='dark', className='btn w-100 mt-2'
                        ),
                        dbc.Button('Reset to Default', id='dv-reset-btn', color='light', className='btn w-100 mt-2'),
                        html.Hr(),
                        html.Div(
                            id='dv-run-details',
                            className='border p-3',
                            children=[html.H6('Run Details'), html.Div('No run yet.', id='dv-run-details-body')],
                        ),
                        html.Br(),
                        dbc.Button(
                            'Go to Decision Support',
                            id='dv-goto-decision',
                            color='info',
                            className='w-100',
                            href='/decision-support',
                        ),
                    ],
                    width=3,
                    className='dv-sidebar',
                ),
                # MAIN VISUALISATION AREA
                dbc.Col(
                    [
                        dbc.Row(
                            [
                                dbc.Col(dbc.Button('Filter', id='dv-filter-btn', color='secondary'), width='auto'),
                                dbc.Col(dbc.Button('Export', id='dv-export-btn', color='secondary'), width='auto'),
                            ],
                            justify='between',
                            className='mb-2',
                        ),
                        dbc.Tabs(
                            [
                                dbc.Tab(label='Time Series', tab_id='tab-timeseries'),
                                dbc.Tab(label='Distributions', tab_id='tab-dists'),
                                dbc.Tab(label='Logs', tab_id='tab-logs'),
                            ],
                            id='dv-tabs',
                            active_tab='tab-map',
                        ),
                        html.Div(
                            dcc.Loading(
                                dcc.Graph(id='dv-graph', figure={}, config={'displayModeBar': True}),
                                type='circle',
                            ),
                            className='dv-graph-wrap',
                        ),
                        dbc.Row(
                            [
                                dbc.Col(
                                    html.Div('Placeholder information about graph', className='text-muted'), width=8
                                ),
                                dbc.Col(dbc.Button('Action', color='secondary'), width=2),
                            ],
                            className='mt-2',
                        ),
                        html.Hr(className='my-4'),
                        # LARGE BOTTOM SUMMARY
                        html.Div(
                            id='dv-summary-table',
                            children=[html.Div('SCENARIO SUMMARY DATA TABLE', className='text-center text-muted mt-5')],
                            className='dv-summary',
                        ),
                    ],
                    width=9,
                ),
            ],
            className='g-4',
        ),
        # hidden store and init interval
        dcc.Store(id='dv-current-run'),
        dcc.Interval(id='dv-init', interval=1000, n_intervals=0, max_intervals=0),
        html.Div(id='dv-notification-area'),
    ],
    className='data-viz-page-container',
)


@callback(
    [
        Output('dv-agent-dropdown', 'options'),
        Output('dv-scenario-dropdown', 'options'),
    ],
    Input('dv-init', 'n_intervals'),
    prevent_initial_call=False,
)
def _populate_dropdowns(_):
    """Populate agent_config and scenario dropdown options on load."""
    agents = []
    scenarios = []
    try:
        _, agents, _ = api.get_all('agent_config')
        _, scenarios, _ = api.get_all('scenario')
    except Exception as exc:  # pylint: disable=broad-exception-caught
        logger.exception('Error fetching dropdown options: %s', exc)

    agent_opts = [{'label': a['name'], 'value': a['id']} for a in (agents or [])]
    scenario_opts = [{'label': s['name'], 'value': s['id']} for s in (scenarios or [])]
    return agent_opts, scenario_opts


@callback(
    Output('dv-runs-input', 'value'),
    [Input('dv-runs-incr', 'n_clicks'), Input('dv-runs-decr', 'n_clicks')],
    State('dv-runs-input', 'value'),
    prevent_initial_call=True,
)
def _change_runs(_incr, _decr, current):
    """Increment or decrement runs count."""
    triggered = ctx.triggered_id
    if not triggered:
        return no_update
    if triggered == 'dv-runs-incr':
        return (current or 1) + 1
    return max(1, (current or 1) - 1)


@callback(
    [
        Output('dv-current-run', 'data'),
        Output('dv-run-details-body', 'children'),
        Output('dv-notification-area', 'children'),
    ],
    Input('dv-run-btn', 'n_clicks'),
    [
        State('dv-name-input', 'value'),
        State('dv-agent-dropdown', 'value'),
        State('dv-scenario-dropdown', 'value'),
        State('dv-runs-input', 'value'),
    ],
    prevent_initial_call=True,
)
def _start_run(_n, name, agent_id, scenario_id, runs):
    """Build a minimal Run payload and store/display it (no backend run invocation)."""
    if not ctx.triggered_id:
        return no_update

    payload = {
        'name': name or 'unnamed-run',
        'status': 'CREATED',
        'save_dir': None,
        'config': None,
        'logfile': None,
        'scenario_id': scenario_id,
        'agents_id': agent_id,
        'runs': int(runs or 1),
    }

    # store payload locally (frontend store). Backend start-invocation can be added later.
    details = [
        html.P([html.Strong('Name: '), payload['name']]),
        html.P([html.Strong('Agents id: '), str(payload['agents_id'])]),
        html.P([html.Strong('Scenario id: '), str(payload['scenario_id'])]),
        html.P([html.Strong('Runs: '), str(payload['runs'])]),
        html.P([html.Strong('Status: '), payload['status']]),
    ]

    notification = dbc.Alert(f'Run prepared: {payload["name"]}', color='success', duration=3000)

    return payload, details, notification


def _safe_resource_name(resource, obj_id):
    """Return a readable name for a related resource id."""
    if not obj_id:
        return 'Not selected'
    try:
        success, item, _ = api.get_by_id(resource, obj_id)
        if success and item:
            return item.get('name') or str(obj_id)
    except Exception as exc:  # pylint: disable=broad-exception-caught
        logger.exception('Error fetching %s %s: %s', resource, obj_id, exc)
    return f'ID {obj_id}'


def _get_scenario_details(scenario_id):
    """Fetch scenario data by id with graceful fallback."""
    if not scenario_id:
        return None
    try:
        success, scenario, _ = api.get_by_id('scenario', scenario_id)
        if success and scenario:
            return scenario
    except Exception as exc:  # pylint: disable=broad-exception-caught
        logger.exception('Error fetching scenario %s: %s', scenario_id, exc)
    return None


@callback(
    Output('dv-summary-table', 'children'),
    [
        Input('dv-scenario-dropdown', 'value'),
        Input('dv-agent-dropdown', 'value'),
        Input('dv-runs-input', 'value'),
        Input('dv-name-input', 'value'),
    ],
    prevent_initial_call=False,
)
def _render_summary(scenario_id, agent_id, runs, run_name):
    """Render a summary of the selected scenario and run settings."""
    scenario = _get_scenario_details(scenario_id)
    if scenario_id and scenario is None:
        return dbc.Alert('Unable to load scenario details right now.', color='danger', className='mb-0')

    scenario_name = (scenario or {}).get('name', 'No scenario selected')
    virus_name = _safe_resource_name('virus', (scenario or {}).get('virus'))
    prevention_name = _safe_resource_name('prevention', (scenario or {}).get('prevention'))
    simulation_name = _safe_resource_name('simulation', (scenario or {}).get('sim') or (scenario or {}).get('simulation'))
    agent_name = _safe_resource_name('agent_config', agent_id)
    run_total = runs or 1

    rows = [
        ('Scenario', scenario_name),
        ('Virus Config', virus_name),
        ('Prevention Config', prevention_name),
        ('Simulation', simulation_name),
        ('Agent Config', agent_name),
        ('Runs', run_total),
        ('Run Name', run_name or 'unnamed-run'),
    ]

    table_rows = [
        html.Tr([html.Th(label, className='w-25 text-muted small'), html.Td(value)]) for label, value in rows
    ]

    decision_link = dbc.Button('Open Decision Support', color='info', href='/decision-support', className='mt-3')

    return dbc.Card(
        dbc.CardBody(
            [
                html.H5('Scenario Summary', className='mb-3'),
                dbc.Table(table_rows, bordered=False, hover=False, striped=False, responsive=True, size='sm'),
                html.Div(decision_link, className='text-end'),
            ]
        ),
        className='h-100',
    )
