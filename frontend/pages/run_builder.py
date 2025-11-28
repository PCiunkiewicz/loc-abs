"""Run Builder Page for LocABS Application."""
from dash import html, dcc, register_page, callback, Output, Input,  ALL
import json
import dash_bootstrap_components as dbc
from components.tooltip import create_tooltip
#from components.notifications_modal import create_notification_modal
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
            id={"type": "dropdown", "resource": f"{id}"},
            options=[{"label": opt["name"], "value": opt["id"]} for opt in options],
            placeholder=f"Select a {label}",
            className="dropdown-standard"
        ),
    ], className="dropdown-with-actions")

def create_generic_form(form_id, title, resource_type):
    """Create a reusable generic form that can be read-only or editable."""
    return html.Div([
        html.Div([
            html.Label(title, className="form-title"),
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

def create_scenario_form(resource_type):
    """Create a reusable scenario form that can be read-only or editable."""
    return html.Div([
        html.Div([
            html.Label("Scenario", className="form-label"),
            html.Div([
                html.Button("Cancel Edit", 
                           id=f"{resource_type}-cancel-btn", 
                           className="btn btn-secondary btn-sm",
                           style={"display": "none"})
            ], className="form-actions")
        ], className="form-header"),

        html.Div([
            dropdown(id="virus", options=[], label="Virus"),
            dropdown(id="prevention", options=[], label="Prevention"),
            dropdown(id="simulation", options=[], label="Simulation")

        ], className="scenario-form-dropdowns-container"),
        create_resource_modal("virus", "Virus"),
        create_resource_modal("prevention", "Prevention"),
        create_resource_modal("simulation", "Simulation"),

        create_generic_form("virus", "Virus", "Virus"),
        create_generic_form("prevention", "Prevention", "Prevention"),
        create_generic_form("simulation", "Simulation", "Simulation"),

        dcc.Store(id={"type": "resource-store", "resource": "virus"}),
        dcc.Store(id={"type": "resource-store", "resource": "prevention"}),
        dcc.Store(id={"type": "resource-store", "resource": "simulation"}),
        
        # Form buttons (hidden by default)
        html.Div([
            html.Button("Save", id=f"{resource_type}-save-btn", className="btn btn-primary btn-sm me-2"),
            html.Button("Cancel", id=f"{resource_type}-cancel-btn-bottom", className="btn btn-secondary btn-sm")
        ], id=f"{resource_type}-button-group", 
           className="form-button-group",
           style={"display": "none"}),
        
        # Hidden stores for form state
        dcc.Store(id=f"{resource_type}-mode", data={"mode": "readonly", "resource_id": None}),
        dcc.Store(id=f"{resource_type}-original-data")
    ], className="scenario-form-container")


layout = html.Div([
    html.Div([
        html.H1("Run Builder", className="page-title"),
        html.P("Create and manage simulation runs", className="page-subtitle"),
    ], className="page-header"),

    # Top Dropdowns for Scenario and Agent Config
    html.Div([
        dropdown(id="scenario", options=[], label="Scenario"),   
        dropdown(id="agent_config", options=[], label="Agent Configuration"),
    ], className="top-dropdowns"),

    # Action Modals for Scenario and Agent Config
    create_resource_modal("scenario", "Scenario"),
    create_resource_modal("agent_config", "Agent Configuration"),
    dcc.Store(id={"type": "resource-store", "resource": "scenario"}),
    dcc.Store(id={"type": "resource-store", "resource": "agent_config"}),

    # Forms Section
    html.Div([
        html.Div([
            create_scenario_form("scenario")
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
        Output({"type": "dropdown", "resource": ALL}, "options"),
    ],
    [
        Input({"type": "dropdown", "resource": ALL}, "id"),
    ]
)
def populate_dropdown_options(dropdown_ids):
    """Populate dropdown options from API for any resource type."""
    options_list = []
    for dropdown_id in dropdown_ids:
        resource_type = dropdown_id["resource"]
        success, resources, _ = api.get_all(resource_type)
        if success and resources:
            options = [{"label": r["name"], "value": r["id"]} for r in resources]
        else:
            options = []
        options_list.append(options)
    return [options_list]

# TODO: Edit details to be more UI friendly
@callback(
    [
        Output({"type": "action-modal", "resource": ALL}, "is_open"),
        Output({"type": "action-modal-summary", "resource": ALL}, "children"),
        Output({"type": "action-modal-details", "resource": ALL}, "children"),
        Output({"type": "resource-store", "resource": ALL}, "data"),
    ],
    [
        Input({"type": "dropdown", "resource": ALL}, "value"),
    ]
)
def update_modal_content(selected_ids):
    """Update modal content for any resource type."""
    modals_open = []
    summaries = []
    details = []
    stores = []

    resource_types = ["scenario", "agent_config", "virus", "prevention", "simulation"]  # Add more types as needed

    # Ensure output lists have the same length as selected_ids
    for idx, resource_id in enumerate(selected_ids):
        resource_type = resource_types[idx] if idx < len(resource_types) else "resource"
        if resource_id:
            success, resource, _ = api.get_by_id(resource_type, resource_id)
            title = resource_type.replace("_", " ").title()
            if success and resource:
                desc = []
                for k, v in resource.items():
                    key_str = str(k).replace('_', ' ').title()
                    if isinstance(v, dict):
                        dict_items = []
                        for dk, dv in v.items():
                            dict_key = str(dk).replace('_', ' ').title()
                            dict_items.append(html.Li(f"{dict_key}: {dv}"))
                        value_str = html.Ul(dict_items, style={"marginLeft": "1em"})
                    else:
                        value_str = str(v)
                    desc.append(html.P([f"{key_str}: ", value_str]))
                summary = [
                    html.H5(f"{title}: {resource.get('name', '')}"),
                    html.Div(desc),                 
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