"""Run Builder Page for LocABS Application."""
from dash import html, dcc, register_page, callback, Output, Input, State, ALL
from dash import ctx
import dash
import json
import dash_bootstrap_components as dbc
from components.tooltip import create_tooltip
from components.notifications_modal import create_notification_modal
from utilities import api


register_page(__name__, path="/run-builder", name="Run Builder", title="LocABS · Run Builder")


def modal_action_buttons(resource_type):
    """Return Edit, Clone, Delete buttons for a modal."""
    return html.Div([
        html.Button("Select", id={"type": "select-btn", "resource": resource_type}, n_clicks=0, className="btn-success btn-sm"),
        html.Button("Edit", id={"type": "edit-btn", "resource": resource_type}, n_clicks=0, className="btn-primary btn-sm"),
        html.Button("Clone", id={"type": "clone-btn", "resource": resource_type}, n_clicks=0, className="btn-primary btn-sm"),
        html.Button("Delete", id={"type": "delete-btn", "resource": resource_type}, n_clicks=0, className="btn-danger btn-sm"),
    ], className="dropdown-item-actions")

def dropdown(id, options, label):
    """Dropdown with Edit, Clone, Delete buttons for each item."""
    return html.Div([
        html.Div([
                html.Label(label, className="dropdown-label"),
                html.Img(src="/static/tooltip.png", id=f"{id}-tooltip")
            ], className="tooltip-container"),
        create_tooltip(f"Select a {label} from the dropdown. Click the buttons to edit, clone, or delete the selected {label.lower()}.", f"{id}-tooltip"),
        dcc.Dropdown(
            id=f"{id}-dropdown",
            options=[{"label": opt["name"], "value": opt["id"]} for opt in options],
            placeholder=f"Select {label}",
            className="dropdown-standard"
        ),
        dbc.Modal(
            id=f"{id}-action-modal",
            is_open=False,
            children=[
                html.Div(id=f"{id}-modal-content")
            ],
            className="action-modal"
        )   
    ], className="dropdown-with-actions")

def tab_content(title, content, editable=False):
    """Tab content, editable if in edit/clone mode."""
    if editable:
        return html.Div([
            html.H5(f"Edit {title}"),
            html.Form(content),
            html.Button("Save", id=f"save-{title.lower()}-btn", className="btn-primary")
        ])
    else:
        return html.Div([
            html.H5(f"{title} Summary"),
            html.Div(content)
        ])


layout = html.Div([
    html.Div([
        dropdown(id="scenario", options=[], label="Scenarios"),   
        dropdown(id="agent-config", options=[], label="Agent Configurations"),
    ], className="top-dropdowns"),
    dcc.Store(id="scenario-resource-store"),
    dcc.Store(id="agent-config-resource-store"),

    dcc.Tabs(id="main-tabs", value="scenario", children=[
        dcc.Tab(label="Scenario", value="scenario", children=[
            html.Div(id="scenario-tab-content")
        ]),
        dcc.Tab(label="Agent Config", value="agent-config", children=[
            html.Div(id="agent-config-tab-content")
        ]),
    ]),
    dcc.ConfirmDialog(id="clone-confirm-modal"),
    html.Div(id="notification-area")
], className="page-container")


@callback(
    [
        Output("scenario-dropdown", "options"),
        Output("agent-config-dropdown", "options"),

    ],
    [
        Input("scenario-dropdown", "id"),
        Input("agent-config-dropdown", "id"),
    ]
)

def populate_dropdown_options(_, __):
    """Populate dropdown options from API - Scenarios and Agent Configs."""
    success_scen, scenarios, _ = api.get_all('scenario')
    success_agent, agent_configs, _ = api.get_all('agent_config')

    scenario_options = []
    agent_config_options = []

    if success_scen and scenarios:
        scenario_options = [{"label": sc["name"], "value": sc["id"]} for sc in scenarios]

    if success_agent and agent_configs:
        agent_config_options = [{"label": ac["name"], "value": ac["id"]} for ac in agent_configs]

    return scenario_options, agent_config_options

# TODO: Edit details to be more UI friendly
@callback(
    [
        Output("scenario-action-modal", "is_open"),
        Output("scenario-modal-content", "children"),
        Output("scenario-resource-store", "data"),
        Output("agent-config-action-modal", "is_open"), 
        Output("agent-config-modal-content", "children"),
        Output("agent-config-resource-store", "data"),
    ],
    [
        Input("scenario-dropdown", "value"),
        Input("agent-config-dropdown", "value"),
    ],
    [
        State("scenario-action-modal", "is_open"),
        State("agent-config-action-modal", "is_open"),
    ]
)
def display_action_modals(scenario_id, agent_config_id, scen_modal_open, ac_modal_open):
    """Display action modals for Scenario and Agent Config dropdowns."""
    scen_modal_content = html.Div("No Scenario Selected")
    ac_modal_content = html.Div("No Agent Configuration Selected")

    if scenario_id:
        success, scenario, _ = api.get_by_id('scenario', scenario_id)
        if success and scenario:
            scen_modal_content = html.Div([
                html.H5(f"Scenario: {scenario['name']}"),
                html.H5(f"ID:{scenario_id}", id ="scenario-id"),
                html.Details([
                    html.Summary("View Details"),
                    html.Pre(json.dumps(scenario, indent=2)),
                ]),
                modal_action_buttons("scenario")
            ])
    if agent_config_id:
        success, agent_config, _ = api.get_by_id('agent_config', agent_config_id)
        if success and agent_config:
            ac_modal_content = html.Div([
                html.H5(f"Agent Configuration: {agent_config['name']}"),
                html.H5(f"ID:{agent_config_id}"),             
                html.Details([
                    html.Summary("View Details"),
                    html.Pre(json.dumps(agent_config, indent=2)),
                ]),
                html.Div([

                ]),
                # Additional agent config details can be added here
                modal_action_buttons("agent_config")
            ])

    return (
        True if scenario_id else False, 
        scen_modal_content, 
        scenario_id,
        True if agent_config_id else False, 
        ac_modal_content,
        agent_config_id
    )
