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
        className="metric-card",
        style={
            "backgroundColor": "#ffffff", 
            "minWidth": "300px", 
            "padding": "15px", 
            "margin": "10px", 
            "borderRadius": "10px", 
            "boxShadow": "0 2px 4px rgba(0, 0, 0, 0.1)"},
)

def status_row(label: str, color: str, value: str = "#####") -> html.Div:
    """Create a status row with a colored dot, label, and value."""
    dot = html.Span(
        className=f"status-dot bg-{color}",
        style={"width": "20px", "height": "20px", "borderRadius": "50%", "display": "inline-block"},
    )
    left = html.Span([dot, html.Span(f"  {label}:", className="ms-4")], className="d-flex align-items-center")
    right = html.Span(value, className="fw-semibold")
    return html.Div([left, right], className="d-flex justify-content-between align-items-center mb-4")

metric_cards = html.Div(
    [
        html.Div(
            [
                kpi_card("Total Scenarios", "1,234", delta="+5%", subtitle="Since last month"),
                kpi_card("Total Agents", "567", delta="-2%", subtitle="Since last week"),
            ],
            className="container-row",
            style={"display": "flex", "flexDirection": "row", "gap": "20px", "margin": "10px"},
        ),
        html.Div(
            [
                kpi_card("Last Simulation Duration", "3h 45m", subtitle="Completed 2 days ago"),
                kpi_card("Floors Detected", "42", delta="+10%", subtitle="Since last scan"),
            ],
            className="container-row",
            style={"display": "flex", "flexDirection": "row", "gap": "20px", "margin": "10px"},
        ),
    ],
    className="metric-cards-container",
    style={"alignItems": "center", "width": "50vw", "display": "flex", "flexDirection": "column"},
)

runs_card = html.Div(
    [
        # Header section with title and total count
        html.Div(
            [
                html.H3("Recent Simulation Runs", style={
                    "fontSize": "1.25rem",
                    "fontWeight": "600",
                    "marginBottom": "16px",
                    "color": "#1f2937"
                }),
                html.Div(
                    [
                        html.Span("Total Runs", style={
                            "color": "#6b7280",
                            "fontSize": "0.875rem",
                            "fontWeight": "500"
                        }),
                        html.Span(id="total-runs-value", children="#####", style={
                            "fontSize": "1.5rem",
                            "fontWeight": "600",
                            "color": "#111827"
                        }),
                    ],
                    style={
                        "display": "flex",
                        "justifyContent": "space-between",
                        "alignItems": "center",
                        "padding": "12px 0",
                        "borderBottom": "1px solid #e5e7eb",
                        "marginBottom": "16px"
                    }
                ),
            ]
        ),
        # Status breakdown section
        html.Div(
            [
                status_row("CREATED", "primary", "#####"),
                status_row("RUNNING", "info", "#####"),
                status_row("SUCCESS", "success", "#####"),
                status_row("FAILURE", "danger", "#####"),
            ],
            style={
                "display": "flex",
                "flexDirection": "column",
                "gap": "8px"
            }
        ),
    ],
    style={
        "backgroundColor": "#ffffff",
        "padding": "20px",
        "borderRadius": "8px",
        "boxShadow": "0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06)",
        "minWidth": "280px",
        "width": "100%",
    }
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
    className="graph-card",
    style={
        "backgroundColor": "#ffffff",
        "padding": "10px",
        "borderRadius": "8px",
        "boxShadow": "0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06)",
        "width": "100%"
    }
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
                style={"height": "47vh", "width": "100%"},
            )
        ]
    ),
    className="shadow-sm bg-white rounded",
    style={"maxWidth": "600px", "margin": "0", "padding": "12px"},
)

# TODO: Add functionality to buttons
# TODO: Style buttons to be centered in card 


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



layout = html.Div([

    # Overview section
    html.Div([
        html.H2("Overview", className="overview-title"),
        html.P(
            "The LocABS dashboard provides real-time insights into localization simulations, "
            "agent performance metrics, and mapping progress. Monitor active scenarios, "
            "track simulation runs, and quickly access system controls.",
            className="overview-description"
        ),
    ], className="overview-section"),

    html.Div([
        metric_cards,
        runs_card,
    ],   
    className="metric-container d-flex flex-row justify-content-between align-items-center gap-4"
    ),

   # Two-row layout: top has activity/graph side by side, bottom has actions/graph side by side
    html.Div([
        # Row 1: Recent Activity + Graph
        html.Div([
            html.Div(recent_activity_card, style={"flex": "1", "maxWidth": "600px"}),
            html.Div(graph_card, style={"flex": "1", "minWidth": "0"}),
        ], style={
            "display": "flex",
            "flexDirection": "row",
            "gap": "16px",
            "margin": "16px",
            "alignItems": "flex-start"
        }),
        
        # Row 2: Quick Actions + Second Graph
        html.Div([
            html.Div(graph_card, style={"flex": "1", "maxWidth": "50%"}),
            html.Div(graph_card, style={"flex": "1", "maxWidth": "50%"}),  # replace with different graph
        ], style={
            "display": "flex",
            "flexDirection": "row",
            "gap": "16px",
            "margin": "16px",
            "alignItems": "stretch"
        }),
    ], style={
        "marginTop": "20px",
        "display": "flex",
        "flexDirection": "column",
        "gap": "16px"
    }),
],   

)


# "backgroundColor": "#f5f5f5",
#         "minHeight": "calc(100vh - 200px)",
#         "paddingBottom": "100px",