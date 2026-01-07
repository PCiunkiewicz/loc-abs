"""Data Visualisation Page for LocABS Application."""

import dash
from dash import html, dcc, register_page, callback, Output, Input, State, ctx, no_update
from datetime import datetime
import dash_ag_grid as dag
import dash_bootstrap_components as dbc
from utilities import api
from loguru import logger
from components.tooltip import create_tooltip

register_page(__name__, path='/data-viz', name='Data Visualisation', title='LocABS · Data Visualisation')

layout = html.Div(
    [
        dbc.Row(
            [
                # LEFT SIDEBAR
                dbc.Col(
                    [
                        html.H5('SIMULATION', className='mb-3'),
                        html.P(
                            'Configure and launch a new simulation or view existing simulations and their results.',
                            className='dv-sidebar-description',
                        ),
                        html.Div(
                            [
                                html.Div(
                                    [
                                        html.Div(
                                            [
                                                dbc.Label('Simulation', html_for='dv-run-dropdown'),
                                                html.I(
                                                    className='fa fa-circle-question ms-2 dv-tooltip-icon',
                                                    id='dv-run-dropdown-tooltip',
                                                ),
                                            ],
                                            className='dv-label-container',
                                        ),
                                        create_tooltip(
                                            'Select a previous run to view its results and exports',
                                            'dv-run-dropdown-tooltip',
                                            placement='top',
                                        ),
                                        html.P(
                                            'View results from completed simulations',
                                            className='dv-helper-text',
                                        ),
                                        dcc.Dropdown(
                                            id='dv-run-dropdown',
                                            options=[],
                                            placeholder='Select a run to view exports',
                                            clearable=True,
                                        ),
                                    ],
                                    className='mb-4',
                                ),
                                html.Hr(className='mb-3'),
                                html.H6('CREATE NEW SIMULATION', className='mb-3 fw-bold'),
                                html.Div(
                                    [
                                        dbc.Label('Name', html_for='dv-name-input', className='form-label'),
                                        html.I(
                                            className='fa fa-circle-question ms-2 dv-tooltip-icon',
                                            id='dv-name-tooltip',
                                        ),
                                    ],
                                    className='dv-label-container',
                                ),
                                create_tooltip(
                                    'Give your simulation a unique name for easy identification',
                                    'dv-name-tooltip',
                                    placement='top',
                                ),
                                html.P(
                                    'Unique identifier for this simulation run',
                                    className='dv-helper-text',
                                ),
                                dbc.Input(
                                    id='dv-name-input',
                                    type='text',
                                    placeholder='Enter run name',
                                    className='form-control',
                                ),
                                html.Div(
                                    [
                                        html.Div(
                                            [
                                                dbc.Label(
                                                    'Participant Configuration',
                                                    html_for='dv-agent-dropdown',
                                                    className='form-label',
                                                ),
                                                html.I(
                                                    className='fa fa-circle-question ms-2 dv-tooltip-icon',
                                                    id='dv-agent-tooltip',
                                                ),
                                            ],
                                            className='dv-label-container',
                                        ),
                                        create_tooltip(
                                            'Select how participants in the facility behave and move',
                                            'dv-agent-tooltip',
                                            placement='top',
                                        ),
                                        html.P(
                                            'Defines participant behavior and population',
                                            className='dv-helper-text',
                                        ),
                                        dcc.Dropdown(
                                            id='dv-agent-dropdown', options=[], placeholder='Choose an option here'
                                        ),
                                    ],
                                    className='mt-3',
                                ),
                                html.Div(
                                    [
                                        html.Div(
                                            [
                                                dbc.Label('Scenario', html_for='dv-scenario-dropdown'),
                                                html.I(
                                                    className='fa fa-circle-question ms-2 dv-tooltip-icon',
                                                    id='dv-scenario-tooltip',
                                                ),
                                            ],
                                            className='dv-label-container',
                                        ),
                                        create_tooltip(
                                            'Choose scenario settings including outbreak and prevention measures',
                                            'dv-scenario-tooltip',
                                            placement='top',
                                        ),
                                        html.P(
                                            'Scenario setup with outbreak and protective measures',
                                            className='dv-helper-text',
                                        ),
                                        dcc.Dropdown(
                                            id='dv-scenario-dropdown', options=[], placeholder='Choose an option here'
                                        ),
                                    ],
                                    className='mt-3',
                                ),
                                html.Div(
                                    [
                                        html.Div(
                                            [
                                                dbc.Label('Simulation Iterations', html_for='dv-runs-input'),
                                                html.I(
                                                    className='fa fa-circle-question ms-2 dv-tooltip-icon',
                                                    id='dv-runs-tooltip',
                                                ),
                                            ],
                                            className='dv-label-container',
                                        ),
                                        create_tooltip(
                                            'Number of simulation iterations to run with the same settings',
                                            'dv-runs-tooltip',
                                            placement='top',
                                        ),
                                        html.P(
                                            'How many times to execute the simulation',
                                            className='dv-helper-text',
                                        ),
                                        dbc.Input(
                                            id='dv-runs-input',
                                            type='number',
                                            min=1,
                                            step=1,
                                            value=1,
                                            className='form-control w-100',
                                        ),
                                    ],
                                    className='mt-3',
                                ),
                                dbc.Button(
                                    'Start Simulation', id='dv-run-btn', color='primary', className='btn w-100 mt-3'
                                ),
                            ],
                            id='dv-run-form',
                        ),
                        html.Hr(),
                        html.Div(
                            id='dv-run-details',
                            className='border p-3',
                            children=[
                                html.H6('Simulation Details'),
                                html.Div('No simulation yet.', id='dv-run-details-body'),
                                dbc.Button(
                                    'Cancel Simulation',
                                    id='dv-cancel-btn',
                                    color='danger',
                                    outline=True,
                                    className='w-100 mt-3',
                                ),
                                dbc.Button(
                                    'Go to Decision Support',
                                    id='dv-goto-decision',
                                    color='info',
                                    className='w-100',
                                    href='/decision-support',
                                ),
                            ],
                            style={'display': 'none'},
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
                                dbc.Col(dbc.Button('Export', id='dv-export-btn', color='secondary'), width='auto'),
                            ],
                            justify='end',
                            className='mb-2',
                        ),
                        dbc.Tabs(
                            [
                                dbc.Tab(label='Animation', tab_id='tab-animation'),
                                dbc.Tab(label='Snapshot', tab_id='tab-snapshot'),
                                dbc.Tab(label='Excess Risk', tab_id='tab-excess-risk'),
                                dbc.Tab(label='Epidemiological Status', tab_id='tab-epi-status'),
                                dbc.Tab(label='Viral Concentration', tab_id='tab-viral-conc'),
                            ],
                            id='dv-tabs',
                            active_tab='tab-animation',
                        ),
                        html.Div(
                            dcc.Loading(
                                html.Div(
                                    id='dv-content-area',
                                    children=[
                                        html.Div(
                                            'Select a simulation to view or generate exports',
                                            className='text-center text-muted',
                                            style={'paddingLeft': '20px'},
                                        )
                                    ],
                                    className='dv-summary',
                                ),
                                type='circle',
                            ),
                            className='dv-graph-wrap',
                        ),
                    ],
                    width=9,
                ),
            ],
            className='g-4',
        ),
        # BOTTOM SUMMARY TABLE
        html.Div(
            id='dv-summary-table',
            children=[html.Div('Loading runs...', className='text-center text-muted mt-5')],
            className='dv-summary w-100',
        ),
        # hidden store and init interval
        dcc.Store(id='dv-current-run'),
        dcc.Store(id='dv-run-metadata', storage_type='local'),
        dcc.Interval(id='dv-init', interval=500, n_intervals=0, max_intervals=1),
        dcc.Interval(id='dv-run-poll', interval=3000, n_intervals=0, disabled=True),
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
        {'label': f'{r.get("name", "run")} ({r.get("status", "").lower()})', 'value': r['id']} for r in (runs or [])
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

    notification = None
    try:
        start_ok, _, start_err = api.start_run(run_obj['id'])
        if not start_ok:
            notification = dbc.Alert(f'Run created but failed to start: {start_err}', color='danger', duration=4000)
    except Exception as exc:  # pylint: disable=broad-exception-caught
        logger.exception('Error enqueueing run %s: %s', run_obj.get('id'), exc)
        notification = dbc.Alert('Run created but failed to start.', color='danger', duration=4000)

    details = _render_run_details(run_obj)
    notification = notification or dbc.Alert(
        f'Run started: {run_obj.get("name", "run")}', color='success', duration=3000
    )

    # refresh run list
    run_opts = []
    try:
        success_runs, runs_all, _ = api.get_all('run')
        if success_runs and runs_all:
            run_opts = [
                {'label': f'{r.get("name", "run")} ({r.get("status", "").lower()})', 'value': r['id']} for r in runs_all
            ]
    except Exception as exc:  # pylint: disable=broad-exception-caught
        logger.exception('Error refreshing runs list: %s', exc)

    return run_obj, details, notification, run_opts or no_update, run_obj.get('id')


@callback(
    Output('dv-run-form', 'style'),
    Output('dv-run-details', 'style'),
    Output('dv-cancel-btn', 'disabled'),
    Input('dv-current-run', 'data'),
)
def _toggle_run_view(run_obj):
    """Hide form while a run is active and show the run details/cancel area."""
    if run_obj:
        return {'display': 'none'}, {'display': 'block'}, False
    return {}, {'display': 'none'}, True


@callback(
    Output('dv-current-run', 'data', allow_duplicate=True),
    Output('dv-run-details-body', 'children', allow_duplicate=True),
    Output('dv-notification-area', 'children', allow_duplicate=True),
    Output('dv-run-dropdown', 'options', allow_duplicate=True),
    Output('dv-run-dropdown', 'value', allow_duplicate=True),
    Input('dv-cancel-btn', 'n_clicks'),
    State('dv-current-run', 'data'),
    prevent_initial_call=True,
)
def _cancel_run(_n, run_obj):
    """Cancel the active run and restore the form."""
    if not _n or not run_obj:
        return no_update, no_update, no_update, no_update, no_update

    run_id = run_obj.get('id')
    try:
        success, _, err = api.update('run', run_id, {'status': 'CANCELLED'})
    except Exception as exc:  # pylint: disable=broad-exception-caught
        logger.exception('Error cancelling run %s: %s', run_id, exc)
        alert = dbc.Alert('Failed to cancel run.', color='danger', duration=3000)
        return no_update, no_update, alert, no_update, no_update

    if not success:
        alert = dbc.Alert(f'Failed to cancel run: {err}', color='danger', duration=3000)
        return no_update, no_update, alert, no_update, no_update

    run_opts = []
    try:
        success_runs, runs_all, _ = api.get_all('run')
        if success_runs and runs_all:
            run_opts = [
                {'label': f'{r.get("name", "run")} ({r.get("status", "").lower()})', 'value': r['id']} for r in runs_all
            ]
    except Exception as exc:  # pylint: disable=broad-exception-caught
        logger.exception('Error refreshing runs list after cancel: %s', exc)

    details = html.Div('No run yet.')
    notification = dbc.Alert('Run cancelled.', color='warning', duration=3000)
    return None, details, notification, run_opts or no_update, None


def _render_run_details(run_obj):
    """Format run details for display."""
    if not run_obj:
        return html.Div('No run yet.')

    details = [
        html.P([html.Strong('Name: '), run_obj.get('name')]),
        html.P([html.Strong('ID: '), str(run_obj.get('id'))]),
        html.P([html.Strong('Status: '), run_obj.get('status', 'UNKNOWN')]),
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


def _format_duration(start_iso: str) -> str:
    """Return human-friendly duration from iso timestamp to now."""
    try:
        start = datetime.fromisoformat(start_iso)
    except Exception:
        return 'N/A'
    delta = datetime.now() - start
    seconds = int(delta.total_seconds())
    if seconds < 0:
        return 'N/A'
    mins, secs = divmod(seconds, 60)
    hours, mins = divmod(mins, 60)
    if hours:
        return f'{hours}h {mins:02d}m'
    if mins:
        return f'{mins}m {secs:02d}s'
    return f'{secs}s'


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
    Output('dv-summary-table', 'children', allow_duplicate=True),
    Output('dv-run-metadata', 'data', allow_duplicate=True),
    [
        Input('dv-init', 'n_intervals'),
        Input('dv-run-btn', 'n_clicks'),
        Input('dv-cancel-btn', 'n_clicks'),
    ],
    State('dv-run-metadata', 'data'),
    prevent_initial_call='initial_duplicate',
)
def _load_runs_table(_init, _run_clicks, _cancel_clicks, metadata):
    """Load runs table initially and after run creation/cancellation."""
    return _fetch_and_render_runs_table(metadata)


@callback(
    Output('dv-summary-table', 'children'),
    Output('dv-run-metadata', 'data', allow_duplicate=True),
    [
        Input('dv-run-poll', 'n_intervals'),
    ],
    State('dv-run-metadata', 'data'),
    prevent_initial_call='initial_duplicate',
)
def _render_runs_table(_tick, metadata):
    """Render a table of runs covering the bottom space."""
    return _fetch_and_render_runs_table(metadata)


def _fetch_and_render_runs_table(metadata):
    """Render a table of runs covering the bottom space."""
    metadata = metadata or {}
    try:
        success, runs, err = api.get_all('run')
    except Exception as exc:  # pylint: disable=broad-exception-caught
        logger.exception('Error fetching runs table: %s', exc)
        return dbc.Alert('Unable to load runs right now.', color='danger', className='mb-0'), metadata

    if not success:
        return dbc.Alert(f'Unable to load runs: {err}', color='danger', className='mb-0'), metadata

    runs = runs or []
    if not runs:
        return html.Div('No runs yet.', className='text-center text-muted mt-3'), metadata

    # Fetch all scenarios and agents once for efficient lookup
    scenarios_map = {}
    agents_map = {}
    try:
        _, scenarios, _ = api.get_all('scenario')
        _, agents, _ = api.get_all('agent_config')
        scenarios_map = {s['id']: s['name'] for s in (scenarios or []) if 'id' in s and 'name' in s}
        agents_map = {a['id']: a['name'] for a in (agents or []) if 'id' in a and 'name' in a}
    except Exception as exc:  # pylint: disable=broad-exception-caught
        logger.exception('Error fetching scenarios/agents for runs table: %s', exc)

    updated_meta = dict(metadata)
    row_data = []
    terminal = {'failed', 'cancelled', 'error', 'stopped', 'success', 'completed', 'finished'}
    for r in runs:
        run_id = str(r.get('id'))
        meta_entry = updated_meta.get(run_id, {})

        timestamp = r.get('created_at') or r.get('timestamp') or r.get('started_at') or meta_entry.get('timestamp')
        if not timestamp:
            timestamp = datetime.now().isoformat(timespec='seconds')

        status = str(r.get('status', '')).lower()
        duration = r.get('duration') or r.get('runtime') or r.get('run_time') or meta_entry.get('duration')
        if not duration:
            duration = _format_duration(timestamp)
            if status in terminal:
                duration = _format_duration(timestamp)

        # Get scenario name - check if embedded, otherwise lookup from map
        scenario_obj = r.get('scenario')
        if isinstance(scenario_obj, dict):
            scenario_name = scenario_obj.get('name', 'Unknown')
        elif scenario_obj:
            scenario_name = scenarios_map.get(scenario_obj, f'ID {scenario_obj}')
        else:
            scenario_name = 'Not selected'

        # Get agent name - check if embedded, otherwise lookup from map
        agent_obj = r.get('agents')
        if isinstance(agent_obj, dict):
            agent_name = agent_obj.get('name', 'Unknown')
        elif agent_obj:
            agent_name = agents_map.get(agent_obj, f'ID {agent_obj}')
        else:
            agent_name = 'Not selected'

        row_data.append(
            {
                'timestamp': timestamp,
                'name': r.get('name', 'run'),
                'status': str(r.get('status', '')).upper(),
                'id': r.get('id'),
                'runs': r.get('runs'),
                'duration': duration,
                'scenario': scenario_name,
                'agent': agent_name,
            }
        )
        updated_meta[run_id] = {'timestamp': timestamp, 'duration': duration}

    column_defs = [
        {'headerName': 'Timestamp', 'field': 'timestamp', 'minWidth': 160},
        {'headerName': 'Run Name', 'field': 'name', 'minWidth': 160},
        {'headerName': 'Status', 'field': 'status', 'minWidth': 120},
        {'headerName': 'ID', 'field': 'id', 'maxWidth': 90},
        {'headerName': '# Runs', 'field': 'runs', 'maxWidth': 110},
        {'headerName': 'Scenario', 'field': 'scenario', 'minWidth': 160},
        {'headerName': 'Agent Config', 'field': 'agent', 'minWidth': 160},
    ]

    grid = dag.AgGrid(
        id='dv-runs-grid',
        columnDefs=column_defs,
        rowData=row_data,
        defaultColDef={
            'resizable': True,
            'sortable': True,
            'filter': True,
        },
        dashGridOptions={
            'pagination': True,
            'paginationPageSize': 10,
            'animateRows': True,
        },
        className='ag-theme-alpine w-100',
    )

    return dbc.Card(dbc.CardBody([html.H5('Runs', className='mb-3'), grid]), className='w-100'), updated_meta


@callback(
    Output('dv-content-area', 'children'),
    Output('dv-notification-area', 'children', allow_duplicate=True),
    Output('dv-run-details-body', 'children', allow_duplicate=True),
    Output('dv-run-poll', 'disabled'),
    [
        Input('dv-run-dropdown', 'value'),
        Input('dv-tabs', 'active_tab'),
    ],
    [
        State('dv-content-area', 'children'),
    ],
    prevent_initial_call=True,
)
def _load_content(run_id, active_tab, current_content):
    """Load content based on selected run and active tab."""
    if not run_id:
        return (
            html.Div(
                'Select a simulation to view content', className='text-center text-muted', style={'paddingLeft': '20px'}
            ),
            no_update,
            no_update,
            True,
        )

    notification = no_update
    run_details = no_update
    poll_disabled = False

    try:
        run_success, run_data, run_err = api.get_run_status(run_id)
    except Exception as exc:  # pylint: disable=broad-exception-caught
        logger.exception('Error fetching run status for run %s: %s', run_id, exc)
        alert = dbc.Alert('Unable to load run status right now.', color='danger', duration=3000)
        return (
            html.Div('Unable to load content right now.', className='text-muted', style={'paddingLeft': '20px'}),
            alert,
            run_details,
            True,
        )

    if not run_success or not run_data:
        alert = dbc.Alert(f'Unable to load run status: {run_err}', color='danger', duration=3000)
        return (
            html.Div('Unable to load content right now.', className='text-muted', style={'paddingLeft': '20px'}),
            alert,
            run_details,
            True,
        )

    run_details = _render_run_details(run_data)
    status = str(run_data.get('status', '')).lower()

    # Map tab to export type
    export_type_map = {
        'tab-animation': ('ANIMATION', 'Animation', 'my-animation'),
        'tab-snapshot': ('SNAPSHOT', 'Snapshot', 'my-snapshot'),
        'tab-excess-risk': ('EXCESS_RISK', 'Excess Risk', 'excess-risk'),
        'tab-epi-status': ('EPIDEMIOLOGICAL_STATUS', 'Epidemiological Status', 'epi-status'),
        'tab-viral-conc': ('VIRAL_CONCENTRATION', 'Viral Concentration', 'viral-conc'),
    }

    if active_tab not in export_type_map:
        return (
            html.Div('Select a valid tab', className='text-center text-muted', style={'paddingLeft': '20px'}),
            notification,
            run_details,
            poll_disabled,
        )

    export_type, export_label, placeholder = export_type_map[active_tab]

    try:
        success, all_exports, err = api.get_exports_for_run(run_id)
    except Exception as exc:  # pylint: disable=broad-exception-caught
        logger.exception('Error fetching exports for run %s: %s', run_id, exc)
        alert = dbc.Alert('Unable to load exports right now.', color='danger', duration=3000)
        return (
            html.Div('Unable to load exports.', className='text-muted', style={'paddingLeft': '20px'}),
            alert,
            run_details,
            poll_disabled,
        )

    if not success:
        alert = dbc.Alert(f'Unable to load exports: {err}', color='danger', duration=3000)
        return (
            html.Div('Unable to load exports.', className='text-muted', style={'paddingLeft': '20px'}),
            alert,
            run_details,
            poll_disabled,
        )

    all_exports = all_exports or []
    # Filter exports by type for this tab
    exports = [exp for exp in all_exports if exp.get('export_type') == export_type]

    # Create export generation form for this specific type
    export_form = dbc.Card(
        dbc.CardBody(
            [
                html.H5(f'Generate {export_label}', className='mb-3'),
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                dbc.Label('Export Name'),
                                dbc.Input(
                                    id={'type': 'export-name', 'run': run_id, 'tab': active_tab},
                                    type='text',
                                    placeholder=f'{placeholder}.gif',
                                    debounce=False,
                                    className='form-control',
                                ),
                                html.Small(
                                    'Must include extension: .png, .gif, .svg, .html, or .pdf',
                                    className='form-text text-muted',
                                ),
                            ],
                            width=8,
                        ),
                        dbc.Col(
                            [
                                dbc.Label('\u00a0'),  # Non-breaking space for alignment
                                dbc.Button(
                                    [html.I(className='fa fa-file-export me-2'), f'Generate {export_label}'],
                                    id={
                                        'type': 'generate-export-btn',
                                        'run': run_id,
                                        'tab': active_tab,
                                        'export_type': export_type,
                                    },
                                    color='primary',
                                    className='w-100',
                                ),
                            ],
                            width=4,
                        ),
                    ],
                    className='mb-3',
                ),
                html.Hr(className='mb-3'),
                html.H5(f'View Existing {export_label}s', className='mb-3'),
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                dbc.Label('Select Export to View'),
                                dcc.Dropdown(
                                    id={'type': 'export-select', 'run': run_id, 'tab': active_tab},
                                    options=[
                                        {
                                            'label': f'{exp.get("name", "Unnamed")} (ID: {exp.get("id")})',
                                            'value': exp.get('id'),
                                        }
                                        for exp in exports
                                    ],
                                    placeholder='Select an export to visualize',
                                    clearable=True,
                                ),
                            ],
                            width=12,
                        ),
                    ],
                    className='mb-3',
                )
                if exports
                else None,
            ]
        ),
        className='mb-3',
    )

    exports_display = (
        _render_exports(exports)
        if exports
        else html.Div(f'No {export_label.lower()} exports yet. Generate one above!', className='text-muted')
    )

    return html.Div([export_form, exports_display]), notification, run_details, poll_disabled


@callback(
    Output('dv-notification-area', 'children', allow_duplicate=True),
    Output('dv-content-area', 'children', allow_duplicate=True),
    Input(
        {
            'type': 'generate-export-btn',
            'run': dash.dependencies.ALL,
            'tab': dash.dependencies.ALL,
            'export_type': dash.dependencies.ALL,
        },
        'n_clicks',
    ),
    [
        State({'type': 'export-name', 'run': dash.dependencies.ALL, 'tab': dash.dependencies.ALL}, 'value'),
        State('dv-run-dropdown', 'value'),
        State('dv-tabs', 'active_tab'),
    ],
    prevent_initial_call=True,
)
def _generate_export(n_clicks_list, names, run_id, active_tab):
    """Generate a new export when the button is clicked."""
    if not ctx.triggered_id:
        return no_update, no_update

    if not run_id:
        alert = dbc.Alert('Please select a simulation run first', color='warning', duration=3000)
        return alert, no_update

    # Get export type from triggered button
    triggered = ctx.triggered_id
    export_type = triggered.get('export_type') if isinstance(triggered, dict) else 'ANIMATION'

    # Get the name from the input - names is a list of values from all matching inputs
    name = None
    if names:
        # Find the first non-empty name
        for n in names:
            if n:
                name = n
                break

    if not name:
        alert = dbc.Alert('Please enter an export name', color='warning', duration=3000)
        return alert, no_update

    # Validate file extension
    valid_extensions = {'.png', '.gif', '.svg', '.html', '.pdf'}
    name_lower = name.lower()

    if not any(name_lower.endswith(ext) for ext in valid_extensions):
        alert = dbc.Alert(
            'Export name must include a valid extension: .png, .gif, .svg, .html, or .pdf',
            color='warning',
            duration=4000,
        )
        return alert, no_update

    try:
        success, export_data, err = api.create_export(run_id, name, export_type)
    except Exception as exc:
        logger.exception('Error creating export: %s', exc)
        alert = dbc.Alert(f'Failed to create export: {str(exc)}', color='danger', duration=3000)
        return alert, no_update

    if not success:
        alert = dbc.Alert(f'Failed to create export: {err}', color='danger', duration=4000)
        return alert, no_update

    # Map export type to friendly name
    type_labels = {
        'ANIMATION': 'Animation',
        'SNAPSHOT': 'Snapshot',
        'EXCESS_RISK': 'Excess Risk',
        'EPIDEMIOLOGICAL_STATUS': 'Epidemiological Status',
        'VIRAL_CONCENTRATION': 'Viral Concentration',
    }
    type_label = type_labels.get(export_type, export_type)

    alert = dbc.Alert(
        f'{type_label} export "{name}" created successfully!',
        color='success',
        duration=4000,
    )

    # Refresh the exports list for the current type
    try:
        success, all_exports, _ = api.get_exports_for_run(run_id)
        all_exports = all_exports or []
        exports = [exp for exp in all_exports if exp.get('export_type') == export_type]
    except Exception as exc:
        logger.exception('Error refreshing exports: %s', exc)
        return alert, no_update

    # Map tab to placeholder
    placeholder_map = {
        'tab-animation': 'my-animation',
        'tab-snapshot': 'my-snapshot',
        'tab-excess-risk': 'excess-risk',
        'tab-epi-status': 'epi-status',
        'tab-viral-conc': 'viral-conc',
    }
    placeholder = placeholder_map.get(active_tab, 'my-export')

    # Recreate the export form and display
    export_form = dbc.Card(
        dbc.CardBody(
            [
                html.H5(f'Generate {type_label}', className='mb-3'),
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                dbc.Label('Export Name'),
                                dbc.Input(
                                    id={'type': 'export-name', 'run': run_id, 'tab': active_tab},
                                    type='text',
                                    placeholder=f'{placeholder}.gif',
                                    debounce=False,
                                    className='form-control',
                                ),
                                html.Small(
                                    'Must include extension: .png, .gif, .svg, .html, or .pdf',
                                    className='form-text text-muted',
                                ),
                            ],
                            width=8,
                        ),
                        dbc.Col(
                            [
                                dbc.Label('\u00a0'),
                                dbc.Button(
                                    [html.I(className='fa fa-file-export me-2'), f'Generate {type_label}'],
                                    id={
                                        'type': 'generate-export-btn',
                                        'run': run_id,
                                        'tab': active_tab,
                                        'export_type': export_type,
                                    },
                                    color='primary',
                                    className='w-100',
                                ),
                            ],
                            width=4,
                        ),
                    ],
                    className='mb-3',
                ),
                html.Hr(className='mb-3'),
                html.H5(f'View Existing {type_label}s', className='mb-3'),
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                dbc.Label('Select Export to View'),
                                dcc.Dropdown(
                                    id={'type': 'export-select', 'run': run_id, 'tab': active_tab},
                                    options=[
                                        {
                                            'label': f'{exp.get("name", "Unnamed")} (ID: {exp.get("id")})',
                                            'value': exp.get('id'),
                                        }
                                        for exp in exports
                                    ],
                                    placeholder='Select an export to visualize',
                                    clearable=True,
                                ),
                            ],
                            width=12,
                        ),
                    ],
                    className='mb-3',
                )
                if exports
                else None,
            ]
        ),
        className='mb-3',
    )

    exports_display = (
        _render_exports(exports)
        if exports
        else html.Div(f'No {type_label.lower()} exports yet. Generate one above!', className='text-muted')
    )
    return alert, html.Div([export_form, exports_display])


@callback(
    Output('dv-notification-area', 'children', allow_duplicate=True),
    Input({'type': 'export-select', 'run': dash.dependencies.ALL, 'tab': dash.dependencies.ALL}, 'value'),
    [
        State('dv-run-dropdown', 'value'),
        State('dv-tabs', 'active_tab'),
    ],
    prevent_initial_call=True,
)
def _view_selected_export(export_ids, run_id, active_tab):
    """Display details of the selected export."""
    if not ctx.triggered_id or not export_ids or not export_ids[0]:
        return no_update

    export_id = export_ids[0]

    try:
        success, export_data, err = api.get_by_id('export', export_id)
    except Exception as exc:
        logger.exception('Error fetching export %s: %s', export_id, exc)
        alert = dbc.Alert('Failed to load export details', color='danger', duration=3000)
        return alert

    if not success:
        alert = dbc.Alert(f'Failed to load export: {err}', color='danger', duration=3000)
        return alert

    # Create a detailed view of the export
    export_info = dbc.Alert(
        [
            html.H5(f'Export: {export_data.get("name", "Unnamed")}', className='mb-3'),
            html.Hr(),
            html.P([html.Strong('Type: '), export_data.get('export_type', 'Unknown')]),
            html.P([html.Strong('ID: '), str(export_data.get('id', 'N/A'))]),
            html.P([html.Strong('Output File: '), export_data.get('outfile', 'Not set')]),
            html.P([html.Strong('Created: '), export_data.get('created_at', 'Unknown')]),
            html.P([html.Strong('Parameters: '), str(export_data.get('params', {}))]),
        ],
        color='info',
        dismissable=True,
    )

    return export_info
