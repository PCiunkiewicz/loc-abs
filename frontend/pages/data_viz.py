"""Data Visualisation Page for LocABS Application."""

from dash import html, dcc, register_page, callback, Output, Input, State, ctx, no_update
from datetime import datetime
import dash_ag_grid as dag
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
                                html.Div(
                                    [
                                        dbc.Label(
                                            'Agent Configuration', html_for='dv-agent-dropdown', className='form-label'
                                        ),
                                        dcc.Dropdown(
                                            id='dv-agent-dropdown', options=[], placeholder='Choose an option here'
                                        ),
                                    ],
                                    className='mt-3',
                                ),
                                html.Div(
                                    [
                                        dbc.Label('Scenarios', html_for='dv-scenario-dropdown'),
                                        dcc.Dropdown(
                                            id='dv-scenario-dropdown', options=[], placeholder='Choose an option here'
                                        ),
                                    ],
                                    className='mt-3',
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
                                    ],
                                    className='mt-3',
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
                                    className='mt-3',
                                ),
                                dbc.Button(
                                    'Run Simulation', id='dv-run-btn', color='primary', className='btn w-100 mt-3'
                                ),
                            ],
                            id='dv-run-form',
                        ),
                        html.Hr(),
                        html.Div(
                            id='dv-run-details',
                            className='border p-3',
                            children=[
                                html.H6('Run Details'),
                                html.Div('No run yet.', id='dv-run-details-body'),
                                dbc.Button(
                                    'Cancel Run',
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
                                html.Div(
                                    id='dv-export-list',
                                    children=[
                                        html.Div('Select a run to view exports', className='text-center text-muted')
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
        dcc.Interval(id='dv-init', interval=500, n_intervals=0, max_intervals=0),
        dcc.Interval(id='dv-run-poll', interval=500, n_intervals=0, disabled=True),
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
    Output('dv-summary-table', 'children'),
    Output('dv-run-metadata', 'data', allow_duplicate=True),
    [
        Input('dv-init', 'n_intervals'),
        Input('dv-run-poll', 'n_intervals'),
        Input('dv-run-btn', 'n_clicks'),
        Input('dv-cancel-btn', 'n_clicks'),
    ],
    State('dv-run-metadata', 'data'),
    prevent_initial_call='initial_duplicate',
)
def _render_runs_table(_init, _tick, _run_clicks, _cancel_clicks, metadata):
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

        scenario_name = (
            r.get('scenario', {}).get('name')
            if isinstance(r.get('scenario'), dict)
            else _safe_resource_name('scenario', r.get('scenario'))
        )
        agent_name = (
            r.get('agents', {}).get('name')
            if isinstance(r.get('agents'), dict)
            else _safe_resource_name('agent_config', r.get('agents'))
        )
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
        {'headerName': 'Duration', 'field': 'duration', 'minWidth': 120},
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
    Output('dv-export-list', 'children'),
    Output('dv-notification-area', 'children', allow_duplicate=True),
    Output('dv-run-details-body', 'children', allow_duplicate=True),
    Output('dv-run-poll', 'disabled'),
    [Input('dv-run-dropdown', 'value'), Input('dv-run-poll', 'n_intervals')],
    prevent_initial_call=True,
)
def _load_exports(run_id, _tick):
    """Load exports for the selected run and render in the visualisation area."""
    if not run_id:
        return (
            html.Div('Select a run to view exports', className='text-center text-muted'),
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
        return html.Div('Unable to load exports right now.', className='text-muted'), alert, run_details, True

    if not run_success or not run_data:
        alert = dbc.Alert(f'Unable to load run status: {run_err}', color='danger', duration=3000)
        return html.Div('Unable to load exports right now.', className='text-muted'), alert, run_details, True

    run_details = _render_run_details(run_data)
    status = str(run_data.get('status', '')).lower()
    terminal_statuses = {'completed', 'finished', 'failed', 'cancelled', 'error', 'stopped', 'success'}

    try:
        success, exports, err = api.get_all('export', params={'run': run_id})
    except Exception as exc:  # pylint: disable=broad-exception-caught
        logger.exception('Error fetching exports for run %s: %s', run_id, exc)
        alert = dbc.Alert('Unable to load exports right now.', color='danger', duration=3000)
        return html.Div('Unable to load exports right now.', className='text-muted'), alert, run_details, poll_disabled

    if not success:
        alert = dbc.Alert(f'Unable to load exports: {err}', color='danger', duration=3000)
        return html.Div('Unable to load exports right now.', className='text-muted'), alert, run_details, poll_disabled

    exports = exports or []
    has_exports = bool(exports)
    poll_disabled = status in {'failed', 'cancelled', 'error', 'stopped'} or (
        status in terminal_statuses and has_exports
    )

    if status in terminal_statuses:
        if has_exports:
            notification = dbc.Alert('Run completed. Exports ready.', color='success', duration=3000)
        elif status in {'failed', 'cancelled', 'error', 'stopped'}:
            notification = dbc.Alert(f'Run ended with status: {status.upper()}', color='warning', duration=3000)
        else:
            notification = dbc.Alert('Run finished but no exports yet.', color='warning', duration=3000)

    return _render_exports(exports), notification, run_details, poll_disabled
