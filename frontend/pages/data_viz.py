"""Data Visualisation Page for LocABS Application."""

from datetime import datetime
from typing import Any

import dash
import dash_ag_grid as dag
import dash_bootstrap_components as dbc
from dash import Input, Output, State, callback, ctx, dcc, html, no_update, register_page
from loguru import logger

from components.tooltip import create_tooltip
from utilities import api

register_page(__name__, path='/data-viz', name='Data Visualisation', title='LocABS · Data Visualisation')

EXPORT_TYPE_MAP = {
    'tab-animation': ('ANIMATION', 'Animation', 'my-animation'),
    'tab-snapshot': ('SNAPSHOT', 'Snapshot', 'my-snapshot'),
    'tab-excess-risk': ('EXCESS_RISK', 'Excess Risk', 'excess-risk'),
    'tab-epi-status': ('EPIDEMIOLOGICAL_STATUS', 'Epidemiological Status', 'epi-status'),
    'tab-viral-conc': ('VIRAL_CONCENTRATION', 'Viral Concentration', 'viral-conc'),
}

layout = html.Div(
    [
        dbc.Row(
            [
                # LEFT SIDEBAR
                dbc.Col(
                    [
                        html.H5('SIMULATION'),
                        html.P(
                            'Configure and launch a new simulation or view existing simulations and their results.',
                            className='dv-sidebar-description',
                        ),
                        html.Div(
                            [
                                html.Div(
                                    [
                                        dcc.Dropdown(
                                            id='dv-run-dropdown',
                                            options=[],
                                            placeholder='Select a run to view exports',
                                            clearable=True,
                                        ),
                                    ],
                                    className='dv-sidebar-section',
                                ),
                                html.H5('CREATE NEW SIMULATION', className='fw-bold'),
                                html.Div(
                                    [
                                        dbc.Label('Name', html_for='dv-name-input', className='dv-sidebar-form-label'),
                                        html.I(
                                            className='fa fa-circle-question dv-tooltip-icon',
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
                                                    className='dv-sidebar-form-label',
                                                ),
                                                html.I(
                                                    className='fa fa-circle-question dv-tooltip-icon',
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
                                    className='dv-sidebar-input-section',
                                ),
                                html.Div(
                                    [
                                        html.Div(
                                            [
                                                dbc.Label('Scenario', html_for='dv-scenario-dropdown'),
                                                html.I(
                                                    className='fa fa-circle-question dv-tooltip-icon',
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
                                    className='dv-sidebar-input-section',
                                ),
                                html.Div(
                                    [
                                        html.Div(
                                            [
                                                dbc.Label('Simulation Iterations', html_for='dv-runs-input'),
                                                html.I(
                                                    className='fa fa-circle-question dv-tooltip-icon',
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
                                    className='dv-sidebar-input-section',
                                ),
                                dbc.Button(
                                    'Start Simulation', id='dv-run-btn', color='primary', className='dv-sidebar-run-btn'
                                ),
                            ],
                            id='dv-run-form',
                        ),
                        html.Hr(),
                        html.Div(
                            id='dv-run-details',
                            className='border p-3',
                            children=[
                                dbc.Row(
                                    [
                                        dbc.Col(html.H4('Simulation Details', className='mb-0'), width='auto'),
                                        dbc.Col(
                                            dbc.Button(
                                                html.I(className='fa fa-times'),
                                                id='dv-close-run-btn',
                                                color='danger',
                                                size='sm',
                                                outline=True,
                                                style={'display': 'none'},
                                            ),
                                            width='auto',
                                        ),
                                    ],
                                    justify='between',
                                    align='center',
                                    className='mb-3',
                                ),
                                html.Div('No simulation yet.', id='dv-run-details-body'),
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
                                            className='dv-content-placeholder',
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
            children=[html.Div('Loading runs...', className='dv-summary-loading')],
            className='dv-summary w-100',
        ),
        # hidden store and init interval
        dcc.Store(id='dv-current-run'),
        dcc.Store(id='dv-run-metadata', storage_type='local'),
        dcc.Store(id='dv-viewer-state', storage_type='session'),
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
def _populate_dropdowns(_: int) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
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
        Output('dv-run-poll', 'disabled', allow_duplicate=True),
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
def _start_run(_n: int, name: str, agent_id: str, scenario_id: str, runs: int) -> tuple[Any, Any, Any, Any, Any, bool]:
    """Trigger a run creation via API and refresh run selection."""
    if not ctx.triggered_id:
        return no_update, no_update, no_update, no_update, no_update, no_update

    if not scenario_id or not agent_id:
        alert = dbc.Alert('Select both scenario and agent config before running.', color='warning', duration=3000)
        return no_update, no_update, alert, no_update, no_update, no_update

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
        return no_update, no_update, alert, no_update, no_update, no_update

    if not success or not run_obj:
        alert = dbc.Alert(f'Failed to start run: {err}', color='danger', duration=3000)
        return no_update, no_update, alert, no_update, no_update, no_update

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

    return run_obj, details, notification, run_opts or no_update, run_obj.get('id'), False


@callback(
    Output('dv-run-form', 'style'),
    Output('dv-run-details', 'style'),
    Output('dv-close-run-btn', 'style'),
    Input('dv-current-run', 'data'),
)
def _toggle_run_view(run_obj: Any) -> tuple[dict[str, str], dict[str, str], dict[str, str]]:
    """Hide form while a run is active and show the run details area."""
    if run_obj:
        status = run_obj.get('status', '').upper()
        # If run is completed/finished, show close button
        if status in ['SUCCESS', 'FAILED']:
            return {'display': 'none'}, {'display': 'block'}, {'display': 'block'}
        # If run is in progress, hide close button
        return {'display': 'none'}, {'display': 'block'}, {'display': 'none'}
    return {}, {'display': 'none'}, {'display': 'none'}


@callback(
    Output('dv-current-run', 'data', allow_duplicate=True),
    Output('dv-run-details-body', 'children', allow_duplicate=True),
    Output('dv-run-dropdown', 'options', allow_duplicate=True),
    Input('dv-run-poll', 'n_intervals'),
    State('dv-current-run', 'data'),
    prevent_initial_call=True,
)
def _poll_run_status(_n: int, run_obj: Any) -> tuple[Any, Any, Any]:
    """Poll the status of the current active run and update details."""
    if not run_obj:
        return no_update, no_update, no_update

    run_id = run_obj.get('id')
    if not run_id:
        return no_update, no_update, no_update

    try:
        success, updated_run, err = api.get_run_status(run_id)
    except Exception as exc:  # pylint: disable=broad-exception-caught
        logger.exception('Error polling run status for %s: %s', run_id, exc)
        return no_update, no_update, no_update

    if not success or not updated_run:
        return no_update, no_update, no_update

    # Update the run details display
    details = _render_run_details(updated_run)

    # Refresh the dropdown to show updated status
    run_opts = []
    try:
        success_runs, runs_all, _ = api.get_all('run')
        if success_runs and runs_all:
            run_opts = [
                {'label': f'{r.get("name", "run")} ({r.get("status", "").lower()})', 'value': r['id']} for r in runs_all
            ]
    except Exception as exc:  # pylint: disable=broad-exception-caught
        logger.exception('Error refreshing runs list: %s', exc)

    # Check if run is complete - if so, clear the current run to show the form again
    status = updated_run.get('status', '').upper()
    if status in ['COMPLETED', 'FAILED', 'CANCELLED', 'ERROR']:
        return None, details, run_opts or no_update

    return updated_run, details, run_opts or no_update


@callback(
    Output('dv-current-run', 'data', allow_duplicate=True),
    Output('dv-run-details-body', 'children', allow_duplicate=True),
    Output('dv-run-dropdown', 'options', allow_duplicate=True),
    Input('dv-close-run-btn', 'n_clicks'),
    prevent_initial_call=True,
)
def _close_run_details(_n: int) -> tuple[Any, Any, Any]:
    """Close the run details panel and return to form view."""
    if not _n:
        return no_update, no_update, no_update

    # Refresh the dropdown to show updated runs
    run_opts = []
    try:
        success_runs, runs_all, _ = api.get_all('run')
        if success_runs and runs_all:
            run_opts = [
                {'label': f'{r.get("name", "run")} ({r.get("status", "").lower()})', 'value': r['id']} for r in runs_all
            ]
    except Exception as exc:  # pylint: disable=broad-exception-caught
        logger.exception('Error refreshing runs list: %s', exc)

    details = html.Div('No simulation yet.')
    return None, details, run_opts or no_update


def _render_run_details(run_obj: Any) -> list[html.P]:
    """Format run details for display."""
    if not run_obj:
        return html.Div('No run yet.')

    if isinstance(run_obj, list):
        if not run_obj:
            return html.Div('No run yet.')
        run_obj = run_obj[0]

    status = run_obj.get('status', 'UNKNOWN').upper()

    details = [
        html.P(
            [html.Strong('Name: ', className='dv-run-details-label'), run_obj.get('name')],
            className='dv-run-details-text',
        ),
        html.P(
            [html.Strong('ID: ', className='dv-run-details-label'), str(run_obj.get('id'))],
            className='dv-run-details-text',
        ),
        html.P(
            [html.Strong('Status: ', className='dv-run-details-label'), status],
            className='dv-run-details-text',
        ),
        html.P(
            [html.Strong('Runs: ', className='dv-run-details-label'), str(run_obj.get('runs'))],
            className='dv-run-details-text',
        ),
    ]

    # Add success alert if run completed successfully
    if status == 'SUCCESS':
        details.insert(
            0,
            dbc.Alert(
                [html.I(className='fa fa-check-circle me-2'), 'Simulation completed successfully!'],
                color='success',
                className='mb-3',
            ),
        )
    elif status == 'FAILED':
        details.insert(
            0,
            dbc.Alert(
                [html.I(className='fa fa-exclamation-triangle me-2'), 'Simulation failed. Please check the logs.'],
                color='danger',
                className='mb-3',
            ),
        )

    return details


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


def _format_timestamp(iso_timestamp: str) -> str:
    """Format ISO timestamp to user-friendly format."""
    try:
        dt = datetime.fromisoformat(iso_timestamp.replace('Z', '+00:00'))
        return dt.strftime('%b %d, %Y %I:%M %p')
    except Exception:
        return iso_timestamp


def _render_exports(exports: list[dict[str, Any]], run_id: str, active_tab: str) -> html.Div:
    """Render a scrollable, sortable, filterable table of exports for a run."""
    if not exports:
        return html.Div('No exports found for this run yet.', className='text-muted')

    rows = []
    for exp in exports:
        exp_id = exp.get('id')
        outfile = exp.get('outfile', '')
        relative_path = outfile.replace('data/exports/', '') if outfile else ''

        view_btn = (
            dbc.Button(
                [html.I(className='fa fa-eye'), ' View'],
                id={'type': 'view-export-btn', 'export_id': exp_id, 'run': run_id, 'tab': active_tab},
                color='success',
                size='sm',
                className='dv-export-view-btn',
            )
            if relative_path
            else None
        )

        download_btn = (
            html.A(
                [html.I(className='fa fa-download'), ' Download'],
                href=f'/exports/{relative_path}',
                download=exp.get('name', 'export'),
                className='btn btn-sm btn-outline-primary dv-export-download-btn',
            )
            if relative_path
            else html.Span('Pending', className='dv-export-pending')
        )

        created_at = _format_timestamp(exp.get('created_at', '')) if exp.get('created_at') else ''

        rows.append(
            html.Tr(
                [
                    html.Td(exp.get('name', 'unnamed'), className='dv-export-name-cell'),
                    html.Td(exp.get('export_type', ''), className='dv-export-cell'),
                    html.Td(created_at, className='dv-export-cell'),
                    html.Td([view_btn, download_btn] if view_btn else download_btn, className='dv-export-actions-cell'),
                ]
            )
        )

    return dbc.Card(
        dbc.CardBody(
            [
                html.H5('Exports', className='dv-exports-header'),
                html.Div(
                    dbc.Table(
                        [
                            html.Thead(
                                html.Tr(
                                    [
                                        html.Th('Name'),
                                        html.Th('Type'),
                                        html.Th('Created'),
                                        html.Th('Actions'),
                                    ],
                                    className='table-light',
                                )
                            ),
                            html.Tbody(rows),
                        ],
                        bordered=False,
                        striped=True,
                        hover=True,
                        responsive=True,
                        size='sm',
                        className='dv-exports-table',
                    ),
                    className='dv-exports-table-wrapper',
                ),
            ]
        )
    )


def _create_export_form(
    run_id: str, active_tab: str, export_type: str, export_label: str, placeholder: str
) -> dbc.Card:
    """Create export generation form."""
    return dbc.Card(
        dbc.CardBody(
            [
                html.H5(f'Generate {export_label}', className='dv-export-form-header'),
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                html.Div(
                                    [
                                        dbc.Label('Export Name', className='dv-export-label'),
                                        html.I(
                                            className='fa fa-circle-question dv-tooltip-icon ms-1',
                                            id={'type': 'export-name-tooltip', 'run': run_id, 'tab': active_tab},
                                        ),
                                    ],
                                    className='d-flex align-items-center',
                                ),
                                create_tooltip(
                                    'Enter a name for your export file with a valid extension',
                                    {'type': 'export-name-tooltip', 'run': run_id, 'tab': active_tab},
                                    placement='top',
                                ),
                                dbc.Input(
                                    id={'type': 'export-name', 'run': run_id, 'tab': active_tab},
                                    type='text',
                                    placeholder=f'{placeholder}.gif',
                                    debounce=False,
                                    className='dv-export-input',
                                ),
                                html.Small(
                                    'Must include extension: .png, .gif, .svg, .html, or .pdf',
                                    className='dv-export-help-text',
                                ),
                            ],
                            width=8,
                        ),
                        dbc.Col(
                            [
                                dbc.Label('\u00a0', className='dv-export-btn-col-label'),
                                dbc.Button(
                                    [html.I(className='fa fa-file-export'), f' Generate {export_label}'],
                                    id={
                                        'type': 'generate-export-btn',
                                        'run': run_id,
                                        'tab': active_tab,
                                        'export_type': export_type,
                                    },
                                    color='primary',
                                    className='dv-export-btn',
                                ),
                            ],
                            width=4,
                        ),
                    ],
                    className='dv-export-form-row',
                ),
            ]
        ),
        className='dv-export-form',
    )


@callback(
    Output('dv-summary-table', 'children', allow_duplicate=True),
    Output('dv-run-metadata', 'data', allow_duplicate=True),
    [
        Input('dv-init', 'n_intervals'),
        Input('dv-run-btn', 'n_clicks'),
    ],
    State('dv-run-metadata', 'data'),
    prevent_initial_call='initial_duplicate',
)
def _load_runs_table(_init: int, _run_clicks: int, metadata: dict[str, Any]) -> tuple[Any, dict[str, Any]]:
    """Load runs table initially and after run creation."""
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
def _render_runs_table(_tick: int, metadata: dict[str, Any]) -> tuple[Any, dict[str, Any]]:
    """Render a table of runs covering the bottom space."""
    return _fetch_and_render_runs_table(metadata)


def _get_resource_maps() -> tuple[dict[int, str], dict[int, str]]:
    """Fetch scenarios and agents maps for efficient lookup."""
    scenarios_map = {}
    agents_map = {}
    try:
        _, scenarios, _ = api.get_all('scenario')
        _, agents, _ = api.get_all('agent_config')
        scenarios_map = {s['id']: s['name'] for s in (scenarios or []) if 'id' in s and 'name' in s}
        agents_map = {a['id']: a['name'] for a in (agents or []) if 'id' in a and 'name' in a}
    except Exception as exc:  # pylint: disable=broad-exception-caught
        logger.exception('Error fetching scenarios/agents for runs table: %s', exc)
    return scenarios_map, agents_map


def _get_resource_name(resource_obj: Any, resource_map: dict[int, str]) -> str:
    """Get resource name from object or map."""
    if isinstance(resource_obj, dict):
        return resource_obj.get('name', 'Unknown')
    if resource_obj:
        return resource_map.get(resource_obj, f'ID {resource_obj}')
    return 'Not selected'


def _process_run_data(
    r: dict[str, Any], metadata: dict[str, Any], scenarios_map: dict[int, str], agents_map: dict[int, str]
) -> dict[str, Any]:
    """Process a single run and return formatted row data."""
    run_id = str(r.get('id'))
    meta_entry = metadata.get(run_id, {})

    timestamp = r.get('created_at') or r.get('timestamp') or r.get('started_at') or meta_entry.get('timestamp')
    if not timestamp:
        timestamp = datetime.now().isoformat(timespec='seconds')

    str(r.get('status', '')).lower()
    duration = r.get('duration') or r.get('runtime') or r.get('run_time') or meta_entry.get('duration')
    if not duration:
        duration = _format_duration(timestamp)

    scenario_name = _get_resource_name(r.get('scenario'), scenarios_map)
    agent_name = _get_resource_name(r.get('agents'), agents_map)

    return {
        'timestamp': timestamp,
        'name': r.get('name', 'run'),
        'status': str(r.get('status', '')).upper(),
        'id': r.get('id'),
        'runs': r.get('runs'),
        'duration': duration,
        'scenario': scenario_name,
        'agent': agent_name,
    }


def _fetch_and_render_runs_table(metadata: dict[str, Any]) -> tuple[Any, dict[str, Any]]:
    """Render a table of runs covering the bottom space."""
    metadata = metadata or {}
    try:
        success, runs, err = api.get_all('run')
    except Exception as exc:  # pylint: disable=broad-exception-caught
        logger.exception('Error fetching runs table: %s', exc)
        return dbc.Alert('Unable to load runs right now.', color='danger', className='dv-summary-alert'), metadata

    if not success:
        return dbc.Alert(f'Unable to load runs: {err}', color='danger', className='dv-summary-alert'), metadata

    runs = runs or []
    if not runs:
        return html.Div('No runs yet.', className='dv-summary-empty'), metadata

    scenarios_map, agents_map = _get_resource_maps()

    updated_meta = dict(metadata)
    row_data = []

    for r in runs:
        run_data = _process_run_data(r, updated_meta, scenarios_map, agents_map)
        row_data.append(run_data)
        updated_meta[str(r.get('id'))] = {'timestamp': run_data['timestamp'], 'duration': run_data['duration']}

    column_defs = [
        {'headerName': 'Timestamp', 'field': 'timestamp', 'minWidth': 160},
        {'headerName': 'Run Name', 'field': 'name', 'minWidth': 160},
        {'headerName': 'Status', 'field': 'status', 'minWidth': 120},
        {'headerName': 'ID', 'field': 'id', 'minWidth': 100},
        {'headerName': '# Runs', 'field': 'runs', 'minWidth': 110},
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

    return dbc.Card(
        dbc.CardBody([html.H5('Runs', className='dv-summary-header'), grid]), className='dv-summary-card'
    ), updated_meta


@callback(
    Output('dv-content-area', 'children', allow_duplicate=True),
    Output('dv-notification-area', 'children', allow_duplicate=True),
    Output('dv-run-details-body', 'children', allow_duplicate=True),
    Output('dv-run-poll', 'disabled', allow_duplicate=True),
    Output('dv-viewer-state', 'data', allow_duplicate=True),
    [
        Input('dv-run-dropdown', 'value'),
        Input('dv-tabs', 'active_tab'),
    ],
    State('dv-viewer-state', 'data'),
    prevent_initial_call=True,
)
def _load_content(run_id: str, active_tab: str, viewer_state: dict):
    """Load content based on selected run and active tab."""
    if not ctx.triggered_id:
        return (
            html.Div('Select a simulation to view content', className='dv-content-placeholder'),
            no_update,
            no_update,
            True,
            {},
        )

    notification = no_update
    run_details = no_update
    poll_disabled = False
    error_result = None

    # Fetch run status
    try:
        run_success, run_data, run_err = api.get_run_status(run_id)
        if not run_success or not run_data:
            error_msg = f'Unable to load run status: {run_err}' if run_err else 'Unable to load run status right now.'
            error_result = (
                html.Div('Unable to load content right now.', className='dv-content-error'),
                dbc.Alert(error_msg, color='danger', duration=3000),
                run_details,
                True,
                {},
            )
    except Exception as exc:  # pylint: disable=broad-exception-caught
        logger.exception('Error fetching run status for run %s: %s', run_id, exc)
        error_result = (
            html.Div('Unable to load content right now.', className='dv-content-error'),
            dbc.Alert('Unable to load run status right now.', color='danger', duration=3000),
            run_details,
            True,
            {},
        )

    if error_result:
        return error_result

    run_details = _render_run_details(run_data)

    if active_tab not in EXPORT_TYPE_MAP:
        return (
            html.Div('Select a valid tab', className='dv-content-placeholder'),
            notification,
            run_details,
            poll_disabled,
            {},
        )

    export_type, export_label, placeholder = EXPORT_TYPE_MAP[active_tab]

    # Fetch exports
    try:
        success, all_exports, err = api.get_exports_for_run(run_id)
        if not success:
            error_msg = f'Unable to load exports: {err}' if err else 'Unable to load exports right now.'
            error_result = (
                html.Div('Unable to load exports.', className='dv-content-error'),
                dbc.Alert(error_msg, color='danger', duration=3000),
                run_details,
                poll_disabled,
                {},
            )
    except Exception as exc:  # pylint: disable=broad-exception-caught
        logger.exception('Error fetching exports for run %s: %s', run_id, exc)
        error_result = (
            html.Div('Unable to load exports.', className='dv-content-error'),
            dbc.Alert('Unable to load exports right now.', color='danger', duration=3000),
            run_details,
            poll_disabled,
            {},
        )

    if error_result:
        return error_result

    all_exports = all_exports or []
    exports = [exp for exp in all_exports if exp.get('export_type') == export_type]

    export_form = _create_export_form(run_id, active_tab, export_type, export_label, placeholder)

    exports_display = (
        _render_exports(exports, run_id, active_tab)
        if exports
        else html.Div(f'No {export_label.lower()} exports yet. Generate one above!', className='text-muted')
    )

    return html.Div([export_form, exports_display]), notification, run_details, poll_disabled, {}


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

    triggered = ctx.triggered_id
    export_type = triggered.get('export_type') if isinstance(triggered, dict) else 'ANIMATION'

    name = None
    if names:
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

    export_type_data = EXPORT_TYPE_MAP.get(active_tab, ('', '', ''))
    type_label = export_type_data[1] if len(export_type_data) > 1 else export_type
    alert = dbc.Alert(f'{type_label} export "{name}" created successfully!', color='success', duration=4000)

    try:
        success, all_exports, _ = api.get_exports_for_run(run_id)
        all_exports = all_exports or []
        exports = [exp for exp in all_exports if exp.get('export_type') == export_type]
    except Exception as exc:
        logger.exception('Error refreshing exports: %s', exc)
        return alert, no_update

    _, _, placeholder = EXPORT_TYPE_MAP[active_tab]
    export_form = _create_export_form(run_id, active_tab, export_type, type_label, placeholder)

    exports_display = (
        _render_exports(exports, run_id, active_tab)
        if exports
        else html.Div(f'No {type_label.lower()} exports yet. Generate one above!', className='text-muted')
    )
    return alert, html.Div([export_form, exports_display])


@callback(
    Output('dv-viewer-state', 'data', allow_duplicate=True),
    Input(
        {
            'type': 'view-export-btn',
            'export_id': dash.dependencies.ALL,
            'run': dash.dependencies.ALL,
            'tab': dash.dependencies.ALL,
        },
        'n_clicks',
    ),
    [
        State('dv-run-dropdown', 'value'),
        State('dv-tabs', 'active_tab'),
    ],
    prevent_initial_call=True,
)
def _view_export(n_clicks_list, run_id, active_tab):
    """Set viewer state to display the export."""
    if not ctx.triggered_id:
        return no_update

    actual_clicks = [n for n in (n_clicks_list or []) if n is not None and n > 0]
    if not actual_clicks:
        return no_update

    triggered = ctx.triggered_id
    export_id = triggered.get('export_id')

    if not export_id:
        return no_update

    try:
        success, export_data, err = api.get_by_id('export', export_id)
    except Exception as exc:
        logger.exception('Error fetching export %s: %s', export_id, exc)
        return no_update

    if not success or not export_data:
        return no_update

    return {'open': True, 'export_id': export_id, 'run_id': run_id, 'active_tab': active_tab}


@callback(
    Output('dv-content-area', 'children', allow_duplicate=True),
    Input('dv-viewer-state', 'data'),
    prevent_initial_call=True,
)
def _render_viewer(viewer_state: dict):
    """Render the export viewer when viewer_state indicates it should be shown."""
    if not viewer_state or not viewer_state.get('open'):
        return no_update

    export_id = viewer_state.get('export_id')
    run_id = viewer_state.get('run_id')
    active_tab = viewer_state.get('active_tab')

    if not export_id or not run_id or not active_tab:
        return no_update

    try:
        success, export_data, err = api.get_by_id('export', export_id)
    except Exception as exc:
        logger.exception('Error fetching export %s for viewer: %s', export_id, exc)
        return html.Div('Failed to load export', className='text-danger')

    if not success or not export_data:
        return html.Div('Export not found', className='text-danger')

    outfile = export_data.get('outfile', '')
    if not outfile:
        return html.Div('Export file not available', className='text-warning')

    if outfile.startswith('data/exports/'):
        relative_path = outfile[len('data/exports/') :]
    else:
        relative_path = outfile
    file_url = f'/exports/{relative_path}'

    file_ext = outfile.lower().split('.')[-1]

    # Create appropriate viewer based on file type
    if file_ext in ['png', 'jpg', 'jpeg', 'gif', 'svg']:
        content = html.Img(src=file_url, className='dv-export-viewer-image')
    elif file_ext in ['html', 'pdf']:
        content = html.Iframe(src=file_url, className='dv-export-viewer-iframe')
    else:
        content = html.Div(
            [
                html.P('Preview not available for this file type.', className='dv-export-viewer-no-preview-text'),
                html.A(
                    [html.I(className='fa fa-download'), ' Download File'],
                    href=file_url,
                    target='_blank',
                    className='btn btn-primary',
                ),
            ],
            className='dv-export-viewer-no-preview',
        )

    # Create viewer with close button
    viewer = dbc.Card(
        dbc.CardBody(
            [
                dbc.Row(
                    [
                        dbc.Col(
                            html.H5(export_data.get('name', 'Export'), className='dv-export-viewer-title'),
                            className='d-flex align-items-center',
                        ),
                        dbc.Col(
                            [
                                html.A(
                                    [html.I(className='fa fa-download'), ' Download'],
                                    href=file_url,
                                    download=export_data.get('name', 'export'),
                                    className='btn btn-primary btn-sm me-2',
                                ),
                                dbc.Button(
                                    html.I(className='fa fa-times'),
                                    id={'type': 'close-export-btn', 'run': run_id, 'tab': active_tab},
                                    color='danger',
                                    size='sm',
                                    outline=True,
                                ),
                            ],
                            width='auto',
                            className='ms-auto d-flex align-items-center',
                        ),
                    ],
                    className='dv-export-viewer-header',
                ),
                html.Hr(),
                html.Div(content, className='dv-export-viewer-content'),
            ]
        ),
        className='dv-export-viewer',
    )

    return viewer


@callback(
    Output('dv-content-area', 'children', allow_duplicate=True),
    Output('dv-viewer-state', 'data', allow_duplicate=True),
    Input({'type': 'close-export-btn', 'run': dash.dependencies.ALL, 'tab': dash.dependencies.ALL}, 'n_clicks'),
    prevent_initial_call=True,
)
def _close_export_view(n_clicks_list):
    """Close export view and return to export list."""
    if not ctx.triggered_id:
        return no_update, no_update

    actual_clicks = [n for n in (n_clicks_list or []) if n is not None and n > 0]
    if not actual_clicks:
        return no_update, no_update

    triggered = ctx.triggered_id
    run_id = triggered.get('run')
    active_tab = triggered.get('tab')

    if not run_id or active_tab not in EXPORT_TYPE_MAP:
        return no_update, no_update

    export_type, export_label, placeholder = EXPORT_TYPE_MAP[active_tab]

    try:
        success, all_exports, _ = api.get_exports_for_run(run_id)
        exports = [exp for exp in (all_exports or []) if exp.get('export_type') == export_type]
    except Exception as exc:
        logger.exception('Error refreshing exports: %s', exc)
        return no_update, no_update

    export_form = _create_export_form(run_id, active_tab, export_type, export_label, placeholder)
    exports_display = (
        _render_exports(exports, run_id, active_tab)
        if exports
        else html.Div(f'No {export_label.lower()} exports yet. Generate one above!', className='text-muted')
    )

    return html.Div([export_form, exports_display]), {}
