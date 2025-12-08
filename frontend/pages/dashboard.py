"""Dashboard Page for LocABS Application."""

from datetime import datetime

import dash_ag_grid as dag
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
from dash import Input, Output, callback, dcc, html, register_page

register_page(__name__, path='/', name='Dashboard', title='LocABS · Dashboard')


# Sample data for recent activity table
# TODO: Replace with actual data fetching logic or database queries later
recent_activity_data = pd.DataFrame(
    [
        {
            'scenario': 'Baseline A',
            'run_id': '#1842',
            'status': 'Success',
            'duration': '03:12',
            'timestamp': '2025-10-28 09:14',
        },
        {
            'scenario': 'Baseline B',
            'run_id': '#1841',
            'status': 'Failed',
            'duration': '00:47',
            'timestamp': '2025-10-28 08:50',
        },
        {
            'scenario': 'What-if C',
            'run_id': '#1840',
            'status': 'Success',
            'duration': '04:05',
            'timestamp': '2025-10-28 08:20',
        },
    ]
)

ColumnDefs = [
    {'field': 'scenario', 'headerName': 'Scenario'},
    {'field': 'run_id', 'headerName': 'Run ID'},
    {
        'field': 'status',
        'headerName': 'Status',
        'cellStyle': {
            'styleConditions': [
                {'condition': "params.value == 'Success'", 'style': {'color': '#28a745', 'fontWeight': '600'}},
                {'condition': "params.value == 'Failed'", 'style': {'color': '#dc3545', 'fontWeight': '600'}},
                {'condition': "params.value == 'Running'", 'style': {'color': '#17a2b8', 'fontWeight': '600'}},
            ]
        },
    },
    {'field': 'duration', 'headerName': 'Duration'},
    {'field': 'timestamp', 'headerName': 'Timestamp'},
]


def kpi_card(title, value, delta=None, subtitle=None, accent='primary'):
    """Create a KPI card component.

    Args:
        title (str): The title of the KPI.
        value (str): The main value to display.
        delta (str, optional): The change indicator (e.g., "+5%"). Defaults to None.
        subtitle (str, optional): Additional subtitle text. Defaults to None.
        accent (str, optional): Color accent for the delta badge. Defaults to "primary".

    Returns:
        dbc.Card: A Dash Bootstrap Card component representing the KPI.
    """
    trend = (
        html.Span(
            delta,
            className=f'delta badge-{accent}',
        )
        if delta
        else None
    )

    return dbc.Card(
        dbc.CardBody(
            [
                html.Div(title, className='kpi-title'),
                html.H2([value, trend] if trend else value, className='kpi-value'),
                html.Div(subtitle or '', className='kpi-subtitle'),
            ]
        ),
        className='metric-card',
    )


def status_row(label: str, color: str, value: str = '#####') -> html.Div:
    """Create a status row with a colored dot, label, and value.

    Args:
        label (str): The status label.
        color (str): The color for the status dot (e.g., "primary", "success").
        value (str): The value to display next to the label. Defaults to "#####".

    Returns:
        html.Div: A Dash HTML Div component representing the status row.
    """
    dot = html.Span(className=f'status-dot bg-{color}')
    left = html.Span([dot, html.Span(f'  {label}:', className='status-label')], className='status-left')
    right = html.Span(value, className='status-value')
    return html.Div([left, right], className='status-row')


metric_cards = html.Div(
    [
        html.Div(
            [
                kpi_card('Total Scenarios', '1,234', delta='+5%', subtitle='Since last month'),
                kpi_card('Total Agents', '567', delta='-2%', subtitle='Since last week'),
            ],
            className='kpi-row',
        ),
        html.Div(
            [
                kpi_card('Last Simulation Duration', '3h 45m', subtitle='Completed 2 days ago'),
                kpi_card('Floors Detected', '42', delta='+10%', subtitle='Since last scan'),
            ],
            className='kpi-row',
        ),
    ],
    className='metric-cards-container',
)

runs_card = html.Div(
    [
        html.Div(
            [
                html.H3('Recent Simulation Runs', className='runs-card-title'),
                html.Div(
                    [
                        html.Span('Total Runs', className='total-runs-label'),
                        html.Span(id='total-runs-value', children='#####', className='total-runs-value'),
                    ],
                    className='total-runs-row',
                ),
            ]
        ),
        html.Div(
            [
                status_row('CREATED', 'primary', '#####'),
                status_row('RUNNING', 'info', '#####'),
                status_row('SUCCESS', 'success', '#####'),
                status_row('FAILURE', 'danger', '#####'),
            ],
            className='status-breakdown',
        ),
    ],
    className='runs-card',
)

graph_card = dbc.Card(
    dbc.CardBody(
        [
            html.H3('Simulation Duration Over Time', className='graph-card-title'),
            dcc.Graph(
                figure=px.line(
                    x=['2024-01-01', '2024-02-01', '2024-03-01', '2024-04-01'],
                    y=[2, 3, 2.5, 4],
                    labels={'x': 'Date', 'y': 'Duration (hours)'},
                    title='Simulation Duration Over Time',
                ).update_layout(margin=dict(l=20, r=20, t=40, b=20))
            ),
        ],
    ),
    className='graph-card',
)

recent_activity_card = dbc.Card(
    dbc.CardBody(
        [
            dcc.Interval(id='interval-component', interval=5 * 1000, n_intervals=0),
            html.H3('Recent Activity', className='activity-card-title'),
            dag.AgGrid(
                id='recent-activity-grid',
                columnDefs=ColumnDefs,
                rowData=recent_activity_data.to_dict('records'),
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
                className='ag-theme-alpine activity-grid',
                columnSize='sizeToFit',
            ),
        ]
    ),
    className='recent-activity-card',
)


@callback(
    Output('recent-activity-grid', 'rowData'),
    Input('interval-component', 'n_intervals'),
)
def update_recent_activity(_n_intervals):
    """Fetch data from API and return updated row data periodically."""
    # TODO: Replace with actual API call
    updated_data = recent_activity_data.copy()
    updated_data.loc[0, 'timestamp'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return updated_data.to_dict('records')


layout = html.Div(
    [
        html.Div(
            [
                html.H2('Overview', className='overview-title'),
                html.P(
                    'The LocABS dashboard provides real-time insights into localization simulations, '
                    'agent performance metrics, and mapping progress. Monitor active scenarios, '
                    'track simulation runs, and quickly access system controls.',
                    className='overview-description',
                ),
            ],
            className='overview-section',
        ),
        html.Div(
            [
                metric_cards,
                runs_card,
            ],
            className='metric-container',
        ),
        html.Div(
            [
                html.Div(
                    [
                        html.Div(recent_activity_card, className='col-left'),
                        html.Div(graph_card, className='col-right'),
                    ],
                    className='dashboard-row',
                ),
                html.Div(
                    [
                        html.Div(graph_card, className='col-equal'),
                        html.Div(graph_card, className='col-equal'),
                    ],
                    className='dashboard-row-equal',
                ),
            ],
            className='dashboard-rows-container',
        ),
    ]
)
