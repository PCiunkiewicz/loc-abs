"""Dashboard Page for LocABS Application."""
from dash import html, dcc, register_page
import dash_bootstrap_components as dbc
import plotly.express as px

register_page(__name__, path="/", name="Dashboard", title="LocABS · Dashboard")


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

def status_row(label: str, color: str, value: str = "#####") -> html.Div:
    """Create a status row with a colored dot, label, and value."""
    dot = html.Span(
        className=f"bg-{color}",
        style={"width": "20px", "height": "20px", "borderRadius": "50%", "display": "inline-block"},
    )
    left = html.Span([dot, html.Span(f"  {label}:", className="ms-4")], className="d-flex align-items-center")
    right = html.Span(value, className="fw-semibold")
    return html.Div([left, right], className="d-flex justify-content-between align-items-center mb-4")

runs_card = dbc.Card(
    dbc.CardBody(
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
        ]
    ), 
    className="graph-card shadow-sm bg-white rounded w-50",
)

recent_activity_card = dbc.Card(
    dbc.CardBody(
        [
            html.H3("Recent Activity", className="card-title mb-3"),
            dbc.Table(
                [
                    html.Thead(
                        html.Tr(
                            [
                                html.Th("Scenario"),
                                html.Th("Run ID"),
                                html.Th("Status"),
                                html.Th("Duration"),
                                html.Th("Timestamp"),
                            ], 
                        )
                    ),
                    html.Tbody(
                        [
                            html.Tr([html.Td("Baseline A"), html.Td("#1842"), html.Td("Success"), html.Td("03:12"), html.Td("2025-10-28 09:14")]),
                            html.Tr([html.Td("Baseline B"), html.Td("#1841"), html.Td("Failed"), html.Td("00:47"), html.Td("2025-10-28 08:50")]),
                            html.Tr([html.Td("What-if C"),  html.Td("#1840"), html.Td("Success"), html.Td("04:05"), html.Td("2025-10-28 08:20")]),
                        ]
                    ),
                ],
                bordered=False,
                hover=True,
                responsive=True,
                striped=True,
                className="mb-0",
            ),
        ]
    ),
    className="shadow-sm bg-white rounded",
    style={"maxWidth": "600px", "margin": "0", "padding": "12px"},
)


layout = dbc.Container([
    dbc.Container([
        metric_cards,
        runs_card,
    ],   
    fluid=True,
    className="metric-container d-flex flex-row justify-content-between align-items-center gap-4"
    ),

    dbc.Container([
        recent_activity_card,
        graph_card,
    ],
    fluid=True,
    className="d-flex flex-row justify-content-evenly align-items-center gap-4 mt-4"
    ),
],   
fluid=True,
)
