"""Run Builder Page for LocABS Application."""
from dash import html, dcc, register_page, callback, Output, Input,  ALL
from dash import ctx, callback_context
import dash
import json
import dash_bootstrap_components as dbc
from components.tooltip import create_tooltip
from components.notifications_modal import create_notification_modal
from utilities import api

register_page(__name__, path="/run-builder", name="Run Builder", title="LocABS · Run Builder")

def create_resource_modal(resource_type, title):
    """Create a modal for viewing and managing any resource."""
    return dbc.Modal([
        #dbc.ModalHeader(dbc.ModalTitle(id={"type": "modal-title", "resource": resource_type}, children=title)),
        dbc.ModalBody([
            html.Div(id={"type": "action-modal-summary", "resource": resource_type}, className="resource-summary"),
            html.Details([
                html.Summary("View Full Details"),
                html.Pre(id={"type": "action-modal-details", "resource": resource_type}, className="json-display")
            ], className="details-expandable")
        ]),
        dbc.ModalFooter([
            html.Button("Select", id={"type": "select-btn", "resource": resource_type}, className="btn btn-success btn-sm me-2"),
            html.Button("Edit", id={"type": "edit-btn", "resource": resource_type}, className="btn btn-primary btn-sm me-2"),
            html.Button("Clone", id={"type": "clone-btn", "resource": resource_type}, className="btn btn-info btn-sm me-2"),
            html.Button("Delete", id={"type": "delete-btn", "resource": resource_type}, className="btn btn-danger btn-sm me-2"),
            html.Button("Close", id={"type": "close-btn", "resource": resource_type}, className="btn btn-secondary btn-sm")
        ])
    ], id={"type": "action-modal", "resource": resource_type}, size="lg", is_open=False)

def create_confirmation_modal(modal_id, title, message):
    """Create a confirmation modal for destructive actions."""
    return dbc.Modal([
        dbc.ModalHeader(dbc.ModalTitle(title)),
        dbc.ModalBody(html.P(id=f"{modal_id}-message", children=message)),
        dbc.ModalFooter([
            html.Button("Yes", id=f"{modal_id}-yes-btn", className="btn btn-danger btn-sm me-2"),
            html.Button("No", id=f"{modal_id}-no-btn", className="btn btn-secondary btn-sm")
        ])
    ], id=modal_id, size="sm", is_open=False)

def dropdown(id, options, label):
    """Create a dropdown with Edit, Clone, Delete action buttons."""
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
    ], className="dropdown-with-actions")

def create_generic_form(form_id, title, resource_type):
    """Create a reusable generic form that can be read-only or editable."""
    return html.Div([
        html.Div([
            html.H4(title, className="form-title"),
            html.Div([
                html.Button("Cancel Edit", 
                           id=f"{form_id}-cancel-btn", 
                           className="btn btn-secondary btn-sm",
                           style={"display": "none"})
            ], className="form-actions")
        ], className="form-header"),
        
        # Read-only content display
        html.Div(id=f"{form_id}-readonly-content", className="form-readonly-content"),
        
        # Editable fields (hidden by default)
        html.Div(id=f"{form_id}-editable-fields", 
                className="form-editable-fields",
                style={"display": "none"}),
        
        # Form buttons (hidden by default)
        html.Div([
            html.Button("Save", id=f"{form_id}-save-btn", className="btn btn-primary btn-sm me-2"),
            html.Button("Cancel", id=f"{form_id}-cancel-btn-bottom", className="btn btn-secondary btn-sm")
        ], id=f"{form_id}-button-group", 
           className="form-button-group",
           style={"display": "none"}),
        
        # Hidden stores for form state
        dcc.Store(id=f"{form_id}-mode", data={"mode": "readonly", "resource_id": None}),
        dcc.Store(id=f"{form_id}-original-data")
    ], className="generic-form-container")


layout = html.Div([
    html.Div([
        html.H1("Run Builder", className="page-title"),
        html.P("Create and manage simulation runs", className="page-subtitle"),
    ], className="page-header"),

    # Top Dropdowns for Scenario and Agent Config
    html.Div([
        dropdown(id="scenario", options=[], label="Scenarios"),   
        dropdown(id="agent-config", options=[], label="Agent Configurations"),
    ], className="top-dropdowns"),

    # Action Modals for Scenario and Agent Config
    create_resource_modal("scenario", "Scenario"),
    create_resource_modal("agent_config", "Agent Configuration"),
    dcc.Store(id={"type": "resource-store", "resource": "scenario"}),
    dcc.Store(id={"type": "resource-store", "resource": "agent_config"}),

    # Forms Section
    html.Div([
        html.Div([
            create_generic_form("scenario-form", "Scenario", "Scenario Details")
        ], className="form-column"),
        html.Div([
            create_generic_form("agent-config-form", "Agent Config", "Agent Configuration Details")
        ], className="form-column"),
    ], className="forms-section"),

    # Confirmation Modals 
    dcc.ConfirmDialog(
        id="clone-confirm-dialog",
        message="Would you like to make changes to the cloned version?",
    ),
    dcc.ConfirmDialog(
        id="delete-confirm-dialog",
        message="Are you sure you want to delete this item?",
    ),

    # Notiication Area
    html.Div(id="notification-area", className="notification-area"),

], className="page-container")

# Callbacks

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
        Output({"type": "action-modal", "resource": ALL}, "is_open"),
        Output({"type": "action-modal-summary", "resource": ALL}, "children"),
        Output({"type": "action-modal-details", "resource": ALL}, "children"),
        Output({"type": "resource-store", "resource": ALL}, "data"),
    ],
    [
        Input("scenario-dropdown", "value"),
        Input("agent-config-dropdown", "value"),
    ]
)
def update_modal_content(*selected_ids):
    """Update modal content for any resource type."""
    modals_open = []
    summaries = []
    details = []
    stores = []

    resource_types = ["scenario", "agent_config"]  # Add more types as needed

    # Ensure output lists have the same length as selected_ids
    for idx, resource_id in enumerate(selected_ids):
        resource_type = resource_types[idx] if idx < len(resource_types) else "resource"
        if resource_id:
            success, resource, _ = api.get_by_id(resource_type, resource_id)
            title = resource_type.replace("_", " ").title()
            if success and resource:
                summary = [
                    html.H5(f"{title}: {resource.get('name', '')}"),
                    html.P(f"Description: {resource.get('description', 'N/A')}"),
                    html.P(f"ID: {resource_id}")
                ]
                detail = json.dumps(resource, indent=2)
                modals_open.append(True)
                summaries.append(summary)
                details.append(detail)
                stores.append(resource_id)
            else:
                modals_open.append(False)
                summaries.append(f"No {title} Selected")
                details.append("")
                stores.append(None)
        else:
            modals_open.append(False)
            summaries.append("No Resource Selected")
            details.append("")
            stores.append(None)

    return modals_open, summaries, details, stores
# # Delete the resource upon clicking delete button in the modal
# @callback(
#     [
#         Output("notification-area", "children"),
#         Output("scenario-action-modal", "is_open", allow_duplicate=True),
#         Output("agent-config-action-modal", "is_open", allow_duplicate=True),
#     ],
#     Input({"type": "delete-btn", "resource": ALL}, "n_clicks"),
    
#     # TODO: Change this to dcc.Store later - better implemention - didn't understand at first but figured it out

#     [
#         State("scenario-resource-store", "data"),
#         State("agent-config-resource-store", "data"),
#     ],
#     prevent_initial_call=True
# )
# def delete_any_resource(delete_clicks, scenario_id, agent_config_id):
#     """Universal delete handler for all resource types."""
#     if not delete_clicks :
#         return dash.no_update, dash.no_update, dash.no_update
#     # proceed with deletion
#     if not ctx.triggered_id:
#         return dash.no_update, dash.no_update, dash.no_update

#     # Extract resource type from button ID
#     resource_type = ctx.triggered_id["resource"]
    
#     # Map resource type to ID
#     resource_ids = {
#         "scenario": scenario_id,
#         "agent_config": agent_config_id
#     }
    
#     # Get the resource ID
#     resource_id = resource_ids.get(resource_type)
    
#     if not resource_id:
#         return create_notification_modal("No resource selected.", "error"), False, False
    
#     # Delete the resource
#     success, _, msg = api.delete(resource_type, resource_id)
    
#     # Create notification
#     resource_display_names = {
#         "scenario": "Scenario",
#         "agent_config": "Agent Configuration"
#     }
    
#     display_name = resource_display_names.get(resource_type, "Resource")
    
#     if success:
#         notification = create_notification_modal(f"{display_name} deleted successfully.", "success")
#         # Close the appropriate modal
#         close_scen = (resource_type == "scenario")
#         close_ac = (resource_type == "agent_config")
#         return notification, not close_scen, not close_ac
#     else:
#         notification = create_notification_modal(f"Failed to delete {display_name}: {msg}", "error")
#         return notification, False, False