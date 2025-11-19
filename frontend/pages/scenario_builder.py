"""Scenario Builder Page for LocABS Application."""
from dash import html, dcc, register_page, callback, Output, Input, MATCH, State
import dash 
import dash_daq as daq
# import dash_bootstrap_components as dbc
from components_.tooltip import create_tooltip
from components_.notifications_modal import create_notification_modal
from utilities import dash_api
from utilities import validators

register_page(__name__, path="/scenario-builder", name="Scenario Builder", title="LocABS · Scenario Builder")

# TODO: Add save verbose - you accidentally skipped it in the UI
def create_config_panel():
    """Create the main configuration panel with tabs."""
    return html.Div(
        [
            # Tab headers
            html.Div(
                [
                    html.Button("SIMULATIONS", id="tab-simulations", className="tab-button tab-button-active"),
                    html.Button("PREVENTION", id="tab-prevention", className="tab-button tab-button-inactive"),
                ],
                className="tab-headers",
            ),
            # Tab content
            html.Div(id="tab-content", className="tab-content"),
        ],
        className="config-panel",
    )

def create_terrain_form():
    """Create terrain configuration form."""
    return html.Div([

        html.Div([
            html.Div([
                # Terrain Name
                html.Label("Name", className="form-label"),
                dcc.Input(
                    id="terrain-name",
                    type="text",
                    placeholder="Enter terrain name",
                    className="form-input",
                    #required=True,
                    minLength=1,
                    maxLength=250,
                    pattern="^[a-zA-Z0-9\\s_-]+$",  # Allow letters, numbers, spaces, underscores, hyphens
                ),

                # Terrain Properties
                html.Div([
                    html.Div([
                        html.Label("Terrain Type", className="form-label"),
                        html.Div([
                            dcc.Checklist(
                                id="terrain-walkable-checkbox",
                                options=[{"label": " Walkable", "value": "walkable"}],
                                value=["walkable"],
                                inline=True,
                                labelClassName="checklist-label",
                            ),
                            dcc.Checklist(
                                id="terrain-interactive-checkbox",
                                options=[{"label": " Interactive", "value": "interactive"}],
                                value=[],
                                inline=True,
                                labelClassName="checklist-label",
                            ),
                            dcc.Checklist(
                                id="terrain-restricted-checkbox",
                                options=[{"label": " Restricted", "value": "restricted"}],
                                value=[],
                                inline=True,
                                labelClassName="checklist-label",
                            ),
                        ], className="terrain-type-container"),
                            
                        # Access Level Selector
                        html.Div([
                            html.Label("Access Level", className="form-label-small"),
                            dcc.Input(
                                id="terrain-access-input",
                                type="number",
                                value=0,
                                min=0,
                                max=999,  # Reasonable max for access level
                                className="form-input-number",
                                required=True
                            ),
                        ], className="terrain-properties-column"),

                        # Action Buttons
                        html.Div([
                            html.Button("Create Terrain", id="create-terrain-btn", className="btn-primary"),
                            html.Button("Clear", id="clear-terrain-btn", className="btn-secondary"),
                        ], className="btn-container"),
                    ], className="terrain-properties-column"),

                ], className="terrain-properties-row"),

            ]),

            # Color Picker
            html.Div([
                html.Label("Terrain Color", className="form-label"),
                daq.ColorPicker(
                    id="terrain-color-input",
                    value=dict(hex="#0000FF", label="Terrain Color"),
                    size=250
                )
            ]),
        ],
        className="terrain-form-container"
        ),
    ])

def create_virus_form():
    """Create virus configuration form."""
    return html.Div([
        # Virus Name 
        html.Label("Name", className="form-label"),
         dcc.Input(
            id="virus-name",
            type="text",
            placeholder="Enter virus name",
            className="form-input",
            minLength=1,
            maxLength=250,
            pattern="^[a-zA-Z0-9\\s_-]+$",
        ),

        # Attack Rate and Infection Rate
        html.Div([
            html.Div([
                html.Label("Attack Rate", className="form-label-small"),
                dcc.Input(
                    id="virus-attack-rate",
                    type="number",
                    min=0,
                    max=1,
                    step=0.001,
                    value=0.0,
                    placeholder="0.000 - 1.000",
                    className="virus-rate-input",
                ),
            ], className="virus-rate-column"),
            
            html.Div([
                html.Label("Infection Rate", className="form-label-small"),
                dcc.Input(
                    id="virus-infection-rate",
                    type="number",
                    min=0,
                    max=1,
                    step=0.001,
                    value=0.0,
                    placeholder="0.000 - 1.000",
                    className="virus-rate-input",
                ),
            ], className="virus-rate-column"),
        ], className="virus-rates-row"),
        
        # Fatality Rate
        html.Div([
            html.Label("Fatality Rate", className="form-label"),
            dcc.Input(
                id="virus-fatality-rate",
                type="number",
                min=0,
                max=1,
                step=0.001,
                value=0.0,
                placeholder="0.000 - 1.000",
                className="virus-rate-input",
            ),
        ], className="virus-rate-container"),

        # Action Buttons
        html.Div([
            html.Button("Create Virus", id="create-virus-btn", className="btn-primary"),
            html.Button("Clear", id="clear-virus-btn", className="btn-secondary"),
        ], className="btn-container"),
    ])


def create_agent_config_form():
    """Create agent configuration form."""
    return html.Div([
        html.Div("AGENT CONFIGURATION", className="agent-config-header"),
        
        # Agent Config Name
        html.Label("Name", className="form-label"),
        dcc.Input(
            id="agent-config-name",
            type="text",
            placeholder="Enter agent configuration name",
            className="form-input",
            minLength=1,
            maxLength=250,
            pattern="^[a-zA-Z0-9\\s_-]+$",
        ),

        # Agent Population Section
        html.H6("Agent Population", className="section-header"),
        html.Div([
            # Random Agents
            html.Div([
                html.Label("Random Agents", className="form-label-small"),
                dcc.Input(
                    id="random-agents-input",
                    type="number",
                    value=1,
                    min=0,
                    max=10000, 
                    className="form-input-number",
                ),
            ], className="agent-population-item"),

            # Random Infected
            html.Div([
                html.Label("Random Infected", className="form-label-small"),
                dcc.Input(
                    id="random-infected-input",
                    type="number",
                    value=0,
                    min=0,
                    max=10000, 
                    className="form-input-number",
                ),
            ], className="agent-population-item"),
        ], className="agent-population-row"),

        # TODO: Add back default agent configuration and initial agent state sections - Ask Phillip about whether needed

        html.Div([
            html.Button("Create", id="create-agent-config-btn", className="btn-primary"),
            html.Button("Clear", id="clear-agent-config-btn", className="btn-secondary"),
        ], className="btn-container"),

    ], className="agent-config-container")


def create_side_panel(title, content_id):
    """Create a side panel with title and content."""
    if content_id == "terrain-content":
        panel_content = create_terrain_form()
    elif content_id == "virus-content":
        panel_content = create_virus_form()
    elif content_id == "agent-content":
        panel_content = create_agent_config_form()
    else:
        panel_content = "Content placeholder"
    
    return html.Div(
        [
            html.Div(title, className="side-panel-header"),
            html.Div(panel_content, className="side-panel-content"),
        ],
        className="side-panel",
    )

def create_mask_input(mask_type, label, default_value=0.5, is_checked=False):
    """Create a mask input component with label and slider."""
    return html.Div([
        dcc.Checklist(
            id={"type": "mask-checkbox", "mask": mask_type},
            options=[{"label": f" {label}", "value": mask_type}],
            value=[mask_type] if is_checked else [],
            inline=True,
            labelClassName="mask-checkbox-label",
        ),
        html.Div(
            dcc.Slider(
                id={"type": "mask-effectiveness-slider", "mask": mask_type},
                min=0, max=1, step=0.01, value=default_value,
                marks={0: "0%", 0.5: "50%", 1: "100%"},
                tooltip={"placement": "bottom", "always_visible": True},
                className="mask-slider"
            ),
            id={"type": "mask-slider-container", "mask": mask_type},
            className="mask-slider-container",
            style={"display": "block" if is_checked else "none"},
        ),
    ], className="mask-input-wrapper")

def create_vaccine_type(vaccine_type, label, default_doses=[0.5, 0.5, 0.5], is_checked=False):
    """Create a vaccine input component.
    
    Args:
        vaccine_type (str): The type of vaccine (e.g., "MRNA").
        label (str): The label to display next to the checkbox.
        default_doses (list): List of default effectiveness values for doses 1, 2, and 3.
        is_checked (bool): Whether the vaccine checkbox is checked by default.

    Returns:
        html.Div: A Dash HTML Div component representing the vaccine input.
    """
    return html.Div([
        dcc.Checklist(
            id={"type": "vaccine-checkbox", "vaccine": vaccine_type},
            options=[{"label": f" {label}", "value": vaccine_type}],
            value=[vaccine_type] if is_checked else [],
            inline=True,
            labelClassName="vaccine-checkbox-label",
        ),

        html.Label("Effectiveness", className="form-label"),
        
        html.Div(
            [
                html.Div([
                    html.Div("Dose 1", className="vaccine-dose-header-item"),
                    html.Div("Dose 2", className="vaccine-dose-header-item"),
                    html.Div("Dose 3", className="vaccine-dose-header-item"),
                ], className="vaccine-dose-header"),
                
                html.Div([
                    dcc.Input(
                        id={"type": "vaccine-dose", "vaccine": vaccine_type, "dose": 1},
                        type="number", min=0, max=1, step=0.01, value=default_doses[0],
                        placeholder="0.00", className="vaccine-dose-input",
                    ),
                    dcc.Input(
                        id={"type": "vaccine-dose", "vaccine": vaccine_type, "dose": 2},
                        type="number", min=0, max=1, step=0.01, value=default_doses[1],
                        placeholder="0.00", className="vaccine-dose-input",
                    ),
                    dcc.Input(
                        id={"type": "vaccine-dose", "vaccine": vaccine_type, "dose": 3},
                        type="number", min=0, max=1, step=0.01, value=default_doses[2],
                        placeholder="0.00", className="vaccine-dose-input",
                    ),
                ], className="vaccine-dose-inputs"),
            ],
            id={"type": "vaccine-doses-container", "vaccine": vaccine_type},
            className="vaccine-doses-container",
            style={"display": "block" if is_checked else "none"},
        ),
    ], className="vaccine-wrapper")


# Layout
layout = html.Div(
    [

        html.Div(
            [
                html.Div(
                            [
                                create_side_panel("TERRAINS", "terrain-content"),
                                create_side_panel("VIRUS", "virus-content"),
                            ],
                            className="side-panels-container",
                        ),
                create_config_panel(),
            ],
            className="main-container",
        ),
        
        html.Div([create_agent_config_form()]),

        # Notification Modal Container
        create_notification_modal(),
    ],
    className="scenario-builder-page",
)

# Callbacks
# Terrrain Operations
@callback(
    [
        Output("notification-modal", "is_open"),
        Output("notification-modal-body", "children"),
        Output("notification-modal", "className"),
        Output("terrain-name", "value"),
        Output("terrain-walkable-checkbox", "value"),  
        Output("terrain-interactive-checkbox", "value"),
        Output("terrain-restricted-checkbox", "value"),
        Output("terrain-access-input", "value"),
        Output("terrain-color-input", "value"),   
    ],  
    Input("create-terrain-btn", "n_clicks"),
    [
        State("terrain-name", "value"),
        State("terrain-walkable-checkbox", "value"),
        State("terrain-interactive-checkbox", "value"),
        State("terrain-restricted-checkbox", "value"),
        State("terrain-access-input", "value"),
        State("terrain-color-input", "value"),
    ],
    prevent_initial_call=True,
)

def create_terrain(n_clicks, name, walkable, interactive, restricted, access_level, color):
    """Create a new terrain via backend API.

    Args:
        n_clicks (int): Number of clicks on the create terrain button.
        name (str): Name of the terrain.
        walkable (list): List of walkable types selected.
        interactive (list): List of interactive types selected.
        restricted (list): List of restricted types selected.
        access_level (int): Access level of the terrain.
        color (dict): Color value from the color picker.
        terrains_data (list): Current list of terrains in the store.

    Returns:
        tuple: Updated terrains data, notification message, and cleared input values.
    """
    if n_clicks is None or name is None:
        return dash.no_update
    
    # Parse checkbox values
    is_walkable = "walkable" in (walkable or [])
    is_interactive = "interactive" in (interactive or [])
    is_restricted = "restricted" in (restricted or [])

    # Extract color hex value
    color_hex = color.get("hex", "#000000") if color else "#000000"

    is_name_valid, validated_name, error_msg = validators.validate_slug_name(name)
    
    if not is_name_valid:
        notification_body = html.Div([
            error_msg
        ])
        return (
            True, notification_body, "notification-error",
            *([dash.no_update] * 6)
        )

    is_color_valid, valid_color_hex, color_error_msg = validators.validate_hex_color(color_hex)
    if not is_color_valid:
        notification_body = html.Div([
            color_error_msg
        ])
        return (
            True, notification_body, "notification-error",
            *([dash.no_update] * 6)
        )
    # Prepare terrain data
    terrain_data = {
        "name": validated_name,
        "value": valid_color_hex,
        "color": valid_color_hex,
        "walkable": is_walkable,
        "interactive": is_interactive,
        "restricted": is_restricted,
        "access_level": access_level or 0,
    }

    # Call API to create terrain
    success, data, message = dash_api.create('terrain', terrain_data)
    if success:
        # Success notification
        notification_body = html.Div([
            f"Terrain '{validated_name.capitalize()}' created successfully!"
        ])
        modal_class = "notification-success"
        return(
            True,
            notification_body,
            modal_class,
            "",  # Clear name
            ["walkable"],  # Reset to default
            [],  # Clear interactive
            [],  # Clear restricted
            0,   # Reset access level
            {"hex": "#0000FF", "label": "Terrain Color"},  # Reset color
        )

    else:
        # Error notification
        notification_body = html.Div([
            f"Error creating terrain: {message}"
        ])
        modal_class = "notification-error"
        return(
            True,
            notification_body,
            modal_class,
            *([dash.no_update] * 6)
        )

@callback(
    Output("notification-modal", "is_open", allow_duplicate=True),
    Input("close-notification-modal", "n_clicks"),
    State("notification-modal", "is_open"),
    prevent_initial_call=True,
)
def close_modal(n_clicks, is_open):
    """Close the notification modal."""
    if n_clicks and is_open:
        return False
    return dash.no_update


# Clear Terrain Form Callback
@callback(
    [
        Output("terrain-name", "value", allow_duplicate=True),
        Output("terrain-walkable-checkbox", "value", allow_duplicate=True),
        Output("terrain-interactive-checkbox", "value", allow_duplicate=True),
        Output("terrain-restricted-checkbox", "value", allow_duplicate=True),
        Output("terrain-access-input", "value", allow_duplicate=True),
        Output("terrain-color-input", "value", allow_duplicate=True),
    ],
    Input("clear-terrain-btn", "n_clicks"),
    prevent_initial_call=True,
)
def clear_terrain_form(n_clicks):
    """Clear the terrain form."""
    if not n_clicks:
        return dash.no_update
    return "", ["walkable"], [], [], 0, {"hex": "#0000FF", "label": "Terrain Color"}

# Virus Operations
@callback(
    [
        Output("notification-modal", "is_open", allow_duplicate=True),
        Output("notification-modal-body", "children", allow_duplicate=True),    
        Output("notification-modal", "className", allow_duplicate=True),
        Output("virus-name", "value"),
        Output("virus-attack-rate", "value"),
        Output("virus-infection-rate", "value"),
        Output("virus-fatality-rate", "value"),   
    ],

    Input("create-virus-btn", "n_clicks"),
    [
        State("virus-name", "value"),
        State("virus-attack-rate", "value"),
        State("virus-infection-rate", "value"),
        State("virus-fatality-rate", "value"),  
    ],
    prevent_initial_call=True,
)
def create_virus(n_clicks, name, attack_rate, infection_rate, fatality_rate):
    """Create a new virus via backend API.

    Args:
        n_clicks (int): Number of clicks on the create virus button.
        name (str): Name of the virus.
        attack_rate (float): Attack rate of the virus.
        infection_rate (float): Infection rate of the virus.
        fatality_rate (float): Fatality rate of the virus.
    
    Returns:
        tuple: Notification modal states and cleared input values.
    """
    if n_clicks is None or name is None:
        return dash.no_update

    is_valid, validated_name, error_msg = validators.validate_slug_name(name)
    if not is_valid:
        notification_body = html.Div([
            error_msg
        ])
        return (
            True, notification_body, "notification-error",
            *([dash.no_update] * 6)
        )

    # Prepare virus data
    virus_data = {
        "name": validated_name,
        "attack_rate": float(attack_rate or 0.0),
        "infection_rate": float(infection_rate or 0.0),
        "fatality_rate": float(fatality_rate or 0.0),
    }

    success, data, message = dash_api.create('virus', virus_data)
    if success:
        # Success notification
        notification_body = html.Div([
            f"Virus '{name}' created successfully!"
        ])
        modal_class = "notification-success"
        return(
            True,
            notification_body,
            modal_class,
            "",  # Clear name
            0.0,  # Clear attack rate
            0.0,  # Clear infection rate
            0.0,  # Clear fatality rate
        )
    else:
        # Error notification
        notification_body = html.Div([
            f"Error creating virus: {message}"
        ])

        modal_class = "notification-error"

        return(
            True,
            notification_body,
            modal_class,
            *([dash.no_update] * 4)
        )

# Clear Virus Form Callback
@callback(
    [
        Output("virus-name", "value", allow_duplicate=True),
        Output("virus-attack-rate", "value", allow_duplicate=True),
        Output("virus-infection-rate", "value", allow_duplicate=True),
        Output("virus-fatality-rate", "value", allow_duplicate=True),
    ],
    Input("clear-virus-btn", "n_clicks"),
    prevent_initial_call=True,
)
def clear_virus_form(n_clicks):
    """Clear the virus form."""
    if not n_clicks:
        return dash.no_update
    return "", 0.0, 0.0, 0.0

# Simulations Operations
@callback(
    Output("terrain-dropdown", "options"),
    Input("url", "pathname"),  # Trigger on page load
    prevent_initial_call=False,
)

@callback(
    [
        Output("notification-modal", "is_open", allow_duplicate=True),
        Output("notification-modal-body", "children", allow_duplicate=True),
        Output("notification-modal", "className", allow_duplicate=True),
        Output("simulation-name", "value"),
        Output("map-file-dropdown", "value"),
        Output("xy-scale-input", "value"),
        Output("time-step-input", "value"),
        Output("save-resolution-input", "value"),
        Output("max-iterations-input", "value"),
        Output("terrain-dropdown", "value"),
    ],
    Input("create-simulation-btn", "n_clicks"),
    [
        State("simulation-name", "value"),
        State("map-file-dropdown", "value"),
        State("xy-scale-input", "value"),
        State("time-step-input", "value"),
        State("save-resolution-input", "value"),
        State("max-iterations-input", "value"),
        State("terrain-dropdown", "value"),
    ],
    prevent_initial_call=True,
)
def create_simulation(n_clicks, name, map_file, xy_scale, time_step, save_resolution, max_iterations, terrain_ids):
    """Create a new simulation via backend API.

    Args:
        n_clicks (int): Number of clicks on the create simulation button.
        name (str): Name of the simulation.
        map_file (str): Selected map file.
        xy_scale (float): Plot scale for X and Y axes.
        time_step (float): Time step in seconds.
        save_resolution (int): Save resolution.
        max_iterations (int): Maximum number of iterations.
        terrain_ids (list): Selected terrain IDs.

    Returns:
        tuple: Notification modal states and cleared input values.
    """
    if n_clicks is None or map_file is None:
        return dash.no_update

    is_name_valid, validated_name, name_error = validators.validate_slug_name(name)
    if not is_name_valid:
        notification_body = html.Div([
            name_error
        ])
        return (
            True, notification_body, "notification-error",
            *([dash.no_update] * 7)
        )

    # Validate required fields
    if not map_file:
        notification_body = html.Div([
            "Error creating simulation: Map file is required. Please select a map file."
        ])
        return (
            True,
            notification_body,
            "notification-error",
            *([dash.no_update] * 7)
        )
    
    if not terrain_ids or len(terrain_ids) == 0:
        notification_body = html.Div([
            "At least one terrain must be selected."
        ])
        return (
            True, notification_body, "notification-error",
            dash.no_update, dash.no_update, dash.no_update,
            dash.no_update, dash.no_update, dash.no_update,
            dash.no_update
        )

    # TODO: Confirm default values with Phillip and Implement Default options in the UI if necessary
    # Ways to do defaults: placeholder texts, default values in the input fields, default selections in dropdowns when creating new simulation or new scenaerio
    simulation_data = {
        "name": name,
        "mapfile": map_file,
        "xy_scale": float(xy_scale) if xy_scale else 2.77,
        "t_step": float(time_step) if time_step else 5.0,
        "save_resolution": int(save_resolution) if save_resolution else 12,
        "max_iter": int(max_iterations) if max_iterations else 250,
        "save_verbose": None,
        "terrain": terrain_ids,
    }


    # Call API to create simulation
    success, data, message = dash_api.create('simulation', simulation_data)

    if success:
        notification_body = html.Div([
            f"Simulation '{name}' created successfully!"
        ])
        modal_class = "notification-success"
        return(
            True,
            notification_body,
            modal_class,
            "", None, 2.77, 5.0, 12, 250, None
        )

    else:
        notification_body = html.Div([
            f"Error creating simulation: {message}"
        ])
        modal_class = "notification-error"
        return(
            True,
            notification_body,
            modal_class,
            *([dash.no_update] * 7)
        )

@callback(
    [
        Output("simulation-name", "value", allow_duplicate=True),
        Output("map-file-dropdown", "value", allow_duplicate=True),
        Output("xy-scale-input", "value", allow_duplicate=True),
        Output("time-step-input", "value", allow_duplicate=True),
        Output("save-resolution-input", "value", allow_duplicate=True),
        Output("max-iterations-input", "value", allow_duplicate=True),
        Output("terrain-dropdown", "value", allow_duplicate=True),
    ],
    Input("clear-simulation-btn", "n_clicks"),
    prevent_initial_call=True,
)
def clear_simulation_form(n_clicks):
    """Clear the simulation form.
    
    Args:
        n_clicks (int): Number of clicks on clear button.
    
    Returns:
        tuple: Cleared input values.
    """
    if not n_clicks:
        return dash.no_update
    return "", None, 2.77, 5.0, 12, 250, None


# Prevention Operations
@callback(
    [
        Output("notification-modal", "is_open", allow_duplicate=True),
        Output("notification-modal-body", "children", allow_duplicate=True),
        Output("notification-modal", "className", allow_duplicate=True),
        Output("prevention-name", "value"),
        Output({"type": "mask-checkbox", "mask": "N95"}, "value"),
        Output({"type": "mask-effectiveness-slider", "mask": "N95"}, "value"),
        Output({"type": "mask-checkbox", "mask": "HOME"}, "value"),
        Output({"type": "mask-effectiveness-slider", "mask": "HOME"}, "value"),
        Output({"type": "mask-checkbox", "mask": "CLOTH"}, "value"),
        Output({"type": "mask-effectiveness-slider", "mask": "CLOTH"}, "value"),
        Output({"type": "mask-checkbox", "mask": "SURGICAL"}, "value"),
        Output({"type": "mask-effectiveness-slider", "mask": "SURGICAL"}, "value"),
        Output({"type": "vaccine-checkbox", "vaccine": "MRNA"}, "value"),
        Output({"type": "vaccine-dose", "vaccine": "MRNA", "dose": 1}, "value"),
        Output({"type": "vaccine-dose", "vaccine": "MRNA", "dose": 2}, "value"),
        Output({"type": "vaccine-dose", "vaccine": "MRNA", "dose": 3}, "value"),
        Output({"type": "vaccine-checkbox", "vaccine": "ASTRA"}, "value"),
        Output({"type": "vaccine-dose", "vaccine": "ASTRA", "dose": 1}, "value"),
        Output({"type": "vaccine-dose", "vaccine": "ASTRA", "dose": 2}, "value"),
        Output({"type": "vaccine-dose", "vaccine": "ASTRA", "dose": 3}, "value"),
    ],
    Input("create-prevention-btn", "n_clicks"),
    [
        State("prevention-name", "value"),
        State({"type": "mask-checkbox", "mask": "N95"}, "value"),
        State({"type": "mask-effectiveness-slider", "mask": "N95"}, "value"),
        State({"type": "mask-checkbox", "mask": "HOME"}, "value"),
        State({"type": "mask-effectiveness-slider", "mask": "HOME"}, "value"),
        State({"type": "mask-checkbox", "mask": "CLOTH"}, "value"),
        State({"type": "mask-effectiveness-slider", "mask": "CLOTH"}, "value"),
        State({"type": "mask-checkbox", "mask": "SURGICAL"}, "value"),
        State({"type": "mask-effectiveness-slider", "mask": "SURGICAL"}, "value"),
        State({"type": "vaccine-checkbox", "vaccine": "MRNA"}, "value"),
        State({"type": "vaccine-dose", "vaccine": "MRNA", "dose": 1}, "value"),
        State({"type": "vaccine-dose", "vaccine": "MRNA", "dose": 2}, "value"),
        State({"type": "vaccine-dose", "vaccine": "MRNA", "dose": 3}, "value"),
        State({"type": "vaccine-checkbox", "vaccine": "ASTRA"}, "value"),
        State({"type": "vaccine-dose", "vaccine": "ASTRA", "dose": 1}, "value"),
        State({"type": "vaccine-dose", "vaccine": "ASTRA", "dose": 2}, "value"),
        State({"type": "vaccine-dose", "vaccine": "ASTRA", "dose": 3}, "value"),        
    ],
    prevent_initial_call=True,
)
def create_prevention(n_clicks, name,
                          n95_checked, n95_eff,
                          home_checked, home_eff,
                          cloth_checked, cloth_eff,
                          surgical_checked, surgical_eff,
                          mrna_checked, mrna_dose1, mrna_dose2, mrna_dose3,
                          astra_checked, astra_dose1, astra_dose2, astra_dose3):
    """Create a new prevention configuration via backend API.

    Args:
        n_clicks (int): Number of clicks on the create prevention button.
        name (str): Name of the prevention configuration.
        n95_checked (list): N95 mask checkbox value.
        n95_eff (float): N95 mask effectiveness.
        home_checked (list): Home mask checkbox value.
        home_eff (float): Home mask effectiveness.
        cloth_checked (list): Cloth mask checkbox value.
        cloth_eff (float): Cloth mask effectiveness.
        surgical_checked (list): Surgical mask checkbox value.
        surgical_eff (float): Surgical mask effectiveness.
        mrna_checked (list): MRNA vaccine checkbox value.
        mrna_dose1 (float): MRNA vaccine dose 1 effectiveness.
        mrna_dose2 (float): MRNA vaccine dose 2 effectiveness.
        mrna_dose3 (float): MRNA vaccine dose 3 effectiveness.
        astra_checked (list): Astra vaccine checkbox value.
        astra_dose1 (float): Astra vaccine dose 1 effectiveness.
        astra_dose2 (float): Astra vaccine dose 2 effectiveness.
        astra_dose3 (float): Astra vaccine dose 3 effectiveness.

    Returns:
        tuple: Notification modal states and cleared input values.
    """
    if n_clicks is None:
        return dash.no_update

    is_name_valid, validated_name, name_error = validators.validate_slug_name(name)
    if not is_name_valid:
        notification_body = html.Div([
            name_error
        ])
        return (
            True, notification_body, "notification-error",
            *([dash.no_update] * 17)
        )

    mask_data = {}
    if n95_checked and "N95" in n95_checked:
        mask_data["N95"] = n95_eff if n95_eff is not None else 0.85
    if home_checked and "HOME" in home_checked:
        mask_data["HOME"] = home_eff if home_eff is not None else 0.0
    if cloth_checked and "CLOTH" in cloth_checked:
        mask_data["CLOTH"] = cloth_eff if cloth_eff is not None else 0.83
    if surgical_checked and "SURGICAL" in surgical_checked:
        mask_data["SURGICAL"] = surgical_eff if surgical_eff is not None else 0.85
    
    vaccine_data = {}
    if mrna_checked and "MRNA" in mrna_checked:
        vaccine_data["MRNA"] = [
            mrna_dose1 if mrna_dose1 is not None else 0.0,
            mrna_dose2 if mrna_dose2 is not None else 0.31,
            mrna_dose3 if mrna_dose3 is not None else 0.88,
        ]

    if astra_checked and "ASTRA" in astra_checked:
        vaccine_data["ASTRA"] = [
            astra_dose1 if astra_dose1 is not None else 0.0,
            astra_dose2 if astra_dose2 is not None else 0.31,
            astra_dose3 if astra_dose3 is not None else 0.67,
        ]

    prevention_date = {
        "name": validated_name,
        "mask": mask_data,
        "vax": vaccine_data,
    }

    success, data, message = dash_api.create('prevention', prevention_date)
    if success:
        notification_body = html.Div([
            f"Prevention configuration '{name}' created successfully!"
        ])
        modal_class = "notification-success"
        return(
            True, notification_body, modal_class,
            "",         # Clear prevention name
            [], 0.85,   # Clear N95 - Reset to defaults
            [], 0.0,    # Clear HOME - Reset to defaults
            [], 0.83,   # Clear CLOTH - Reset to defaults
            [], 0.85,   # Clear SURGICAL - Reset to defaults
            [], 0.0, 0.31, 0.88,   # Clear MRNA - Reset to defaults
            [], 0.0, 0.31, 0.67,   # Clear ASTRA - Reset to defaults
        )
    else:
        notification_body = html.Div([
            f"Error creating prevention configuration: {message}"
        ])
        modal_class = "notification-error"
        return(
            True,
            notification_body,
            modal_class,
            *([dash.no_update] * 17)
        )

@callback(
    [
        Output("prevention-name", "value", allow_duplicate=True),
        Output({"type": "mask-checkbox", "mask": "N95"}, "value", allow_duplicate=True),
        Output({"type": "mask-effectiveness-slider", "mask": "N95"}, "value", allow_duplicate=True),
        Output({"type": "mask-checkbox", "mask": "HOME"}, "value", allow_duplicate=True),
        Output({"type": "mask-effectiveness-slider", "mask": "HOME"}, "value", allow_duplicate=True),
        Output({"type": "mask-checkbox", "mask": "CLOTH"}, "value", allow_duplicate=True),
        Output({"type": "mask-effectiveness-slider", "mask": "CLOTH"}, "value", allow_duplicate=True),
        Output({"type": "mask-checkbox", "mask": "SURGICAL"}, "value", allow_duplicate=True),
        Output({"type": "mask-effectiveness-slider", "mask": "SURGICAL"}, "value", allow_duplicate=True),
        Output({"type": "vaccine-checkbox", "vaccine": "MRNA"}, "value", allow_duplicate=True),
        Output({"type": "vaccine-dose", "vaccine": "MRNA", "dose": 1}, "value", allow_duplicate=True),
        Output({"type": "vaccine-dose", "vaccine": "MRNA", "dose": 2}, "value", allow_duplicate=True),
        Output({"type": "vaccine-dose", "vaccine": "MRNA", "dose": 3}, "value", allow_duplicate=True),
        Output({"type": "vaccine-checkbox", "vaccine": "ASTRA"}, "value", allow_duplicate=True),
        Output({"type": "vaccine-dose", "vaccine": "ASTRA", "dose": 1}, "value", allow_duplicate=True),
        Output({"type": "vaccine-dose", "vaccine": "ASTRA", "dose": 2}, "value", allow_duplicate=True),
        Output({"type": "vaccine-dose", "vaccine": "ASTRA", "dose": 3}, "value", allow_duplicate=True),
    ],
    Input("clear-prevention-btn", "n_clicks"),
    prevent_initial_call=True,
)
def clear_prevention_form(n_clicks):
    """Clear the prevention form."""
    if not n_clicks:
        return dash.no_update
    return (
        "",         # Clear prevention name
        [], 0.85,   # Clear N95 - Reset to defaults
        [], 0.0,    # Clear HOME - Reset to defaults
        [], 0.83,   # Clear CLOTH - Reset to defaults
        [], 0.85,   # Clear SURGICAL - Reset to defaults
        [], 0.0, 0.31, 0.88,   # Clear MRNA - Reset to defaults
        [], 0.0, 0.31, 0.67,   # Clear ASTRA - Reset to defaults
    )

#Agent Confiuration Operations
@callback(
    [
        Output("notification-modal", "is_open", allow_duplicate=True),
        Output("notification-modal-body", "children", allow_duplicate=True),
        Output("notification-modal", "className", allow_duplicate=True),
        Output("agent-config-name", "value"),
        Output("random-agents-input", "value"),
        Output("random-infected-input", "value"),
    ],
    Input("create-agent-config-btn", "n_clicks"),
    [
        State("agent-config-name", "value"),
        State("random-agents-input", "value"),
        State("random-infected-input", "value"),

    ],
    prevent_initial_call=True,
)

def create_agent_config(n_clicks, name, random_agents, random_infected):
    """Create a new agent configuration via backend API.
    
    Args:
        n_clicks (int): Number of clicks on the create agent configuration button.
        name (str): Name of the agent configuration.
        random_agents (int): Number of random agents.
        random_infected (int): Number of random infected agents.
    
    Returns:
        tuple: Notification modal states and cleared input values.
    """
    if n_clicks is None or name is None:
        return dash.no_update

    is_name_valid, validated_name, name_error = validators.validate_slug_name(name)
    if not is_name_valid:
        notification_body = html.Div([
            name_error
        ])
        return (
            True, notification_body, "notification-error",
            *([dash.no_update] * 3)
        )

    default_config = {
                    "info": {
                        "mask_type": "",
                        "vax_type": "",
                        "vax_doses": 0,
                        "schedule": {},
                        "work_zone": None,
                        "start_zone": None
                    },
                    "state": {
                        "x": 0,
                        "y": 0,
                        "status": "UNKNOWN"
                    }
    }

    custom_config = [ ]

    agent_config_data = {
        "name": validated_name,
        "default": default_config,  # JSONField - dict with 'info' and 'state'
        "random_agents": int(random_agents),
        "random_infected": int(random_infected),
        "custom": custom_config,  
        
    }

    success, data, message = dash_api.create('agent_config', agent_config_data)
    if success:
        notification_body = html.Div([
            f"Agent configuration '{name}' created successfully!"
        ])
        modal_class = "notification-success"
        return(
            True, notification_body, modal_class,
            "", 0, 0
        )
    else:
        notification_body = html.Div([
            f"Error creating agent configuration: {message}"
        ])
        modal_class = "notification-error"
        return(
            True,
            notification_body,
            modal_class,
            *([dash.no_update] * 3)
        )

# Tab Switching Callback
@callback(
    [
        Output("tab-content", "children"),
        Output("tab-simulations", "className"),
        Output("tab-prevention", "className"),
    ],
    [
        Input("tab-simulations", "n_clicks"),
        Input("tab-prevention", "n_clicks"),
    ],
    prevent_initial_call=False,
)

def switch_tabs(sim_clicks, prev_clicks):
    """Switch between Simulations and Prevention tabs.
    
    Args:
        sim_clicks (int): Number of clicks on the Simulations tab.
        prev_clicks (int): Number of clicks on the Prevention tab.    
    
    Returns:
        tuple: Content for the selected tab and updated class names for the tab buttons.
    """
    ctx = dash.callback_context
    active_tab = "simulations"
    
    if ctx.triggered:
        button_id = ctx.triggered[0]["prop_id"].split(".")[0]
        if button_id == "tab-prevention":
            active_tab = "prevention"
    
    if active_tab == "simulations":

        success_terrain, terrains, _ = dash_api.get_all('terrain')
        terrain_options = []
        if success_terrain and terrains:
            terrain_options = [
                {"label": f"{t['id']} - {t['name']}", "value": t['id']} 
                for t in terrains
            ]

        success_maps, map_files_paths, _ = dash_api.get_map_files()
        map_options = []
        if success_maps and map_files_paths:
            map_options = []
            for mp in map_files_paths:
                display_name = mp.replace('data/mapfiles/', '').replace('_', ' ').title()
            
                map_options.append({
                    "label": display_name,  # "Bow View Manor"
                    "value": mp       # "data/mapfiles/bow_view_manor"
                })
        

        time_step_options = [
        {"label": "1 second", "value": 1},
        {"label": "5 seconds", "value": 5},
        {"label": "10 seconds", "value": 10},
        {"label": "30 seconds", "value": 30},
        {"label": "1 minute (60s)", "value": 60},
        {"label": "5 minutes (300s)", "value": 300},
        {"label": "10 minutes (600s)", "value": 600},
        {"label": "30 minutes (1800s)", "value": 1800},
        {"label": "1 hour (3600s)", "value": 3600},
    ]

        content = html.Div([
            html.H5("Simulation Configuration", className="simulation-header"),

            # Simulation Name
            html.Label(" Name", className="form-label"),
            dcc.Input(
                id="simulation-name",
                type="text",
                placeholder="Enter simulation name",
                className="form-input"
            ),
            
            # Map File with Tooltip
            html.Div([
                html.Label("Map File", className="form-label"),
                html.Img(src="/static/tooltip.png", id="map-file-tooltip")
            ], className="tooltip-container"),
            create_tooltip(
                "Select the map file that defines the terrain and environment for the simulation.",
                "map-file-tooltip"
            ),
            dcc.Dropdown(
                id="map-file-dropdown",
                options=map_options,
                placeholder="Select map file",
                className="dropdown-standard",
            ),
            
            # Plot Scale with Tooltip
            html.Div([
                html.Label("Plot Scale", className="form-label"),
                html.Img(src="/static/tooltip.png", id="xy-scale-tooltip")
            ], className="tooltip-container"),
            create_tooltip(
                "Defines the scale for the X and Y axes on the simulation plot.",
                "xy-scale-tooltip"
            ),
            dcc.Input(
                id="xy-scale-input",
                type="number",
                placeholder="2.77",
                value=2.77,
                min= 1.0,
                max= 1000000.0,
                step=0.01,
                className="form-input"
            ),

            # Time Step with Tooltip
            html.Div([
                html.Label("Time Step (s)", className="form-label"),
                html.Img(src="/static/tooltip.png", id="time-step-tooltip")
            ], className="tooltip-container"),
            create_tooltip(
                "Defines the duration of each simulation step in seconds.",
                "time-step-tooltip"
            ),
            dcc.Dropdown(
            id="time-step-input",
            options=time_step_options,
            value=1,  # Default to 1 second
            placeholder="Select time step",
            className="dropdown-standard",
            clearable=False,
               ),

            # Save Resolution with Tooltip
            html.Div([
                html.Label("Save Resolution", className="form-label"),
                html.Img(src="/static/tooltip.png", id="save-resolution-tooltip")
            ], className="tooltip-container"),
            create_tooltip(
                "Number of time steps per iteration.",
                "save-resolution-tooltip"
            ),
            dcc.Input(
                id="save-resolution-input",
                type="number",
                placeholder="12",
                value=12,
                min=1,
                max=2147483647,
                step=1,
                className="form-input"
            ),
            
            # Max Iterations with Tooltip
            html.Div([
                html.Label("Max Iterations", className="form-label"),
                html.Img(src="/static/tooltip.png", id="max-iterations-tooltip")
            ], className="tooltip-container"),
            create_tooltip(
                "Total number of iterations to run the simulation.",
                "max-iterations-tooltip"
            ),
            dcc.Input(
                id="max-iterations-input",
                type="number",
                placeholder="250",
                value=250,
                min=1,
                max=2147483647,
                step=1,
                className="form-input"
            ),

            # Terrain Dropdown with Tooltip
            html.Div([
                html.Label("Terrain", className="form-label"),
                html.Img(src="/static/tooltip.png", id="terrain-tooltip")
            ], className="tooltip-container"),
            create_tooltip(
                "Select the terrain type for the simulation. Terrains are loaded from previously created terrain configurations.",
                "terrain-tooltip"
            ),
            dcc.Dropdown(
                id="terrain-dropdown",
                placeholder="Select terrain",
                options=terrain_options,
                className="dropdown-standard",
                multi=True, 
                closeOnSelect=False
            ),
            
            html.Div([
                html.Button("Create Simulation", id="create-simulation-btn", className="btn-primary"),
                html.Button("Clear", id="clear-simulation-btn", className="btn-secondary"),
            ], className="btn-container"),
        ])
        
        return content, "tab-button tab-button-active", "tab-button tab-button-inactive"
    else:
        content = html.Div([
            html.H5("Prevention Configuration", className="prevention-header"),
            html.Label(" Name", className="form-label"),
            dcc.Input(
            id="prevention-name", 
            type="text",
            placeholder="Enter prevention name",
            className="form-input",
            minLength=1,
            maxLength=250,
            pattern="^[a-zA-Z0-9\\s_-]+$",
            ),

            html.H6("Mask Information", className="prevention-section-header"),
            html.Label("Mask Type", className="form-label"),
            
            html.Div([
                html.Div([
                    create_mask_input("N95", "N95", default_value=0.85, is_checked=False),
                    create_mask_input("HOME", "Home/Cloth", default_value=0.0, is_checked=False),
                ], className="mask-row"),
                
                html.Div([
                    create_mask_input("CLOTH", "Cloth", default_value=0.83, is_checked=False),
                    create_mask_input("SURGICAL", "Surgical", default_value=0.85, is_checked=False),
                ], className="mask-row"),
            ], className="mask-container"),

            html.H6("Vaccine Information", className="prevention-section-header-with-margin"),
            html.Div([
                create_vaccine_type("MRNA", "MRNA (Moderna)", default_doses=[0.0, 0.31, 0.88], is_checked=True),
                create_vaccine_type("ASTRA", "ASTRA (AstraZeneca)", default_doses=[0.0, 0.31, 0.67], is_checked=True),
            ], className="vaccine-container"),

              html.Div([
            html.Button("Create Prevention", id="create-prevention-btn", className="btn-primary"), 
            html.Button("Clear", id="clear-prevention-btn", className="btn-secondary"), 
        ], className="btn-container"),
        ])
        
        return content, "tab-button tab-button-inactive", "tab-button tab-button-active"

@callback(
    Output({"type": "mask-slider-container", "mask": MATCH}, "style"),
    Input({"type": "mask-checkbox", "mask": MATCH}, "value"),
)
def toggle_slider_visibility(checkbox_value):
    """Show slider only when checkbox is checked."""
    is_checked = len(checkbox_value) > 0
    return {"display": "block" if is_checked else "none"}

@callback(
    Output({"type": "vaccine-doses-container", "vaccine": MATCH}, "style"),
    Input({"type": "vaccine-checkbox", "vaccine": MATCH}, "value"),
)
def toggle_vaccine_doses_visibility(checkbox_value):
    """Show vaccine dose inputs only when checkbox is checked."""
    is_checked = len(checkbox_value) > 0
    return {"display": "block" if is_checked else "none"}