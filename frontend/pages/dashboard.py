"""Dashboard Page for LocABS Application."""
from dash import html, dcc, register_page, callback, Output, Input
import dash_bootstrap_components as dbc
import dash_ag_grid as dag
import plotly.express as px
import pandas as pd
from datetime import datetime


register_page(__name__, path="/", name="Dashboard", title="LocABS · Dashboard")


# Sample data for recent activity table
# TODO: Replace with actual data fetching logic or database queries later
recent_activity_data = pd.DataFrame([
    {"scenario": "Baseline A", "run_id": "#1842", "status": "Success", "duration": "03:12", "timestamp": "2025-10-28 09:14"},
    {"scenario": "Baseline B", "run_id": "#1841", "status": "Failed", "duration": "00:47", "timestamp": "2025-10-28 08:50"},
    {"scenario": "What-if C", "run_id": "#1840", "status": "Success", "duration": "04:05", "timestamp": "2025-10-28 08:20"},
]
)

ColumnDefs = [
    {"field": "scenario", "headerName": "Scenario"},
    {"field": "run_id", "headerName": "Run ID"},
    {
        "field": "status", 
        "headerName": "Status", 
         "cellStyle": {
            "styleConditions": [
                {"condition": "params.value == 'Success'", "style": {"color": "#28a745", "fontWeight": "600"}},
                {"condition": "params.value == 'Failed'", "style": {"color": "#dc3545", "fontWeight": "600"}},
                {"condition": "params.value == 'Running'", "style": {"color": "#17a2b8", "fontWeight": "600"}},
            ]
        } 
    },
    {"field": "duration", "headerName": "Duration"},
    {"field": "timestamp", "headerName": "Timestamp"},
]

def kpi_card(title, value, delta=None, subtitle=None, accent="primary"):
    """Create a KPI card component."""
    trend = html.Span(
        delta,
        className=f"delta ms-2 badge bg-{accent}",
        style={"fontSize": "0.75rem"},
    ) if delta else None

    return dbc.Card(
        dbc.CardBody(
            [
                html.Div(title, className="title text-muted medium "),
                html.H2([value, trend] if trend else value, className="value mb-0"),
                html.Div(subtitle or "", className="subtitle text-muted medium mt-1",),
            ]
        ),
        className="metric-card shadow-sm h-100 w-100 p-3 rounded",
        style={"backgroundColor": "#F0F2F6", },
)

def status_row(label: str, color: str, value: str = "#####") -> html.Div:
    """Create a status row with a colored dot, label, and value."""
    dot = html.Span(
        className=f"bg-{color}",
        style={"width": "20px", "height": "20px", "borderRadius": "50%", "display": "inline-block"},
    )
    left = html.Span([dot, html.Span(f"  {label}:", className="ms-4")], className="d-flex align-items-center")
    right = html.Span(value, className="fw-semibold")
    return html.Div([left, right], className="d-flex justify-content-between align-items-center mb-4")

metric_cards = dbc.Container([
        dbc.Row(
        [
            dbc.Col(kpi_card("Total Scenarios", "1,234", delta="+5%", subtitle="Since last month"), md=6),
            dbc.Col(kpi_card("Total Agents", "567", delta="-2%", subtitle="Since last week"), md=6),
        ], 
        justify="evenly",
        className="row mb-4 w-100"),
        dbc.Row(
        [
            dbc.Col(kpi_card("Last Simulation Duration", "3h 45m", subtitle="Completed 2 days ago"), md=6),
            dbc.Col(kpi_card("Floors Detected", "42", delta="+10%", subtitle="Since last scan"), md=6),
        ], 
        justify="evenly",
        className="row mb-4 w-100"
        )
    ],
    style={ "align-items": "center", "width": "50vw"},)

runs_card = dbc.Card(
    dbc.CardBody(
        [
            dbc.Row(
            [
                # Left column: title + total runs
                dbc.Row(
                    [
                        html.H3("Recent Simulation Runs", className="card-title mb-2"),
                        dbc.Row([
                            dbc.Col("Total Runs", className="text-muted medium"),
                            dbc.Col( html.H3("#####", className="mb-3")),
                        ], className="m-3 justify-content-between w-100" ),
                    ],
                ),
                # Right column: status breakdown
                dbc.Row(
                    [
                        status_row("CREATED", "dark", "#####"),
                        status_row("RUNNING", "info", "#####"),
                        status_row("SUCCESS", "success", "#####"),
                        status_row("FAILURE", "danger", "#####"),
                    ],
                ),
            ],
            className="g-2 align-items-center",
            )
        ]
    ),
    className="runs-card shadow-sm bg-white rounded",
    
)

graph_card = dbc.Card(
    dbc.CardBody(
        [
            html.H3("Simulation Duration Over Time", className="card-title mb-4"),
            dcc.Graph(
                # TODO: Replace with actual graph
                figure=px.line(
                    x=["2024-01-01", "2024-02-01", "2024-03-01", "2024-04-01"],
                    y=[2, 3, 2.5, 4],
                    labels={"x": "Date", "y": "Duration (hours)"},
                    title="Simulation Duration Over Time",
                ).update_layout(margin=dict(l=20, r=20, t=40, b=20))
            ),
        ],
    ), 
    className="graph-card shadow-sm bg-white rounded w-100",
)

recent_activity_card = dbc.Card(
    dbc.CardBody(
        [   
            dcc.Interval(id="interval-component", interval=5*1000, n_intervals=0),
            html.H3("Recent Activity", className="card-title mb-4"),
            dag.AgGrid(
                id= "recent-activity-grid",
                columnDefs=ColumnDefs,
                rowData=recent_activity_data.to_dict('records'),
                defaultColDef={
                    "resizable": True,
                    "sortable": True,
                    "filter": True,
                },
                dashGridOptions={
                    "pagination": True,
                    "paginationPageSize": 10,
                    "animateRows": True,
                },
                className="ag-theme-alpine",
                columnSize="sizeToFit",
                style={"height": "420px", "width": "100%"},
            )
        ]
    ),
    className="shadow-sm bg-white rounded",
    style={"maxWidth": "600px", "margin": "0", "padding": "12px"},
)

actions_card = dbc.Card(
    dbc.CardBody(
        [
            html.H3("Quick Actions", className="card-title mb-4"),
            dbc.Button("Create New Scenario", color="primary", className="mb-4 w-75"),
            dbc.Button("Open Data Visualisation", color="primary", className="mb-4 w-75"),
            dbc.Button("Manage Agents", color="primary", className="mb-4 w-75"),
            dbc.Button("Stop Simulation", color="primary", className="mb-4 w-75"),  
        ]
    ),
    className="shadow-sm bg-white rounded",
    style={
        "padding": "12px",
        "maxWidth": "600px",
        "height": "500px",
        "display": "flex",
        "flexDirection": "column",
        "alignItems": "center",
        "justifyContent": "center"},
)

@callback(
    Output("recent-activity-grid", "rowData"),
    Input("interval-component", "n_intervals"),
)

def update_recent_activity(n_intervals):
    """Fetch data from API and return updated row data periodically."""
    # TODO: Replace with actual API call
    # recent_activity_data = pd.DataFrame(response.json())
    # where response is return value from API call

    updated_data = recent_activity_data.copy()
    updated_data.loc[0, "timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return updated_data.to_dict('records')



layout = dbc.Container([

    dbc.Container([
        metric_cards,
        runs_card,
    ],   
    fluid=True,
    className="metric-container d-flex flex-row justify-content-between align-items-center gap-4"
    ),

   # Two-column layout: left has activity/actions stacked, right has graphs stacked
    html.Div([
        # Left column
        html.Div([
            recent_activity_card,
            html.Div(style={"height": "70px"}),  # spacer
            actions_card,
        ], style={"flex": "1", "maxWidth": "33vw"}),
        
        # Right column
        html.Div([
            graph_card,
            html.Div(style={"height": "30px"}),  # spacer
            graph_card,  # replace with a different graph if needed
        ], style={"flex": "1", "minWidth": "0"}),
    ], style={
        "display": "flex",
        "flexDirection": "row",
        "gap": "10px",
        "marginTop": "20px",
        "justifyContent": "space-evenly",
        "alignItems": "flex-start"
    }),
],   
fluid=True,
)
