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
                        html.Div(
                            [
                                dbc.Label('Run', html_for='dv-run-dropdown'),
                                dcc.Dropdown(
                                    id='dv-run-dropdown',
                                    options=[],
                                    placeholder='Select a run to view exports',
                                    clearable=True,
                                ),
                            ],
                            className='mb-3',
                        ),
                        dbc.Button('Run Simulation', id='dv-run-btn', color='primary', className='btn w-100'),
                        dbc.Button('Clear', id='dv-reset-btn', color='light', className='btn w-100 mt-2'),
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
                        html.Hr(),
                        html.Div(
                            id='dv-export-list',
                            children=[html.Div('Select a run to view exports', className='text-center text-muted')],
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
        Output('dv-run-dropdown', 'options'),
    ],
    Input('dv-init', 'n_intervals'),
    prevent_initial_call=False,
)
def _populate_dropdowns(_):
    """Populate agent_config and scenario dropdown options on load."""
    agents = []
    scenarios = []
    runs = []
    try:
        _, agents, _ = api.get_all('agent_config')
        _, scenarios, _ = api.get_all('scenario')
        _, runs, _ = api.get_all('run')
    except Exception as exc:  # pylint: disable=broad-exception-caught
        logger.exception('Error fetching dropdown options: %s', exc)

    agent_opts = [{'label': a['name'], 'value': a['id']} for a in (agents or [])]
    scenario_opts = [{'label': s['name'], 'value': s['id']} for s in (scenarios or [])]
    run_opts = [
        {'label': f"{r.get('name', 'run')} ({r.get('status', '').lower()})", 'value': r['id']} for r in (runs or [])
    ]
    return agent_opts, scenario_opts, run_opts


@callback(
    [
        Output('dv-current-run', 'data'),
        Output('dv-run-details-body', 'children'),
        Output('dv-notification-area', 'children', allow_duplicate=True),
        Output('dv-run-dropdown', 'options', allow_duplicate=True),
        Output('dv-run-dropdown', 'value', allow_duplicate=True),
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
    """Trigger a run creation via API and refresh run selection."""
    if not ctx.triggered_id:
        return no_update, no_update, no_update, no_update, no_update

    if not scenario_id or not agent_id:
        alert = dbc.Alert('Select both scenario and agent config before running.', color='warning', duration=3000)
        return no_update, no_update, alert, no_update, no_update

    safe_name = (name or 'unnamed_run').replace(' ', '_')
    payload = {
        'name': safe_name,
        'scenario': scenario_id,
        'agents': agent_id,
        'runs': int(runs or 1),
    }

    try:
        success, run_obj, err = api.create('run', payload)
    except Exception as exc:  # pylint: disable=broad-exception-caught
        logger.exception('Error starting run: %s', exc)
        alert = dbc.Alert('Failed to start run.', color='danger', duration=3000)
        return no_update, no_update, alert, no_update, no_update

    if not success or not run_obj:
        alert = dbc.Alert(f'Failed to start run: {err}', color='danger', duration=3000)
        return no_update, no_update, alert, no_update, no_update

    details = _render_run_details(run_obj)
    notification = dbc.Alert(f'Run started: {run_obj.get("name", "run")}', color='success', duration=3000)

    # refresh run list
    run_opts = []
    try:
        success_runs, runs_all, _ = api.get_all('run')
        if success_runs and runs_all:
            run_opts = [
                {'label': f"{r.get('name', 'run')} ({r.get('status', '').lower()})", 'value': r['id']}
                for r in runs_all
            ]
    except Exception as exc:  # pylint: disable=broad-exception-caught
        logger.exception('Error refreshing runs list: %s', exc)

    return run_obj, details, notification, run_opts or no_update, run_obj.get('id')


def _render_run_details(run_obj):
    """Format run details for display."""
    if not run_obj:
        return html.Div('No run yet.')

    details = [
        html.P([html.Strong('Name: '), run_obj.get('name')]),
        html.P([html.Strong('Status: '), run_obj.get('status', 'UNKNOWN')]),
        html.P([html.Strong('Scenario id: '), str(run_obj.get('scenario'))]),
        html.P([html.Strong('Agents id: '), str(run_obj.get('agents'))]),
        html.P([html.Strong('Runs: '), str(run_obj.get('runs'))]),
    ]
    return details


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


def _render_exports(exports):
    """Render a simple table/list of exports for a run."""
    if not exports:
        return html.Div('No exports found for this run yet.', className='text-muted')

    rows = []
    for exp in exports:
        link = (
            html.A('Download', href=exp.get('outfile'), target='_blank')
            if exp.get('outfile')
            else html.Span('Pending', className='text-muted')
        )
        rows.append(
            html.Tr(
                [
                    html.Td(exp.get('name', 'unnamed'), className='fw-semibold'),
                    html.Td(exp.get('export_type', '')),
                    html.Td(exp.get('created_at', '')),
                    html.Td(link),
                ]
            )
        )

    return dbc.Card(
        dbc.CardBody(
            [
                html.H5('Exports', className='mb-3'),
                dbc.Table(
                    [
                        html.Thead(
                            html.Tr(
                                [html.Th('Name'), html.Th('Type'), html.Th('Created'), html.Th('File')],
                                className='table-light',
                            )
                        ),
                        html.Tbody(rows),
                    ],
                    bordered=False,
                    striped=False,
                    hover=False,
                    responsive=True,
                    size='sm',
                ),
            ]
        )
    )


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
    simulation_name = _safe_resource_name(
        'simulation', (scenario or {}).get('sim') or (scenario or {}).get('simulation')
    )
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

    table_rows = [html.Tr([html.Th(label, className='w-25 text-muted small'), html.Td(value)]) for label, value in rows]

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


@callback(
    Output('dv-export-list', 'children'),
    Output('dv-notification-area', 'children', allow_duplicate=True),
    Input('dv-run-dropdown', 'value'),
    prevent_initial_call=True,
)
def _load_exports(run_id):
    """Load exports for the selected run and render in the visualisation area."""
    if not run_id:
        return html.Div('Select a run to view exports', className='text-center text-muted'), no_update

    try:
        success, exports, err = api.get_all('export', params={'run': run_id})
    except Exception as exc:  # pylint: disable=broad-exception-caught
        logger.exception('Error fetching exports for run %s: %s', run_id, exc)
        alert = dbc.Alert('Unable to load exports right now.', color='danger', duration=3000)
        return html.Div('Unable to load exports right now.', className='text-muted'), alert

    if not success:
        alert = dbc.Alert(f'Unable to load exports: {err}', color='danger', duration=3000)
        return html.Div('Unable to load exports right now.', className='text-muted'), alert

    exports = exports or []
    return _render_exports(exports), no_update
