"""Decision Support Page for LocABS Application."""

from dash import html, register_page, dcc, callback, Input, Output, State
import dash_bootstrap_components as dbc
from utilities import api
import plotly.graph_objects as go

register_page(__name__, path='/decision-support', name='Decision Support', title='LocABS Decision Support')

layout = html.Div(
    [
        # Main Container
        html.Div(
            [
                # Left Sidebar - Run Selection
                html.Div(
                    [
                        html.Div(
                            'SELECT SIMULATION RUN',
                            className='ds-sidebar-header',
                        ),
                        html.Div(
                            [
                                # Run Dropdown
                                html.Div(
                                    [
                                        html.Label('Simulation Run', className='ds-input-label'),
                                        dcc.Dropdown(
                                            id='ds-run-dropdown',
                                            options=[],
                                            placeholder='Select a run...',
                                            className='dropdown-standard',
                                        ),
                                    ],
                                    className='ds-input-group',
                                ),
                                # Run Details
                                html.Div(
                                    [
                                        html.H6('Run Details', className='ds-section-title'),
                                        html.Div(
                                            [
                                                html.Div(
                                                    [
                                                        html.Strong('Name: '),
                                                        html.Span(id='ds-run-name', children='N/A'),
                                                    ],
                                                    className='ds-detail-row',
                                                ),
                                                html.Div(
                                                    [
                                                        html.Strong('Scenario: '),
                                                        html.Span(id='ds-run-scenario', children='N/A'),
                                                    ],
                                                    className='ds-detail-row',
                                                ),
                                                html.Div(
                                                    [
                                                        html.Strong('Agent Config: '),
                                                        html.Span(id='ds-run-agent', children='N/A'),
                                                    ],
                                                    className='ds-detail-row',
                                                ),
                                                html.Div(
                                                    [
                                                        html.Strong('Number of Runs: '),
                                                        html.Span(id='ds-run-count', children='N/A'),
                                                    ],
                                                    className='ds-detail-row',
                                                ),
                                            ],
                                            className='ds-details-container',
                                        ),
                                    ],
                                    className='ds-details-section',
                                ),
                                # Action Buttons
                                html.Div(
                                    [
                                        html.Button(
                                            [html.I(className='fa fa-play me-2'), 'Analyze Run'],
                                            id='ds-analyze-btn',
                                            className='btn btn-primary ds-btn',
                                        ),
                                    ],
                                    className='ds-button-group',
                                ),
                            ],
                            className='ds-sidebar-content',
                        ),
                    ],
                    className='ds-sidebar',
                ),
                # Center - Main Visualization Area
                html.Div(
                    [
                        html.Div(
                            [
                                html.Div(
                                    'BAYESIAN NETWORK VISUALIZATION',
                                    className='ds-section-header',
                                ),
                                html.Div(
                                    [
                                        dcc.Graph(
                                            id='ds-network-graph',
                                            config={'displayModeBar': False},
                                            className='ds-network-graph',
                                        ),
                                    ],
                                    className='ds-visualization-area',
                                ),
                                html.Div(
                                    [
                                        html.Button(
                                            [html.I(className='fa fa-folder-open me-2'), 'QUICK ACCESS TO ITEM SNIPS'],
                                            id='ds-quick-access-btn',
                                            className='btn btn-outline-light ds-action-btn',
                                        ),
                                        html.Button(
                                            [html.I(className='fa fa-chart-bar me-2'), 'SELECT OTHER'],
                                            id='ds-select-other-btn',
                                            className='btn btn-outline-light ds-action-btn',
                                        ),
                                    ],
                                    className='ds-action-bar',
                                ),
                            ],
                            className='ds-main-section',
                        ),
                    ],
                    className='ds-center',
                ),
                # Right Sidebar - Results Area
                html.Div(
                    [
                        html.Div(
                            'RESULTS AREA',
                            className='ds-sidebar-header',
                        ),
                        html.Div(
                            [
                                html.Div(
                                    [
                                        html.Div(id='ds-result-panel-1', className='ds-result-panel'),
                                    ],
                                    className='ds-result-section',
                                ),
                                html.Div(
                                    [
                                        html.Div(id='ds-result-panel-2', className='ds-result-panel'),
                                    ],
                                    className='ds-result-section',
                                ),
                            ],
                            className='ds-sidebar-content',
                        ),
                    ],
                    className='ds-sidebar ds-right-sidebar',
                ),
            ],
            className='ds-top-section',
        ),
        # Bottom Section - Inference Areas
        html.Div(
            [
                html.Div(
                    [
                        html.Div(
                            'FORWARD INFERENCE',
                            className='ds-inference-header',
                        ),
                        html.Div(
                            id='ds-forward-inference-content',
                            className='ds-inference-content',
                        ),
                    ],
                    className='ds-inference-section',
                ),
                html.Div(
                    [
                        html.Div(
                            'BACKWARD INFERENCE',
                            className='ds-inference-header',
                        ),
                        html.Div(
                            id='ds-backward-inference-content',
                            className='ds-inference-content',
                        ),
                    ],
                    className='ds-inference-section',
                ),
            ],
            className='ds-bottom-section',
        ),
    ],
    className='ds-page-container',
)


# Callbacks
@callback(
    Output('ds-run-dropdown', 'options'),
    Input('ds-run-dropdown', 'id'),
)
def load_runs(_):
    """Load all runs from the backend."""
    success, runs, _ = api.get_all('run')
    if not success or not runs:
        return []

    options = [{'label': f'{run.get("name", "Run")} (ID: {run.get("id")})', 'value': run.get('id')} for run in runs]
    return options


@callback(
    [
        Output('ds-run-name', 'children'),
        Output('ds-run-scenario', 'children'),
        Output('ds-run-agent', 'children'),
        Output('ds-run-count', 'children'),
    ],
    Input('ds-run-dropdown', 'value'),
    prevent_initial_call=True,
)
def update_run_details(run_id):
    """Update run details when a run is selected."""
    if not run_id:
        return 'N/A', 'N/A', 'N/A', 'N/A'

    success, run_data, _ = api.get_by_id('run', run_id)
    if not success or not run_data:
        return 'N/A', 'N/A', 'N/A', 'N/A'

    name = run_data.get('name', 'N/A')
    scenario = run_data.get('scenario', {}).get('name', 'N/A') if isinstance(run_data.get('scenario'), dict) else 'N/A'
    agent = run_data.get('agents', {}).get('name', 'N/A') if isinstance(run_data.get('agents'), dict) else 'N/A'
    runs = run_data.get('runs', 'N/A')

    return name, scenario, agent, runs


@callback(
    Output('ds-network-graph', 'figure'),
    Input('ds-analyze-btn', 'n_clicks'),
    State('ds-run-dropdown', 'value'),
    prevent_initial_call=True,
)
def update_network_visualization(_n_clicks, _run_id):
    """Update the Bayesian network visualization."""
    # Placeholder network visualization
    fig = go.Figure()

    # Add some sample nodes
    fig.add_trace(
        go.Scatter(
            x=[1, 2, 3, 2, 2],
            y=[1, 2, 1, 1.5, 0.5],
            mode='markers+text',
            marker=dict(size=50, color='#3b82f6'),
            text=['Node 1', 'Node 2', 'Node 3', 'Node 4', 'Node 5'],
            textposition='middle center',
            textfont=dict(color='white', size=10),
        )
    )

    fig.update_layout(
        showlegend=False,
        plot_bgcolor='#1a1a1a',
        paper_bgcolor='#1a1a1a',
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        margin=dict(l=0, r=0, t=0, b=0),
        height=400,
    )

    return fig
