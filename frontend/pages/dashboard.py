"""Dashboard page wired to backend runs."""

import dash_ag_grid as dag
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
from dash import Input, Output, callback, dcc, html, register_page, State

from components.tooltip import create_info_icon_with_tooltip, create_tooltip
from utilities import api

register_page(__name__, path='/dashboard', name='Dashboard', title='LocABS Dashboard')


def _name_from_field(val, resource: str) -> str:
    """Best-effort readable label with API call fallback for IDs."""
    if val is None:
        return 'N/A'
    if isinstance(val, dict):
        return val.get('name') or str(val.get('id', 'N/A'))

    # If it's just an ID (number or string), fetch the name from API
    try:
        success, data, _ = api.get(resource, val)
        if success and data and isinstance(data, dict):
            return data.get('name', str(val))
    except Exception:  # pylint: disable=broad-exception-caught
        pass

    return str(val)


def _build_runs_df() -> tuple[pd.DataFrame, str | None]:
    """Fetch runs from API and normalize into a dataframe."""
    try:
        success, runs, err = api.get_all('run')
    except Exception as exc:  # pylint: disable=broad-exception-caught
        return pd.DataFrame(), str(exc)

    if not success:
        return pd.DataFrame(), err or 'Unable to load runs'

    rows = []
    for r in runs or []:
        ts_raw = r.get('created_at') or r.get('timestamp') or r.get('started_at')
        ts_dt = pd.to_datetime(ts_raw, errors='coerce')
        timestamp = ts_dt.strftime('%Y-%m-%d %H:%M:%S') if pd.notnull(ts_dt) else ''
        duration_val = r.get('duration') or r.get('runtime') or r.get('run_time')
        try:
            duration_min = round(float(duration_val), 2) if duration_val is not None else None
        except (TypeError, ValueError):
            duration_min = None

        rows.append(
            {
                'run_name': r.get('name', 'run'),
                'run_id': r.get('id'),
                'status': str(r.get('status', '')).upper(),
                'duration_min': duration_min,
                'timestamp': timestamp,
                'scenario': _name_from_field(r.get('scenario'), 'scenario'),
                'agent': _name_from_field(r.get('agents'), 'agent_config'),
                'runs': r.get('runs'),
                'ts_dt': ts_dt,
            }
        )

    df = pd.DataFrame(rows)
    if not df.empty:
        df['duration_display'] = df['duration_min'].apply(lambda m: f'{m} min' if m is not None else 'N/A')
        df.sort_values(by='ts_dt', ascending=False, inplace=True, ignore_index=True)
    return df, None


def kpi_card(title, value, subtitle=None, value_id=None, tooltip_text=None, max_value=None, current_value=None):
    """KPI card with optional tooltip and progress bar."""
    card_id = f'{value_id}-card' if value_id else None

    progress_bar = None
    ratio_text = None
    if max_value is not None and current_value is not None:
        try:
            percentage = min(100, (float(current_value) / float(max_value)) * 100) if float(max_value) > 0 else 0
        except (ValueError, TypeError):
            percentage = 0

        progress_bar = html.Div(
            [
                html.Div(
                    style={
                        'width': f'{percentage}%',
                        'height': '100%',
                        'backgroundColor': '#60a5fa',
                        'borderRadius': '4px',
                        'transition': 'width 0.3s ease',
                    }
                ),
            ],
            className='progress-bar-container',
        )

        ratio_text = html.Div(
            f'{current_value} / {max_value}',
            className='ratio-text',
        )

    card = dbc.Card(
        dbc.CardBody(
            [
                html.Div(
                    [
                        html.Span(title),
                        html.I(className='fa fa-info-circle ms-1 kpi-info-icon') if tooltip_text else None,
                    ],
                    className='kpi-title',
                    id=card_id,
                ),
                html.H2(value, className='kpi-value', id=value_id),
                html.Div(
                    [
                        progress_bar if progress_bar else None,
                        ratio_text if max_value is not None else None,
                    ],
                    className='kpi-footer',
                ),
                html.Div(subtitle or '', className='kpi-subtitle'),
            ]
        ),
        className='metric-card',
    )

    if tooltip_text and card_id:
        return html.Div(
            [
                card,
                create_tooltip(tooltip_text, card_id, placement='top'),
            ]
        )
    return card


def last_run_summary(run: dict) -> html.Div:
    """Render last run summary details."""
    items = [
        ('Simulation Name', run.get('run_name', 'N/A')),
        ('Simulation ID', f'#{run.get("run_id", "N/A")}'),
        ('Number of Tests', run.get('runs', 'N/A')),
        ('Scenario Used', run.get('scenario', 'N/A')),
        ('People Configuration', run.get('agent', 'N/A')),
    ]
    rows = [html.Tr([html.Th(label), html.Td(val)]) for label, val in items]
    return dbc.Card(
        dbc.CardBody(
            [
                html.Div(
                    [
                        create_info_icon_with_tooltip(
                            'Latest Simulation Summary',
                            'Detailed information about the most recently completed simulation, including the scenario used and people behavior configuration.',
                            'latest-simulation-summary',
                        ),
                    ]
                ),
                dbc.Table(rows, bordered=False, striped=False, hover=False, size='sm', className='summary-table'),
            ]
        ),
        className='summary-card',
    )


def duration_line(df: pd.DataFrame):
    """Render duration line chart as a complete Graph component."""
    if df.empty:
        return html.Div(
            html.P(
                'Graph is not available at this moment. No simulation data found.',
                className='graph-placeholder',
            ),
            className='graph-placeholder-container',
        )

    fig = px.line(
        df.sort_values('ts_dt'),
        x='timestamp',
        y='duration_min',
        markers=True,
        labels={'timestamp': 'Date & Time', 'duration_min': 'Duration (minutes)'},
    )
    fig.update_layout(
        margin={'l': 10, 'r': 10, 't': 10, 'b': 10},
        height=300,
        hovermode='x unified',
    )
    return dcc.Graph(
        id='duration-graph',
        figure=fig,
        config={
            'displayModeBar': True,
            'displaylogo': False,
            'modeBarButtonsToAdd': ['drawline', 'drawopenpath', 'eraseshape'],
            'toImageButtonOptions': {
                'format': 'png',
                'filename': 'duration_chart',
                'height': 400,
                'width': 400,
                'scale': 1,
            },
        },
        className='duration-graph-container',
    )


def status_bar(df: pd.DataFrame):
    """Render status bar chart as a complete Graph component."""
    if df.empty:
        return html.Div(
            html.P(
                'Graph is not available at this moment. No simulation data found.',
                className='graph-placeholder',
            ),
            className='graph-placeholder-container',
        )

    agg = df.groupby('status')['run_id'].count().reset_index(name='count')
    fig = px.bar(
        agg,
        x='status',
        y='count',
        labels={'count': 'Number of Simulations', 'status': 'Result'},
    )
    fig.update_layout(
        margin={'l': 10, 'r': 10, 't': 30, 'b': 10},
        height=270,
        hovermode='closest',
    )
    return dcc.Graph(
        id='status-graph',
        figure=fig,
        config={
            'displayModeBar': True,
            'displaylogo': False,
            'toImageButtonOptions': {
                'format': 'png',
                'filename': 'status_chart',
                'height': 500,
                'width': 700,
                'scale': 1,
            },
        },
        className='status-graph-container',
    )


column_defs = [
    {
        'field': 'run_name',
        'headerName': 'Simulation Name',
        'minWidth': 150,
        'cellRenderer': 'markdown',
        'tooltipField': 'run_name',
    },
    {'field': 'run_id', 'headerName': 'ID #', 'maxWidth': 80, 'hide': True},
    {
        'field': 'status',
        'headerName': 'Result',
        'maxWidth': 120,
        'cellClassRules': {
            'status-success': "value === 'SUCCESS'",
            'status-failed': "value === 'FAILED'",
            'status-running': "value === 'RUNNING'",
        },
    },
    {'field': 'timestamp', 'headerName': 'When', 'minWidth': 150},
    {'field': 'duration_display', 'headerName': 'Duration', 'maxWidth': 100},
]


@callback(
    Output('kpi-cards-container', 'children'),
    Input('dashboard-metadata', 'data'),
    Input('kpi-scenarios', 'children'),
    Input('kpi-agents', 'children'),
    Input('kpi-last-duration', 'children'),
    Input('kpi-total-runs', 'children'),
)
def update_kpi_cards(metadata, scenarios, agents, duration, total_runs):
    """Update KPI cards with progress bars showing current/max values."""
    # Parse current values
    try:
        scenarios_val = int(scenarios) if scenarios not in ['N/A', '—', '...', None] else 0
    except (ValueError, TypeError):
        scenarios_val = 0

    try:
        agents_val = int(agents) if agents not in ['N/A', '—', '...', None] else 0
    except (ValueError, TypeError):
        agents_val = 0

    try:
        runs_val = int(total_runs) if total_runs not in ['0', 'N/A', None] else 0
    except (ValueError, TypeError):
        runs_val = 0

    return [
        kpi_card(
            'Number of Scenarios Created',
            scenarios,
            value_id='kpi-scenarios-display',
            tooltip_text='Total number of different scenarios that have been created for the simulation. '
            'Each scenario represents a unique test condition or situation.',
            max_value=1000,
            current_value=scenarios_val,
        ),
        kpi_card(
            'Number of Participant Profiles',
            agents,
            value_id='kpi-agents-display',
            tooltip_text='Number of different participant profiles configured. '
            'Each profile defines how individuals behave and make decisions in the facility.',
            max_value=20,
            current_value=agents_val,
        ),
        kpi_card(
            'Latest Simulation Duration',
            duration,
            value_id='kpi-duration-display',
            tooltip_text='How long the most recent simulation took to complete (in minutes).',
        ),
        kpi_card(
            'Total Simulations',
            total_runs,
            value_id='kpi-runs-display',
            tooltip_text='Total number of simulations completed using all scenarios and people configurations.',
            max_value=100,
            current_value=runs_val,
        ),
    ]


@callback(
    Output('glossary-modal', 'is_open'),
    Input('glossary-open-btn', 'n_clicks'),
    Input('glossary-close-btn', 'n_clicks'),
    State('glossary-modal', 'is_open'),
    prevent_initial_call=True,
)
def toggle_glossary(n_open, n_close, is_open):
    """Toggle glossary modal."""
    return not is_open


@callback(
    Output('recent-activity-grid', 'rowData'),
    Output('duration-graph-container', 'children'),
    Output('status-graph-container', 'children'),
    Output('last-run-summary', 'children'),
    Output('kpi-scenarios', 'children'),
    Output('kpi-agents', 'children'),
    Output('kpi-last-duration', 'children'),
    Output('kpi-total-runs', 'children'),
    Output('dashboard-metadata', 'data', allow_duplicate=True),
    Output('last-updated-text', 'children'),
    Input('runs-refresh', 'n_intervals'),
    Input('time-filter', 'value'),
    Input('manual-refresh-btn', 'n_clicks'),
    State('dashboard-metadata', 'data'),
    prevent_initial_call='initial_duplicate',
)
def update_dashboard(_n, time_filter, _refresh_clicks, metadata):
    """Update dashboard components periodically."""
    df, err = _build_runs_df()
    if err:
        df = pd.DataFrame()

    if not df.empty and time_filter:
        now = pd.Timestamp.now()
        if time_filter == '24h':
            df = df[df['ts_dt'] >= (now - pd.Timedelta(hours=24))]
        elif time_filter == '7d':
            df = df[df['ts_dt'] >= (now - pd.Timedelta(days=7))]
        elif time_filter == '30d':
            df = df[df['ts_dt'] >= (now - pd.Timedelta(days=30))]

    meta = metadata or {}
    scenario_count = meta.get('scenarios', '...')
    agent_cfg_count = meta.get('agent_configs', '...')
    if scenario_count in {'...', None}:
        try:
            success_s, scenarios, _ = api.get_all('scenario')
            if success_s and scenarios is not None:
                scenario_count = str(len(scenarios))
        except Exception:
            scenario_count = 'N/A'
    if agent_cfg_count in {'...', None}:
        try:
            success_a, agents, _ = api.get_all('agent_config')
            if success_a and agents is not None:
                agent_cfg_count = str(len(agents))
        except Exception:
            agent_cfg_count = 'N/A'

    row_data = (
        df[['run_name', 'run_id', 'status', 'timestamp', 'duration_display']].to_dict('records') if not df.empty else []
    )

    duration_graph = duration_line(df)
    status_graph = status_bar(df)

    if df.empty:
        summary = last_run_summary({})
        kpi_scenarios = scenario_count
        kpi_agents = agent_cfg_count
        kpi_last_duration = 'N/A'
        kpi_total_runs = '0'
    else:
        latest = df.iloc[0].to_dict()
        summary = last_run_summary(latest)
        kpi_scenarios = scenario_count
        kpi_agents = agent_cfg_count
        kpi_last_duration = latest.get('duration_display', 'N/A')
        kpi_total_runs = str(len(df))

    meta.update({'scenarios': scenario_count, 'agent_configs': agent_cfg_count})
    last_updated = pd.Timestamp.now().strftime('%I:%M:%S %p')
    return (
        row_data,
        duration_graph,
        status_graph,
        summary,
        kpi_scenarios,
        kpi_agents,
        kpi_last_duration,
        kpi_total_runs,
        meta,
        f'Last updated: {last_updated}',
    )


layout = html.Div(
    [
        dcc.Interval(id='runs-refresh', interval=5000, n_intervals=0),
        dcc.Store(id='dashboard-metadata'),
        dbc.Modal(
            [
                dbc.ModalHeader(dbc.ModalTitle('Understanding Your Dashboard')),
                dbc.ModalBody(
                    [
                        html.H5('Key Terms Explained', className='glossary-title'),
                        html.Div(
                            [
                                html.H6('Simulation', className='glossary-term-title'),
                                html.P(
                                    'A test run of a scenario with specific people behaviors. '
                                    'Think of it as pressing "play" to see what happens in your facility under certain conditions.'
                                ),
                                html.Hr(),
                                html.H6('Scenario', className='glossary-term-title'),
                                html.P(
                                    'The scenario and conditions for your test. '
                                    'This includes the facility layout, starting positions, and any special circumstances.'
                                ),
                                html.Hr(),
                                html.H6('Number of Participant Profiles', className='glossary-term-title'),
                                html.P(
                                    'The different behavior profiles configured for participants in your simulation. '
                                    'Each profile determines how individuals move, react, and make decisions.'
                                ),
                                html.Hr(),
                                html.H6('Result Status', className='glossary-term-title'),
                                html.P(
                                    html.Ul(
                                        [
                                            html.Li(
                                                [html.Strong('Success: '), 'The simulation completed without issues.']
                                            ),
                                            html.Li([html.Strong('Failed: '), 'The simulation encountered an error.']),
                                            html.Li(
                                                [
                                                    html.Strong('Running: '),
                                                    'The simulation is currently in progress.',
                                                ]
                                            ),
                                        ]
                                    )
                                ),
                            ]
                        ),
                    ]
                ),
                dbc.ModalFooter(
                    dbc.Button('Close', id='glossary-close-btn', color='secondary', className='glossary-close-button')
                ),
            ],
            id='glossary-modal',
            size='lg',
            is_open=False,
        ),
        html.Div(
            [
                html.Div(
                    [
                        html.Div(
                            [
                                html.Div(
                                    [
                                        html.H4(
                                            'Quick Overview', className='section-subtitle', style={'display': 'inline'}
                                        ),
                                        html.I(
                                            className='fa fa-info-circle ms-1',
                                            id='overview-info-icon',
                                            style={'fontSize': '0.875rem', 'color': '#6c757d'},
                                        ),
                                    ],
                                    style={'display': 'flex', 'alignItems': 'center', 'gap': '0.25rem'},
                                ),
                                html.Small(
                                    id='last-updated-text',
                                    className='last-updated-text',
                                    children='Last updated: --:--:-- --',
                                ),
                            ],
                            className='overview-text',
                        ),
                        dbc.Button(
                            'Learn More',
                            id='glossary-open-btn',
                            color='link',
                            size='sm',
                            className='learn-more-button',
                        ),
                        create_tooltip(
                            'Summary of key metrics and performance indicators for your simulations.',
                            'overview-info-icon',
                            placement='top',
                        ),
                    ],
                    className='overview-left',
                ),
                html.Div(
                    [
                        html.Label('Time Period:', className='filter-label'),
                        dcc.Dropdown(
                            id='time-filter',
                            options=[
                                {'label': 'All Time', 'value': 'all'},
                                {'label': 'Last 24 Hours', 'value': '24h'},
                                {'label': 'Last 7 Days', 'value': '7d'},
                                {'label': 'Last 30 Days', 'value': '30d'},
                            ],
                            value='all',
                            clearable=False,
                            className='filter-dropdown',
                        ),
                        html.Button(
                            html.I(className='fa fa-refresh'),
                            id='manual-refresh-btn',
                            className='refresh-button',
                            title='Refresh dashboard',
                        ),
                    ],
                    className='filter-container',
                ),
            ],
            className='dashboard-filter-bar',
        ),
        html.Div(
            id='kpi-cards-container',
            className='cards-row',
        ),
        html.Div(id='kpi-scenarios', style={'display': 'none'}),
        html.Div(id='kpi-agents', style={'display': 'none'}),
        html.Div(id='kpi-last-duration', style={'display': 'none'}),
        html.Div(id='kpi-total-runs', style={'display': 'none'}),
        html.Div(
            [
                dbc.Card(
                    dbc.CardBody(
                        [
                            create_info_icon_with_tooltip(
                                'Recent Simulations',
                                'List of your most recent simulations showing name, ID number, and result. '
                                'Click column headers to sort the list, or use the search bar to find specific simulations.',
                                'recent-activity-title',
                            ),
                            html.P(
                                'Your recent simulations with sortable columns and search filters.',
                                className='card-description',
                            ),
                            dag.AgGrid(
                                id='recent-activity-grid',
                                columnDefs=column_defs,
                                rowData=[],
                                defaultColDef={'resizable': True, 'sortable': True, 'filter': True},
                                dashGridOptions={
                                    'pagination': True,
                                    'paginationPageSize': 5,
                                    'animateRows': True,
                                },
                                className='ag-theme-alpine activity-grid',
                                columnSize='sizeToFit',
                            ),
                        ]
                    ),
                    className='panel-card',
                ),
                dbc.Card(
                    dbc.CardBody(
                        [
                            create_info_icon_with_tooltip(
                                'How Long Simulations Take',
                                'Timeline showing how many minutes each simulation took to complete. '
                                'Use the toolbar buttons to zoom in/out, move around the chart, or download the image. '
                                'Hover your mouse over any point to see exact details.',
                                'duration-chart-title',
                            ),
                            html.P(
                                'See how simulation duration changes over time with interactive chart controls.',
                                className='card-description',
                            ),
                            html.Div(id='duration-graph-container'),
                        ]
                    ),
                    className='panel-card',
                ),
            ],
            className='split-row',
        ),
        html.Div(),
        html.Div(
            [
                html.Div(id='last-run-summary'),
                dbc.Card(
                    dbc.CardBody(
                        [
                            create_info_icon_with_tooltip(
                                'Simulation Results',
                                'Bar chart showing how many simulations completed successfully, failed, or are still in progress. '
                                'Use the toolbar to zoom, explore, or download the chart. '
                                'Hover your mouse over any bar to see the exact number.',
                                'status-chart-title',
                            ),
                            html.P(
                                'See how your simulations are performing with interactive chart controls.',
                                className='card-description',
                            ),
                            html.Div(id='status-graph-container'),
                        ]
                    ),
                    className='panel-card',
                ),
            ],
            className='split-row',
        ),
    ],
    className='dashboard-shell',
)
