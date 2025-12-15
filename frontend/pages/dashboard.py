"""Dashboard page wired to backend runs."""

import dash_ag_grid as dag
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
from dash import Input, Output, callback, dcc, html, register_page, State

from utilities import api

register_page(__name__, path='/', name='Dashboard', title='LocABS Dashboard')


def _name_from_field(val, _resource: str) -> str:
    """Best-effort readable label without extra API calls."""
    if val is None:
        return 'N/A'
    if isinstance(val, dict):
        return val.get('name') or str(val.get('id', 'N/A'))
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


def kpi_card(title, value, subtitle=None, value_id=None):
    """Simple KPI card."""
    return dbc.Card(
        dbc.CardBody(
            [
                html.Div(title, className='kpi-title'),
                html.H2(value, className='kpi-value', id=value_id),
                html.Div(subtitle or '', className='kpi-subtitle'),
            ]
        ),
        className='metric-card',
    )


def last_run_summary(run: dict) -> html.Div:
    """Render last run summary details."""
    items = [
        ('Run Name', run.get('run_name', 'N/A')),
        ('Run ID', f'#{run.get("run_id", "N/A")}'),
        ('# Runs', run.get('runs', 'N/A')),
        ('Scenario', run.get('scenario', 'N/A')),
        ('Agent Config', run.get('agent', 'N/A')),
    ]
    rows = [html.Tr([html.Th(label), html.Td(val)]) for label, val in items]
    return dbc.Card(
        dbc.CardBody(
            [
                html.H4('Last Run Summary', className='card-title'),
                dbc.Table(rows, bordered=False, striped=False, hover=False, size='sm', className='summary-table'),
            ]
        ),
        className='summary-card',
    )


def duration_line(df: pd.DataFrame):
    """Render duration line chart."""
    if df.empty:
        fig = px.line(title='Run Duration Over Time')
    else:
        fig = px.line(
            df.sort_values('ts_dt'),
            x='timestamp',
            y='duration_min',
            markers=True,
            labels={'timestamp': 'Timestamp', 'duration_min': 'Duration (min)'},
        )
    fig.update_layout(margin={'l': 10, 'r': 10, 't': 40, 'b': 10}, height=280)
    return fig


def status_bar(df: pd.DataFrame):
    """Render status bar chart."""
    if df.empty:
        fig = px.bar(title='Runs by Status')
    else:
        agg = df.groupby('status')['run_id'].count().reset_index(name='count')
        fig = px.bar(agg, x='status', y='count', title='Runs by Status', labels={'count': 'Count', 'status': 'Status'})
    fig.update_layout(margin={'l': 10, 'r': 10, 't': 40, 'b': 10}, height=280)
    return fig


column_defs = [
    {'field': 'run_name', 'headerName': 'Run Name', 'minWidth': 140},
    {'field': 'run_id', 'headerName': 'Run ID', 'maxWidth': 90},
    {
        'field': 'status',
        'headerName': 'Status',
        'cellClassRules': {
            'status-success': "value === 'SUCCESS'",
            'status-failed': "value === 'FAILED'",
            'status-running': "value === 'RUNNING'",
        },
    },
    {'field': 'duration_min', 'headerName': 'Duration (min)', 'maxWidth': 140},
    {'field': 'timestamp', 'headerName': 'Timestamp', 'minWidth': 160},
]


@callback(
    Output('recent-activity-grid', 'rowData'),
    Output('duration-graph', 'figure'),
    Output('status-graph', 'figure'),
    Output('last-run-summary', 'children'),
    Output('kpi-scenarios', 'children'),
    Output('kpi-agents', 'children'),
    Output('kpi-last-duration', 'children'),
    Output('kpi-total-runs', 'children'),
    Output('dashboard-metadata', 'data', allow_duplicate=True),
    Input('runs-refresh', 'n_intervals'),
    State('dashboard-metadata', 'data'),
    prevent_initial_call='initial_duplicate',
)
def update_dashboard(_n, metadata):
    """Update dashboard components periodically."""
    df, err = _build_runs_df()
    if err:
        df = pd.DataFrame()

    meta = metadata or {}
    scenario_count = meta.get('scenarios', '...')
    agent_cfg_count = meta.get('agent_configs', '...')
    # fetch counts only if unknown
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
        df[['run_name', 'run_id', 'status', 'duration_min', 'timestamp']].to_dict('records') if not df.empty else []
    )

    duration_fig = duration_line(df)
    status_fig = status_bar(df)

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
    return (
        row_data,
        duration_fig,
        status_fig,
        summary,
        kpi_scenarios,
        kpi_agents,
        kpi_last_duration,
        kpi_total_runs,
        meta,
    )


layout = html.Div(
    [
        dcc.Interval(id='runs-refresh', interval=1000, n_intervals=0),
        dcc.Store(id='dashboard-metadata'),
        html.Div(
            [
                html.H2('Simulation Dashboard', className='overview-title'),
                html.P('Fast overview of runs, statuses, and timing.', className='overview-description'),
            ],
            className='overview-section compact',
        ),
        html.Div(
            [
                kpi_card('Total Scenarios', '—', value_id='kpi-scenarios'),
                kpi_card('Total Agents', '—', value_id='kpi-agents'),
                kpi_card('Last Simulation Duration', '—', value_id='kpi-last-duration'),
                kpi_card('Total Runs', '—', value_id='kpi-total-runs'),
            ],
            className='cards-row',
        ),
        html.Div(
            [
                dbc.Card(
                    dbc.CardBody(
                        [
                            html.H4('Recent Activity', className='card-title'),
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
                            html.H4('Run Duration Over Time', className='card-title'),
                            dcc.Graph(id='duration-graph', config={'displayModeBar': False}, style={'height': '260px'}),
                        ]
                    ),
                    className='panel-card',
                ),
            ],
            className='split-row',
        ),
        html.Div(
            [
                html.Div(id='last-run-summary'),
                dbc.Card(
                    dbc.CardBody(
                        [
                            html.H4('Run Status Overview', className='card-title'),
                            dcc.Graph(id='status-graph', config={'displayModeBar': False}, style={'height': '260px'}),
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
