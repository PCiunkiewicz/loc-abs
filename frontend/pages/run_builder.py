"""Run Builder Page for LocABS Application."""
from dash import html, dcc, register_page, callback, Output, Input, State, ctx,  ALL, no_update 
import json
import dash_bootstrap_components as dbc
from components.tooltip import create_tooltip
from components.resource_form import render_resource_form
from components.input_components import create_mask_input, create_vaccine_type
#from components.notifications_modal import create_notification_modal
from utilities import api

register_page(__name__, path="/run-builder", name="Run Builder", title="LocABS · Run Builder")

# TODO: Ensure that when an item is chosen it doesn't show

virus_fields = [
    {"id": "virus-name", "label": "Name", "type": "text", "className": "form-input"},
    {"id": "virus-attack-rate", "label": "Attack Rate", "type": "number", "min": 0, "max": 1, "step": 0.001, "className": "form-input"},
    {"id": "virus-infection-rate", "label": "Infection Rate", "type": "number", "min": 0, "max": 1, "step": 0.001, "className": "form-input"},
    {"id": "virus-fatality-rate", "label": "Fatality Rate", "type": "number", "min": 0, "max": 1, "step": 0.001, "className": "form-input"},
]

simulation_fields = [
    {"id": "simulation-name", "label": "Name", "type": "text", "className": "form-input"},
    {"id": "map-file-dropdown", "label": "Map File", "type": "dropdown", "options": [], "className": "dropdown-standard"},
    {"id": "xy-scale-input", "label": "XY Scale", "type": "number", "min": 1.0, "max": 1000000.0, "step": 0.01, "className": "form-input"},
    {"id": "time-step-input", "label": "Time Step (s)", "type": "dropdown", "options": [
                                                                                        {"label": "1 second", "value": 1},
                                                                                        {"label": "5 seconds", "value": 5},
                                                                                        {"label": "10 seconds", "value": 10},
                                                                                        {"label": "30 seconds", "value": 30},
                                                                                        {"label": "1 minute (60s)", "value": 60},
                                                                                        {"label": "5 minutes (300s)", "value": 300},
                                                                                        {"label": "10 minutes (600s)", "value": 600},
                                                                                        {"label": "30 minutes (1800s)", "value": 1800},
                                                                                        {"label": "1 hour (3600s)", "value": 3600}, ], "className": "dropdown-standard"},
    {"id": "save-resolution-input", "label": "Save Resolution", "type": "number", "min": 1, "max": 2147483647, "step": 1, "className": "form-input"},
    {"id": "max-iterations-input", "label": "Max Iterations", "type": "number", "min": 1, "max": 2147483647, "step": 1, "className": "form-input"},
    {"id": "terrain-dropdown", "label": "Terrain", "type": "dropdown", "options": [], "className": "dropdown-standard", "multi": True},
]

prevention_fields = [
    {"id": "prevention-name", "label": "Name", "type": "text", "className": "form-input"},
    {"id": "mask-n95", "component": lambda readonly, value: create_mask_input("N95", "N95", default_value=value or 0.85, is_checked=not readonly, is_disabled=readonly)},
    {"id": "mask-home", "component": lambda readonly, value: create_mask_input("HOME", "Home/Cloth", default_value=value or 0.0, is_checked=not readonly, is_disabled=readonly)},
    {"id": "mask-cloth", "component": lambda readonly, value: create_mask_input("CLOTH", "Cloth", default_value=value or 0.83, is_checked=not readonly, is_disabled=readonly)},
    {"id": "mask-surgical", "component": lambda readonly, value: create_mask_input("SURGICAL", "Surgical", default_value=value or 0.85, is_checked=not readonly, is_disabled=readonly)},
    {"id": "vaccine-mrna", "component": lambda readonly, value: create_vaccine_type("MRNA", "MRNA (Moderna)", default_doses=value or [0.0, 0.31, 0.88], is_checked=not readonly, is_disabled=readonly)},
    {"id": "vaccine-astra", "component": lambda readonly, value: create_vaccine_type("ASTRA", "ASTRA (AstraZeneca)", default_doses=value or [0.0, 0.31, 0.67], is_checked=not readonly, is_disabled=readonly)},
]

agentconfig_fields = [
    {"id": "agent-config-name", "label": "Name", "type": "text", "className": "form-input"},
    {"id": "random-agents-input", "label": "Random Agents", "type": "number", "min": 0, "max": 10000, "className": "form-input-number"},
    {"id": "random-infected-input", "label": "Random Infected", "type": "number", "min": 0, "max": 10000, "className": "form-input-number"},
    # Add more fields as needed for default/custom agent config
]

def create_resource_modal(resource_type, title):
    """Create a modal for viewing and managing any resource."""
    return dbc.Modal([
        dbc.ModalHeader(dbc.ModalTitle(id={"type": "action-modal-title", "resource": resource_type}, children=title)),
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
                html.Div([
                    html.Label(label, className="dropdown-label"),
                    html.Img(src="/static/tooltip.png", id=f"{id}-tooltip", className="tooltip-icon"),
                ], className="dropdown-actions"),
                html.Button("Create", id={"type": "create-btn", "resource": f"{id}"}, title=f"Edit {label}", className="drop-down-btn btn-primary"),
                
            ], className="tooltip-container"),
        create_tooltip(f"Select a {label} from the dropdown. Click the buttons to edit, clone, or delete the selected {label.lower()}.", f"{id}-tooltip"),
        dcc.Dropdown(
            id={"type": "dropdown", "resource": f"{id}"},
            options=[{"label": opt["name"], "value": opt["id"]} for opt in options],
            placeholder=f"Select a {label}",
            className="dropdown-standard"
        ),
    ], className="dropdown-with-actions")

def create_generic_form(form_id, title, fields):
    """Create a reusable generic form that can be read-only or editable, with custom content."""
    form_fields_div_id = f"{form_id}-editable-fields"

    @callback(
        Output(form_fields_div_id, "children"),
        [
            Input({"type": "form-mode", "resource": form_id}, "data"),
            Input({"type": "original-data", "resource": form_id}, "data"),
        ],
    )
    def update_form_fields(mode_data, values_data):
        readonly = True
        if mode_data and mode_data.get("mode") == "edit":
            readonly = False
        return render_resource_form(fields, values=values_data, readonly=readonly)

    return html.Div([
        html.Div([
           
            html.Div([
                html.Label(title, className="form-label"),
                html.Button("Cancel Edit", 
                           id=f"{form_id}-cancel-btn", 
                           className="btn btn-secondary btn-sm",
                           style={"display": "none"})
            ], className="form-actions")
        ], className="form-header"),
        html.Div(
            id=form_fields_div_id, 
            className="form-editable-fields",
        ),
        # Form buttons (hidden by default)
        html.Div([
            html.Button("Save", id=f"{form_id}-save-btn", className="btn btn-primary btn-sm me-2"),
            html.Button("Cancel", id=f"{form_id}-cancel-btn-bottom", className="btn btn-secondary btn-sm")
        ], id={"type": "form-button-group", "resource": form_id}, 
           className="form-button-group",
           style={"display": "none"}),
        # Hidden stores for form state
        dcc.Store(id={"type": "form-mode", "resource": form_id}, data={"mode": "readonly", "resource_id": None}),
        dcc.Store(id={"type": "original-data", "resource": form_id})
    ], className="generic-form-container")


def create_scenario_form(resource_type):
    """Create a reusable scenario form that can be read-only or editable."""
    form_fields_div_id = f"{resource_type}-editable-fields"

    # Callback to control readonly state for subforms based on scenario form mode
    @callback(
        Output("virus-editable-fields", "children"),
        Output("prevention-editable-fields", "children"),
        Output("simulation-editable-fields", "children"),
        Input({"type": "form-mode", "resource": resource_type}, "data"),
        State({"type": "original-data", "resource": "virus"}, "data"),
        State({"type": "original-data", "resource": "prevention"}, "data"),
        State({"type": "original-data", "resource": "simulation"}, "data"),
    )
    def update_subforms(scenario_mode, virus_data, prevention_data, simulation_data):
        readonly = True
        if scenario_mode and scenario_mode.get("mode") == "edit":
            readonly = False
        virus_form = render_resource_form(virus_fields, values=virus_data, readonly=readonly)
        prevention_form = render_resource_form(prevention_fields, values=prevention_data, readonly=readonly)
        simulation_form = render_resource_form(simulation_fields, values=simulation_data, readonly=readonly)
        return virus_form, prevention_form, simulation_form

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

        html.Div([
            dcc.Tabs([
                dcc.Tab(label="Viruses", children=[
                    html.Div(id="virus-editable-fields", className="form-editable-fields"),
                ]),
                dcc.Tab(label="Preventions", children=[
                    html.Div(id="prevention-editable-fields", className="form-editable-fields"),
                ]),
                dcc.Tab(label="Simulations", children=[
                    html.Div(id="simulation-editable-fields", className="form-editable-fields"),
                ]),
            ])
        ]),

        # Add these stores so the callback can access their data!
        dcc.Store(id={"type": "original-data", "resource": "virus"}),
        dcc.Store(id={"type": "original-data", "resource": "prevention"}),
        dcc.Store(id={"type": "original-data", "resource": "simulation"}),

        dcc.Store(id={"type": "resource-store", "resource": "virus"}),
        dcc.Store(id={"type": "resource-store", "resource": "prevention"}),
        dcc.Store(id={"type": "resource-store", "resource": "simulation"}),

        html.Div([
            html.Button("Save", id=f"{resource_type}-save-btn", className="btn btn-primary btn-sm me-2"),
            html.Button("Cancel", id=f"{resource_type}-cancel-btn-bottom", className="btn btn-secondary btn-sm")
        ], id={"type": "form-button-group", "resource": resource_type}, 
           className="form-button-group",
           style={"display": "none"}),

        dcc.Store(id={"type": "form-mode", "resource": resource_type}, data={"mode": "readonly", "resource_id": None}),
        dcc.Store(id={"type": "original-data", "resource": resource_type})
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
            create_generic_form("agent_config", "Agent Config", agentconfig_fields)
        ], className="agent-config-form-column"),
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
        Output({"type": "action-modal-title", "resource": ALL}, "children"),
        Output({"type": "action-modal-summary", "resource": ALL}, "children"),
        Output({"type": "action-modal-details", "resource": ALL}, "children"),
        Output({"type": "resource-store", "resource": ALL}, "data"),
    ],
    [
        Input({"type": "dropdown", "resource": ALL}, "value"),
        Input({"type": "edit-btn", "resource": ALL}, "n_clicks"),
        Input({"type": "delete-btn", "resource": ALL}, "n_clicks"),
    ],
    State({"type": "action-modal", "resource": ALL}, "is_open"),
    prevent_initial_call=True
)
def update_modal_content(selected_ids, edit_clicks, delete_clicks, modals_open_state):
    """Update modal content for any resource type."""
    modals_open = []
    titles = []
    summaries = []
    details = []
    stores = []

    resource_types = ["scenario", "agent_config", "virus", "prevention", "simulation"]  # Add more types as needed

    # Ensure output lists have the same length as selected_ids
    for idx, resource_id in enumerate(selected_ids):
        if edit_clicks[idx] or delete_clicks[idx]:
            modals_open.append(False)
        else:
            modals_open.append(modals_open_state[idx])
        resource_type = resource_types[idx] if idx < len(resource_types) else "resource"
        if resource_id:
            success, resource, _ = api.get_by_id(resource_type, resource_id)
            title = resource["name"] if success and resource else "Resource Details"
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
                    html.Div(desc),                 
                ]
                detail = json.dumps(resource, indent=2)
                if modals_open_state[idx] is False:
                    modals_open[idx] = True # Open modal if it was previously closed
                titles.append(title)
                summaries.append(summary)
                details.append(detail)
                stores.append(resource_id)
            else:
                if modals_open_state[idx] is True:
                    modals_open[idx] = False # Close modal if resource fetch failed
                titles.append(title)
                summaries.append(f"No {title} Selected")
                details.append("")
                stores.append(None)
        else:
            if modals_open_state[idx] is True:
                modals_open[idx] = False # Close modal if no resource selected
            titles.append("No Resource Selected")
            summaries.append("No Resource Selected")
            details.append("")
            stores.append(None)

    return modals_open, titles, summaries, details, stores


# --- Edit Button Functionality ---
@callback(
    [
        Output({"type": "original-data", "resource": ALL}, "data"),
        Output({"type": "form-mode", "resource": ALL}, "data"),  
        Output({"type": "form-button-group", "resource": ALL}, "style"),
    ],
    [
        Input({"type": "edit-btn", "resource": ALL}, "n_clicks"),
        State({"type": "resource-store", "resource": ALL}, "data"),
    ],
    prevent_initial_call=True
)
def handle_edit_delete(edit_clicks, delete_clicks, resource_data):
    """Handle edit and delete button functionality for any resource type."""
    output_data = []
    output_store = []
    output_mode = []
    output_button_style = []

    for idx in range(len(edit_clicks)):
        edit_n = edit_clicks[idx]
        delete_n = delete_clicks[idx]
        resource_id = resource_data[idx]
        resource_type = ctx.inputs_list[0][idx]["id"]["resource"]

        if delete_n and delete_n > 0 and resource_id:
            success = api.delete(resource_type, resource_id)
            if success:
                output_data.append(None)
                output_store.append(None)
                output_mode.append({"mode": "readonly", "resource_id": None})
                output_button_style.append({"display": "none"})
            else:
                output_data.append(no_update)
                output_store.append(no_update)
                output_mode.append(no_update)
                output_button_style.append(no_update)
        elif edit_n and edit_n > 0 and resource_id:
            success, resource, _ = api.get_by_id(resource_type, resource_id)
            if success and resource:
                output_data.append(resource)
                output_store.append(resource_id)
                output_mode.append({"mode": "edit", "resource_id": resource_id})
                output_button_style.append({"display": "block"})
            else:
                output_data.append(no_update)
                output_store.append(no_update)
                output_mode.append(no_update)
                output_button_style.append(no_update)
        else:
            output_data.append(no_update)
            output_store.append(no_update)
            output_mode.append(no_update)
            output_button_style.append(no_update)

    return (
        output_data[:len(edit_clicks)],
        output_store[:len(edit_clicks)],
        output_mode[:len(edit_clicks)],
        output_button_style[:len(edit_clicks)]
    )