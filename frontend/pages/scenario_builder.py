"""Scenario Builder Page for LocABS Application."""
from dash import html, dcc, register_page, callback, Output, Input, MATCH
import dash 
import dash_daq as daq
from components_.tooltip import create_tooltip

register_page(__name__, path="/scenario-builder", name="Scenario Builder", title="LocABS · Scenario Builder")


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
        # Terrain Name
        html.Label("Name", className="form-label"),
        dcc.Input(id="terrain-name", type="text", placeholder="Enter terrain name", className="form-input"),

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
                    html.Div([
                        html.Button("−", id="terrain-access-decrement", className="counter-button counter-button-decrement"),
                        dcc.Input(id="terrain-access-input", type="number", value=0, min=0, className="form-input-number-narrow"),
                        html.Button("+", id="terrain-access-increment", className="counter-button counter-button-increment"),
                    ], className="counter-container"),
                ]),
            ], className="terrain-properties-column"),

            # Color Picker
            html.Div([
                html.Label("Terrain Color", className="form-label"),
                daq.ColorPicker(id="terrain-color-input", value=dict(hex="#0000FF"), size=150)
            ]),

        ], className="terrain-properties-row"),

        # Action Buttons
        html.Div([
            html.Button("Create Terrain", id="create-terrain-btn", className="btn-primary"),
            html.Button("Clear", id="clear-terrain-btn", className="btn-secondary"),
        ], className="btn-container"),
    ])


def create_virus_form():
    """Create virus configuration form."""
    return html.Div([
        # Virus Name
        html.Label("Name", className="form-label"),
        dcc.Input(id="virus-name", type="text", placeholder="Enter virus name", className="form-input"),

        # Attack Rate
        html.Div([
            html.Label("Attack Rate", className="form-label"),
            dcc.Input(id="virus-attack-rate", type="number", min=0, max=1, step=0.001,
                     value=0.0, placeholder="0.070", className="virus-rate-input"),
        ], className="virus-rate-container"),

        # Infection Rate
        html.Div([
            html.Label("Infection Rate", className="form-label"),
            dcc.Input(id="virus-infection-rate", type="number", min=0, max=1, step=0.001,
                     value=0.0, placeholder="0.021", className="virus-rate-input"),
        ], className="virus-rate-container"),
        
        # Fatality Rate
        html.Div([
            html.Label("Fatality Rate", className="form-label"),
            dcc.Input(id="virus-fatality-rate", type="number", min=0, max=1, step=0.001,
                     value=0.0, placeholder="0.013", className="virus-rate-input"),
        ], className="virus-rate-container"),

        # Action Buttons
        html.Div([
            html.Button("Create Virus", id="create-terrain-btn", className="btn-primary"),
            html.Button("Clear", id="clear-terrain-btn", className="btn-secondary"),
        ], className="btn-container"),
    ])


def create_agent_config_form():
    """Create agent configuration form."""
    return html.Div([
        html.Div("AGENT CONFIGURATION", className="agent-config-header"),
        
        # Agent Config Name
        html.Label("Name", className="form-label"),
        dcc.Input(id="agent-config-name", type="text", placeholder="Enter agent configuration name", className="form-input"),

        # Agent Population Section
        html.H6("Agent Population", className="section-header"),

        # Random Agents and Random Infected
        html.Div([
            # Random Agents
            html.Div([
                html.Label("Random Agents", className="form-label-small"),
                html.Div([
                    html.Button("−", id="random-agents-decrement", className="counter-button counter-button-decrement"),
                    dcc.Input(id="random-agents-input", type="number", value=1, min=0, className="form-input-number-narrow"),
                    html.Button("+", id="random-agents-increment", className="counter-button counter-button-increment"),
                ], className="counter-container"),
            ], className="agent-population-item"),

            # Random Infected
            html.Div([
                html.Label("Random Infected", className="form-label-small"),
                html.Div([
                    html.Button("−", id="random-infected-decrement", className="counter-button counter-button-decrement"),
                    dcc.Input(id="random-infected-input", type="number", value=0, min=0, className="form-input-number-narrow"),
                    html.Button("+", id="random-infected-increment", className="counter-button counter-button-increment"),
                ], className="counter-container"),
            ], className="agent-population-item"),
        ], className="agent-population-row"),

        # Default Agent Configuration Section
        html.H6("Default Agent Configuration", className="section-header-with-margin"),

        # Mask Type
        html.Div([
            html.Label("Mask Type", className="form-label-small"),
            dcc.Dropdown(
                id="agent-mask-type",
                options=[
                    {"label": "None", "value": ""},
                    {"label": "N95", "value": "N95"},
                    {"label": "Surgical", "value": "SURGICAL"},
                    {"label": "Cloth", "value": "CLOTH"},
                    {"label": "Home/Cloth", "value": "HOME"},
                ],
                value="",
                placeholder="Select mask type",
                className="dropdown-with-margin",
            ),
        ]),

        # Vaccine Type
        html.Div([
            html.Label("Vaccine Type", className="form-label-small"),
            dcc.Dropdown(
                id="agent-vaccine-type",
                options=[
                    {"label": "None", "value": ""},
                    {"label": "MRNA (Moderna)", "value": "MRNA"},
                    {"label": "ASTRA (AstraZeneca)", "value": "ASTRA"},
                ],
                value="",
                placeholder="Select vaccine type",
                className="dropdown-with-margin",
            ),
        ]),

        # Vaccine Doses
        html.Div([
            html.Label("Vaccine Doses", className="form-label-small"),
            html.Div([
                html.Button("−", id="vaccine-doses-decrement", className="counter-button counter-button-decrement"),
                dcc.Input(id="vaccine-doses-input", type="number", value=0, min=0, max=3, className="form-input-number-narrow"),
                html.Button("+", id="vaccine-doses-increment", className="counter-button counter-button-increment"),
            ], className="counter-container"),
        ]),

        # Work Zone
        html.Div([
            html.Label("Work Zone", className="form-label-small"),
            dcc.Dropdown(
                id="agent-work-zone",
                options=[{"label": "None", "value": "null"}],
                value="null",
                placeholder="Select work zone",
                className="dropdown-with-margin",
            ),
        ]),

        # Start Zone
        html.Div([
            html.Label("Start Zone", className="form-label-small"),
            dcc.Dropdown(
                id="agent-start-zone",
                options=[{"label": "None", "value": "null"}],
                value="null",
                placeholder="Select start zone",
                className="dropdown-with-margin",
            ),
        ]),

        # Agent State Section
        html.H6("Initial Agent State", className="section-header-with-margin"),

        html.Div([
            # Status
            html.Div([
                html.Label("Status", className="form-label-small"),
                dcc.Dropdown(
                    id="agent-status",
                    options=[
                        {"label": "Unknown", "value": "UNKNOWN"},
                        {"label": "Susceptible", "value": "SUSCEPTIBLE"},
                        {"label": "Infected", "value": "INFECTED"},
                        {"label": "Recovered", "value": "RECOVERED"},
                        {"label": "Dead", "value": "DEAD"},
                    ],
                    value="UNKNOWN",
                    className="dropdown-with-margin",
                ),
            ]),

            # Position X
            html.Div([
                html.Label("Position X", className="form-label-small"),
                dcc.Input(id="agent-position-x", type="number", value=0, className="agent-full-width-input"),
            ]),

            # Position Y
            html.Div([
                html.Label("Position Y", className="form-label-small"),
                dcc.Input(id="agent-position-y", type="number", value=0, className="agent-full-width-input"),
            ]),
        ]),

        # Action Buttons
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
    """Create a vaccine input component."""
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
                        html.Div(
                            [
                                create_side_panel("TERRAINS", "terrain-content"),
                                create_side_panel("VIRUS", "virus-content"),
                            ],
                            className="side-panels-container",
                        ),
                    ],
                    className="side-panels-wrapper",
                ),
                create_config_panel(),
            ],
            className="main-container",
        ),
        
        html.Div([create_agent_config_form()]),
    ],
    className="scenario-builder-page",
)


# Callbacks
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
    """Switch between Simulations and Prevention tabs."""
    ctx = dash.callback_context
    active_tab = "simulations"
    
    if ctx.triggered:
        button_id = ctx.triggered[0]["prop_id"].split(".")[0]
        if button_id == "tab-prevention":
            active_tab = "prevention"
    
    if active_tab == "simulations":
        content = html.Div([
            html.H5("Simulation Configuration", className="simulation-header"),
            
            html.Div([
                html.Label("Map File", className="form-label"),
                html.Img(src="/static/tooltip.png", id="map-file")
            ], className="tooltip-container"),
            create_tooltip("Select the map file that defines the terrain and environment for the simulation.", "map-file"),
            dcc.Dropdown(
                options=[{"label": "Bow View Manor", "value": "bow_view_manor"}],
                placeholder="Select map file",
                className="dropdown-standard",
            ),
            
            html.Div([
                html.Label("Plot Scale", className="form-label"),
                html.Img(src="/static/tooltip.png", id="xy-scale")
            ], className="tooltip-container"),
            create_tooltip("Defines the scale for the X and Y axes on the simulation plot.", "xy-scale"),
            dcc.Input(type="number", placeholder="2.77", className="form-input"),

            html.Div([
                html.Label("Time Step (s)", className="form-label"),
                html.Img(src="/static/tooltip.png", id="time-step")
            ], className="tooltip-container"),
            create_tooltip("Defines the duration of each simulation step in seconds.", "time-step"),
            dcc.Input(type="number", placeholder="5", className="form-input"),

            html.Div([
                html.Label("Save Resolution", className="form-label"),
                html.Img(src="/static/tooltip.png", id="save-resolution")
            ], className="tooltip-container"),
            create_tooltip("Number of time steps per iteration.", "save-resolution"),
            dcc.Input(type="number", placeholder="12", className="form-input"),
            
            html.Div([
                html.Label("Max Iterations", className="form-label"),
                html.Img(src="/static/tooltip.png", id="max-iterations")
            ], className="tooltip-container"),
            create_tooltip("Total number of iterations to run the simulation.", "max-iterations"),
            dcc.Input(type="number", placeholder="250", className="form-input"),

            html.Div([
                html.Label("Terrain", className="form-label"),
                html.Img(src="/static/tooltip.png", id="terrain")
            ], className="tooltip-container"),
            create_tooltip("Select the terrain type for the simulation.", "terrain"),
            dcc.Dropdown(
                options=[{"label": "Bow View Manor", "value": "bow_view_manor"}],
                placeholder="Select map file",
                className="dropdown-standard",
            ),
            
            html.Div([
                html.Button("Create Simulation", className="btn-primary"),
                html.Button("Update Values", className="btn-primary"),
                html.Button("Delete Simulation", className="btn-danger"),
            ], className="btn-container"),
        ])
        
        return content, "tab-button tab-button-active", "tab-button tab-button-inactive"
    
    else:
        content = html.Div([
            html.H5("Prevention Configuration", className="prevention-header"),
            
            html.Label(" Name", className="form-label"),
            dcc.Input(type="text", placeholder="Enter prevention name", className="form-input"),

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
                html.Button("Add Prevention", className="btn-primary"),
                html.Button("Update Prevention", className="btn-secondary"),
                html.Button("Clear", className="btn-secondary"),
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