"""Scenario Builder Page for LocABS Application."""
from dash import html, dcc, register_page, callback, Output, Input, MATCH
import dash 
import dash_daq as daq
#import dash_bootstrap_components as dbc
from components_.tooltip import create_tooltip

#TODO: Add tooltips to various components for better UX

register_page(__name__, path="/scenario-builder", name="Scenario Builder", title="LocABS · Scenario Builder")


def create_config_panel():
    """Create the main configuration panel with tabs."""
    return html.Div(
        [
            # Tab headers
            html.Div(
                [
                    html.Button(
                        "SIMULATIONS",
                        id="tab-simulations",
                        style={
                            "flex": "1",
                            "padding": "12px",
                            "backgroundColor": "#ffffff",
                            "border": "none",
                            "borderRadius": "8px 8px 0 0",
                            "fontWeight": "600",
                            "cursor": "pointer",
                        },
                    ),
                    html.Button(
                        "PREVENTION",
                        id="tab-prevention",
                        style={
                            "flex": "1",
                            "padding": "12px",
                            "backgroundColor": "#e0e0e0",
                            "border": "none",
                            "borderRadius": "8px 8px 0 0",
                            "fontWeight": "600",
                            "cursor": "pointer",
                        },
                    ),
                ],
                style={
                    "display": "flex",
                    "gap": "4px",
                    "marginBottom": "0",
                },
            ),
            
            # Tab content
            html.Div(
                id="tab-content",
                style={
                    "backgroundColor": "#ffffff",
                    "padding": "20px",
                    "borderRadius": "0 0 8px 8px",
                    "minHeight": "500px",
                },
            ),
        ],
        style={
            "flex": "1",
            "marginRight": "16px",
            "width": "22vw"
        },
    )

def create_terrain_form():
    """Create terrain configuration form.

    Returns:
        html.Form: Terrain configuration form.
    """
    return html.Div([
        # Terrain Name
        html.Label ("Name", style={"fontWeight": "600", "marginBottom": "8px"}),
        dcc.Input(
            id="terrain-name",
            type="text",
            placeholder="Enter terrain name",
            style={
                "width": "100%",
                "padding": "10px",
                "marginBottom": "20px",
                "borderRadius": "4px",
                "border": "1px solid #ddd",

            }
        ),

        # Terrain Properties (Checkboxes)   
        
        html.Div([

            html.Div([
                html.Label ("Terrain Type", style={"fontWeight": "600", "marginBottom": "8px"}),
                html.Div([
                    dcc.Checklist(
                        id="terrain-walkable-checkbox",
                        options=[{"label": " Walkable", "value": "walkable"}],
                        value=["walkable"],  # Checked by default
                        inline=True,
                        labelStyle={"marginRight": "20px", "cursor": "pointer"},
                    ),
                    dcc.Checklist(
                        id="terrain-interactive-checkbox",
                        options=[{"label": " Interactive", "value": "interactive"}],
                        value=[],
                        inline=True,
                        labelStyle={"marginRight": "20px", "cursor": "pointer"},
                    ),
                    dcc.Checklist(
                        id="terrain-restricted-checkbox",
                        options=[{"label": " Restricted", "value": "restricted"}],
                        value=[],
                        inline=True,
                        labelStyle={"cursor": "pointer"},
                    ),
                ], style={
                    "display": "flex", 
                    "gap": "20px", 
                    "marginBottom": "20px",
                    "flexDirection": "column",
                    "justify-content": "space-between"
                }),
                    
                # Access Level Selector
                html.Div([
                    html.Label("Access Level", style={"fontWeight": "600", "marginBottom": "8px", "fontSize": "14px"}),
                    html.Div([
                        html.Button(
                            "−",
                            id="terrain-access-decrement",
                            style={
                                "padding": "8px 12px",
                                "border": "1px solid #ddd",
                                "backgroundColor": "#f8f9fa",
                                "cursor": "pointer",
                                "borderRadius": "4px 0 0 4px",
                            },
                        ),
                        dcc.Input(
                            id="terrain-access-input",
                            type="number",
                            value=0,
                            min=0,
                            style={
                                "width": "80%",
                                "padding": "8px",
                                "textAlign": "center",
                                "border": "1px solid #ddd",
                                "borderLeft": "none",
                                "borderRight": "none",
                            },
                        ),
                        html.Button(
                            "+",
                            id="terrain-access-increment",
                            style={
                                "padding": "8px 12px",
                                "border": "1px solid #ddd",
                                "backgroundColor": "#f8f9fa",
                                "cursor": "pointer",
                                "borderRadius": "0 4px 4px 0",
                            },
                        ),
                    ], style={"display": "flex", "alignItems": "center", }),
                ]),
            ], style={
                "display": "flex", 
                # "alignItems": "center", 
                "flexDirection": "column",
                # "justify-content": "space-between"
                }),

            # TODO: FIX CSS FOR THIS:
            # TRY THIS: https://community.plotly.com/t/daq-colorpicker-how-to-remove-a-border-radius/76177/5
            # Color Picker
            html.Div([
                html.Label ("Terrain Color", style={"fontWeight": "600", "margin": "0px"}),
                daq.ColorPicker(
                    id="terrain-color-input",
                    value=dict(hex="#0000FF"),
                    size=150,
                    
                    # theme={"dark": False}, # Apply dark theme
                    style={
                        "borderRadius":"0px", 
                        # "border":"1px solid #ddd",
                        # "padding": "20px"
                    }
                )
                
            ]),

        ], style={
            "marginBottom": "20px", 
            "display": "flex", 
             "gap": "20px", 
            "flexDirection": "row",
            "justify-content": "space-around"
            }),

        

        # Action Buttons
        html.Div([
            html.Button(
                "Create Terrain",
                id="create-terrain-btn",
                className="btn btn-primary",
                style={"marginRight": "10px", "padding": "10px 20px"},
            ),
            html.Button(
                "Clear",
                id="clear-terrain-btn",
                className="btn btn-secondary",
                style={"padding": "10px 20px"},
            ),
        ], style={"marginTop": "20px"}),
    ])


def create_virus_form():
    """Create virus configuration form.

    Returns:
    html.div: Virus configuration form.
    """
    return html.Div([
        # Virus Name
        html.Label("Name", style={"fontWeight": "600", "marginBottom": "8px"}),
        dcc.Input(
            id="virus-name",
            type="text",
            placeholder="Enter virus name",
            style={
                "width": "100%",
                "padding": "10px",
                "marginBottom": "20px",
                "borderRadius": "4px",
                "border": "1px solid #ddd",
            }
        ),

        # Attack Rate
        html.Div([
            html.Label("Attack Rate", style={"fontWeight": "600", "marginBottom": "8px"}),
            dcc.Input(
                            id="virus-attack-rate",
                            type="number",
                            min=0,
                            max=1,
                            step=0.001,
                            value=0.0,
                            placeholder="0.070",
                            style={
                                "flex": "1",
                                "padding": "8px",
                                "textAlign": "center",
                                "border": "1px solid #ddd",
                                "borderRadius": "4px",
                            },
            ),
        ],
        style={
            "display": "flex",
            "flexDirection": "column",
            # "alignItems": "center",
            "gap": "5px",
            "marginBottom": "20px",
        }),

        # Infection Rate
        html.Div([
            html.Label("Infection Rate", style={"fontWeight": "600", "marginBottom": "8px"}),
            dcc.Input(
                            id="virus-infection-rate",
                            type="number",
                            min=0,
                            max=1,
                            step=0.001,
                            value=0.0,
                            placeholder="0.021",
                            style={
                                "flex": "1",
                                "padding": "8px",
                                "textAlign": "center",
                                "border": "1px solid #ddd",
                                "borderRadius": "4px",
                            },
            ),
            ],
        style={
            "display": "flex",
            "flexDirection": "column",
            # "alignItems": "center",
            "gap": "5px",
            "marginBottom": "20px",
        } ),
        
        # Fatality Rate
        html.Div([
            html.Label("Fatality Rate", style={"fontWeight": "600", "marginBottom": "8px"}),
            dcc.Input(
                            id="virus-fatality-rate",
                            type="number",
                            min=0,
                            max=1,
                            step=0.001,
                            value=0.0,
                            placeholder="0.013",
                            style={
                                "flex": "1",
                                "padding": "8px",
                                "textAlign": "center",
                                "border": "1px solid #ddd",
                                "borderRadius": "4px",
                            },
            ),
        ],
        style={
            "display": "flex",
            "flexDirection": "column",
            # "alignItems": "center",
            "gap": "5px",
            "marginBottom": "20px",
        } ),

        

        # Action Buttons
        html.Div([
            html.Button(
                "Create Virus",
                id="create-terrain-btn",
                className="btn btn-primary",
                style={"marginRight": "10px", "padding": "10px 20px"},
            ),
            html.Button(
                "Clear",
                id="clear-terrain-btn",
                className="btn btn-secondary",
                style={"padding": "10px 20px"},
            ),
        ], style={"marginTop": "20px"}),

    ])


def create_agent_config_form():
    """Create agent configuration form.

    Returns:
        html.Div: Agent configuration form.
    """
    return html.Div([

        html.Div(
                "AGENT CONFIGURATION",
                style={
                    "backgroundColor": "#000000",
                    "color": "#ffffff",
                    "padding": "12px",
                    "textAlign": "center",
                    "fontWeight": "600",
                    "fontSize": "14px",
                    "borderRadius": "8px 8px 0 0",
                },
            ),
        
        # Agent Config Name
        html.Label("Name", style={"fontWeight": "600", "marginBottom": "8px"}),
        dcc.Input(
            id="agent-config-name",
            type="text",
            placeholder="Enter agent configuration name",
            style={
                "width": "100%",
                "padding": "10px",
                "marginBottom": "20px",
                "borderRadius": "4px",
                "border": "1px solid #ddd",
            }
        ),

        # Agent Population Section
        html.H6("Agent Population", style={
            "fontWeight": "600", 
            "marginBottom": "16px",
            "borderBottom": "2px solid #000",
            "paddingBottom": "8px"
        }),

        # Random Agents and Random Infected in a row
        html.Div([
            # Random Agents
            html.Div([
                html.Label("Random Agents", style={"fontWeight": "600", "marginBottom": "8px", "fontSize": "14px"}),
                html.Div([
                    html.Button(
                        "−",
                        id="random-agents-decrement",
                        style={
                            "padding": "8px 12px",
                            "border": "1px solid #ddd",
                            "backgroundColor": "#f8f9fa",
                            "cursor": "pointer",
                            "borderRadius": "4px 0 0 4px",
                        },
                    ),
                    dcc.Input(
                        id="random-agents-input",
                        type="number",
                        value=1,
                        min=0,
                        style={
                            "width": "80px",
                            "padding": "8px",
                            "textAlign": "center",
                            "border": "1px solid #ddd",
                            "borderLeft": "none",
                            "borderRight": "none",
                        },
                    ),
                    html.Button(
                        "+",
                        id="random-agents-increment",
                        style={
                            "padding": "8px 12px",
                            "border": "1px solid #ddd",
                            "backgroundColor": "#f8f9fa",
                            "cursor": "pointer",
                            "borderRadius": "0 4px 4px 0",
                        },
                    ),
                ], style={"display": "flex", "alignItems": "center"}),
            ], style={"flex": "1"}),

            # Random Infected
            html.Div([
                html.Label("Random Infected", style={"fontWeight": "600", "marginBottom": "8px", "fontSize": "14px"}),
                html.Div([
                    html.Button(
                        "−",
                        id="random-infected-decrement",
                        style={
                            "padding": "8px 12px",
                            "border": "1px solid #ddd",
                            "backgroundColor": "#f8f9fa",
                            "cursor": "pointer",
                            "borderRadius": "4px 0 0 4px",
                        },
                    ),
                    dcc.Input(
                        id="random-infected-input",
                        type="number",
                        value=0,
                        min=0,
                        style={
                            "width": "80px",
                            "padding": "8px",
                            "textAlign": "center",
                            "border": "1px solid #ddd",
                            "borderLeft": "none",
                            "borderRight": "none",
                        },
                    ),
                    html.Button(
                        "+",
                        id="random-infected-increment",
                        style={
                            "padding": "8px 12px",
                            "border": "1px solid #ddd",
                            "backgroundColor": "#f8f9fa",
                            "cursor": "pointer",
                            "borderRadius": "0 4px 4px 0",
                        },
                    ),
                ], style={"display": "flex", "alignItems": "center"}),
            ], style={"flex": "1"}),
        ], style={
            "display": "flex",
            "gap": "20px",
            "marginBottom": "20px",
        }),

        # Default Agent Configuration Section
        html.H6("Default Agent Configuration", style={
            "fontWeight": "600",
            "marginBottom": "16px",
            "marginTop": "20px",
            "borderBottom": "2px solid #000",
            "paddingBottom": "8px"
        }),

        # Agent Info Section
        html.Div([
            # Mask Type
            html.Div([
                html.Label("Mask Type", style={"fontWeight": "600", "marginBottom": "8px", "fontSize": "14px"}),
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
                    style={"marginBottom": "16px"},
                ),
            ]),

            # Vaccine Type
            html.Div([
                html.Label("Vaccine Type", style={"fontWeight": "600", "marginBottom": "8px", "fontSize": "14px"}),
                dcc.Dropdown(
                    id="agent-vaccine-type",
                    options=[
                        {"label": "None", "value": ""},
                        {"label": "MRNA (Moderna)", "value": "MRNA"},
                        {"label": "ASTRA (AstraZeneca)", "value": "ASTRA"},
                    ],
                    value="",
                    placeholder="Select vaccine type",
                    style={"marginBottom": "16px"},
                ),
            ]),

            # Vaccine Doses
            html.Div([
                html.Label("Vaccine Doses", style={"fontWeight": "600", "marginBottom": "8px", "fontSize": "14px"}),
                html.Div([
                    html.Button(
                        "−",
                        id="vaccine-doses-decrement",
                        style={
                            "padding": "8px 12px",
                            "border": "1px solid #ddd",
                            "backgroundColor": "#f8f9fa",
                            "cursor": "pointer",
                            "borderRadius": "4px 0 0 4px",
                        },
                    ),
                    dcc.Input(
                        id="vaccine-doses-input",
                        type="number",
                        value=0,
                        min=0,
                        max=3,
                        style={
                            "width": "80px",
                            "padding": "8px",
                            "textAlign": "center",
                            "border": "1px solid #ddd",
                            "borderLeft": "none",
                            "borderRight": "none",
                        },
                    ),
                    html.Button(
                        "+",
                        id="vaccine-doses-increment",
                        style={
                            "padding": "8px 12px",
                            "border": "1px solid #ddd",
                            "backgroundColor": "#f8f9fa",
                            "cursor": "pointer",
                            "borderRadius": "0 4px 4px 0",
                        },
                    ),
                ], style={"display": "flex", "alignItems": "center", "marginBottom": "16px"}),
            ]),

            # Work Zone
            html.Div([
                html.Label("Work Zone", style={"fontWeight": "600", "marginBottom": "8px", "fontSize": "14px"}),
                dcc.Dropdown(
                    id="agent-work-zone",
                    options=[
                        {"label": "None", "value": "null"},
                        # TODO: Dynamically populate from created terrains
                    ],
                    value="null",
                    placeholder="Select work zone",
                    style={"marginBottom": "16px"},
                ),
            ]),

            # Start Zone
            html.Div([
                html.Label("Start Zone", style={"fontWeight": "600", "marginBottom": "8px", "fontSize": "14px"}),
                dcc.Dropdown(
                    id="agent-start-zone",
                    options=[
                        {"label": "None", "value": "null"},
                        # TODO: Dynamically populate from created terrains
                    ],
                    value="null",
                    placeholder="Select start zone",
                    style={"marginBottom": "16px"},
                ),
            ]),


        ]),


        # Agent State Section
        html.H6("Initial Agent State", style={
            "fontWeight": "600",
            "marginBottom": "16px",
            "marginTop": "20px",
            "borderBottom": "2px solid #000",
            "paddingBottom": "8px"
        }),

        html.Div([
            # Status
            html.Div([
                html.Label("Status", style={"fontWeight": "600", "marginBottom": "8px", "fontSize": "14px"}),
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
                    style={"marginBottom": "16px"},
                ),
            ]),

            # Position X
            html.Div([
                html.Label("Position X", style={"fontWeight": "600", "marginBottom": "8px", "fontSize": "14px"}),
                dcc.Input(
                    id="agent-position-x",
                    type="number",
                    value=0,
                    style={
                        "width": "100%",
                        "padding": "8px",
                        "border": "1px solid #ddd",
                        "borderRadius": "4px",
                        "marginBottom": "16px",
                    },
                ),
            ]),

            # Position Y
            html.Div([
                html.Label("Position Y", style={"fontWeight": "600", "marginBottom": "8px", "fontSize": "14px"}),
                dcc.Input(
                    id="agent-position-y",
                    type="number",
                    value=0,
                    style={
                        "width": "100%",
                        "padding": "8px",
                        "border": "1px solid #ddd",
                        "borderRadius": "4px",
                        "marginBottom": "16px",
                    },
                ),
            ]),
        ]),

        # Action Buttons
        html.Div([
            html.Button(
                "Create",
                id="create-agent-config-btn",
                className="btn btn-primary",
                style={"marginRight": "10px", "padding": "10px 20px"},
            ),
            html.Button(
                "Clear",
                id="clear-agent-config-btn",
                className="btn btn-secondary",
                style={"padding": "10px 20px"},
            ),
        ], style={"marginTop": "20px"}),

    ], style={
        "backgroundColor": "#ffffff",
        "padding": "30px 100px",
        "width": "100vw",
        "alignItems": "center",
        "minHeight": "500px",
        "borderRadius": "0 0 8px 8px",
    })


def create_side_panel(title, content_id):
    """Create a side panel with title and appropriate content.
    
    Args:
        title (str): The title of the panel.
        content_id (str): The identifier for the content to be displayed.
    
    Returns:
        html.Div: Side panel component.
    """
    # Determine content based on content_id
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
            html.Div(
                title,
                style={
                    "backgroundColor": "#000000",
                    "color": "#ffffff",
                    "padding": "12px",
                    "textAlign": "center",
                    "fontWeight": "600",
                    "fontSize": "14px",
                    "borderRadius": "8px 8px 0 0",
                },
            ),
            html.Div(
                panel_content,
                style={
                    "backgroundColor": "#ffffff",
                    "padding": "20px",
                    "minHeight": "500px",
                    "borderRadius": "0 0 8px 8px",
                },
            ),
        ],
        style={
            "marginBottom": "16px",
            "width": "50vw",
        },
    )

def create_mask_input(mask_type, label, default_value=0.5, is_checked=False):
    """Create a mask input component with label and slider.

    Args:
        mask_type (str): The value identifier for the mask (e.g., "N95", "HOME") 
        label (str): Label for the mask input.
        default_value (float): Default effectiveness value (0-1 scale).
        is_checked (bool): Whether the checkbox is checked by default.

    Returns:
        html.Div: Mask input component.
    """
    return html.Div([
        dcc.Checklist(
            id={"type": "mask-checkbox", "mask": mask_type},
            options=[{"label": f" {label}", "value": mask_type}],
            value=[mask_type] if is_checked else [],
            inline=True,
            labelStyle={"marginRight": "10px", "cursor": "pointer", "minWidth": "100px"},
        ),
        html.Div(
            dcc.Slider(
                id={"type": "mask-effectiveness-slider", "mask": mask_type},
                min=0,
                max=1,
                step=0.01,
                value=default_value,
                marks={0: "0%", 0.5: "50%", 1: "100%"},
                tooltip={"placement": "bottom", "always_visible": True},
                className="mask-slider mt-3"
            ),
            id={"type": "mask-slider-container", "mask": mask_type},
            style={"flex": "1", "display": "block" if is_checked else "none"},
        ),
    ], style={
        "display": "flex",
        "flexDirection": "column",  # Stack checkbox and slider vertically
        "flex": "1",  # Each item takes equal width in the row
        "minWidth": "0",  # Prevent overflow
    })

def create_vaccine_type(vaccine_type, label, default_doses=[0.5, 0.5, 0.5], is_checked=False):
    """Create a vaccine input component with label and slider.
    
    Args:
        vaccine_type (str): The value identifier for the vaccine (e.g., "PFIZER", "MODERNA") 
        label (str): Label for the vaccine input.
        default_doses (list): List of 3 default effectiveness values for doses 1, 2, and 3 (0-1 scale).
        is_checked (bool): Whether the checkbox is checked by default.
    
    Returns:
        html.Div: Vaccine input component.
    """
    return html.Div([
        # Vaccine checkbox
        dcc.Checklist(
            id={"type": "vaccine-checkbox", "vaccine": vaccine_type},
            options=[{"label": f" {label}", "value": vaccine_type}],
            value=[vaccine_type] if is_checked else [],
            inline=True,
            labelStyle={"cursor": "pointer", "fontWeight": "600", "marginBottom": "8px"},
        ),

        html.Label("Effectiveness", style={"fontWeight": "600", "marginBottom": "8px"}),
        
        # Dose effectiveness inputs container (hidden if unchecked)
        html.Div(
            [
                # Table header
                html.Div([
                    html.Div("Dose 1", style={"flex": "1", "textAlign": "center", "fontWeight": "600", "fontSize": "12px", "color": "#666"}),
                    html.Div("Dose 2", style={"flex": "1", "textAlign": "center", "fontWeight": "600", "fontSize": "12px", "color": "#666"}),
                    html.Div("Dose 3", style={"flex": "1", "textAlign": "center", "fontWeight": "600", "fontSize": "12px", "color": "#666"}),
                ], style={"display": "flex", "gap": "10px", "marginBottom": "8px"}),
                
                # Dose input fields
                html.Div([
                    # Dose 1
                    dcc.Input(
                        id={"type": "vaccine-dose", "vaccine": vaccine_type, "dose": 1},
                        type="number",
                        min=0,
                        max=1,
                        step=0.01,
                        value=default_doses[0],
                        placeholder="0.00",
                        style={
                            "flex": "1",
                            "padding": "8px",
                            "textAlign": "center",
                            "border": "1px solid #ddd",
                            "borderRadius": "4px",
                        },
                    ),
                    # Dose 2
                    dcc.Input(
                        id={"type": "vaccine-dose", "vaccine": vaccine_type, "dose": 2},
                        type="number",
                        min=0,
                        max=1,
                        step=0.01,
                        value=default_doses[1],
                        placeholder="0.00",
                        style={
                            "flex": "1",
                            "padding": "8px",
                            "textAlign": "center",
                            "border": "1px solid #ddd",
                            "borderRadius": "4px",
                        },
                    ),
                    # Dose 3
                    dcc.Input(
                        id={"type": "vaccine-dose", "vaccine": vaccine_type, "dose": 3},
                        type="number",
                        min=0,
                        max=1,
                        step=0.01,
                        value=default_doses[2],
                        placeholder="0.00",
                        style={
                            "flex": "1",
                            "padding": "8px",
                            "textAlign": "center",
                            "border": "1px solid #ddd",
                            "borderRadius": "4px",
                        },
                    ),
                ], style={"display": "flex", "gap": "10px"}),
            ],
            id={"type": "vaccine-doses-container", "vaccine": vaccine_type},
            style={"display": "block" if is_checked else "none", "marginTop": "8px"},
        ),
    ], style={
        "padding": "12px",
        "border": "1px solid #e0e0e0",
        "borderRadius": "4px",
        "margin": "10px 12px 0px 0px",
        "backgroundColor": "#fafafa",
    })



# Layout
layout = html.Div(
    [
        # Main container
        html.Div(
            [
                # Left panel - Side components
                html.Div(
                    [
                        create_side_panel("TERRAINS", "terrain-content"),
                        create_side_panel("VIRUS", "virus-content"),
                    ],
                    style={
                        "width":"50vw",
                        "display": "flex",
                        "flexDirection": "row",
                        "gap": "16px",
                    },
                ),

                # Right panel - Configuration
                create_config_panel(),
            ],
            style={
                "display": "flex",
                "gap": "16px",
                "padding": "30px",
                "margin": "0",
                
            },
        ),
        
        html.Div(
            [
                create_agent_config_form(),
            ]
        ),
    ],
    style={
        "backgroundColor": "#f5f5f5",
        "minHeight": "calc(100vh - 200px)",
        "paddingBottom": "100px",
    },
)


# Callbacks for tab switching
@callback(
    [
        Output("tab-content", "children"),
        Output("tab-simulations", "style"),
        Output("tab-prevention", "style"),
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
        sim_clicks (int): Number of clicks on the simulations tab.
        prev_clicks (int): Number of clicks on the prevention tab.
    
    Returns:
        tuple: Updated tab content and styles.
    """
    ctx = dash.callback_context
    
    # Default to simulations tab
    active_tab = "simulations"
    
    if ctx.triggered:
        button_id = ctx.triggered[0]["prop_id"].split(".")[0]
        if button_id == "tab-prevention":
            active_tab = "prevention"
    
    # Tab content
    if active_tab == "simulations":
        content = html.Div(
            [
                html.H5("Simulation Configuration", style={"marginBottom": "20px"}),
                
                # Simulations Name
                html.Label(" Name", style={"fontWeight": "600", "marginBottom": "8px"}),
                dcc.Input(
                    type="text",
                    placeholder="Enter simulation name",
                    style={
                        "width": "100%",
                        "padding": "10px",
                        "marginBottom": "20px",
                        "borderRadius": "4px",
                        "border": "1px solid #ddd",
                    },
                ),
                
                # Map File
                # TODO: Integrate dynamic map file options
                # Connect the dropdown to the backend so that newly added map files are automatically reflected in the available selection list.
                html.Div(
                    [
                        html.Label("Map File", style={"fontWeight": "600", "marginBottom": "8px"}),
                        html.Img(src="/static/tooltip.png", id="map-file")
                    ],
                    style={
                        "display": "flex",
                        "alignItems": "center",
                        "justifyContent": "space-between",
                        "marginBottom": "8px",
                    }
                ),
                create_tooltip("Select the map file that defines the terrain and environment for the simulation. Available maps include various layouts and geographical features.", "map-file"),
                dcc.Dropdown(
                    options=[
                        {"label": "Bow View Manor", "value": "bow_view_manor"},
                        
                    ],
                    placeholder="Select map file",
                    style={"marginBottom": "20px"},
                ),
                
                # X-Y Scale
                html.Div(
                    [
                        html.Label("Plot Scale", style={"fontWeight": "600", "marginBottom": "8px"}),
                        html.Img(src="/static/tooltip.png", id="xy-scale")
                    ],
                    style={
                        "display": "flex",
                        "alignItems": "center",
                        "justifyContent": "space-between",
                        "marginBottom": "8px",
                    }
                ),
                create_tooltip("Defines the scale for the X and Y axes on the simulation plot. Adjusting this value changes how distances are represented visually.", "xy-scale"),
                dcc.Input(
                    type="number",
                    placeholder="2.77",
                    style={
                        "width": "100%",
                        "padding": "10px",
                        "marginBottom": "20px",
                        "borderRadius": "4px",
                        "border": "1px solid #ddd",
                    },
                ),

                # TODO: Ask if this should be a dropdown menu with time options or manual input
                # Time Step
                html.Div(
                    [
                        html.Label("Time Step (s)", style={"fontWeight": "600", "marginBottom": "8px"}),
                        html.Img(src="/static/tooltip.png", id="time-step")
                    ],
                    style={
                        "display": "flex",
                        "alignItems": "center",
                        "justifyContent": "space-between",
                        "marginBottom": "8px",
                    }
                ),
                create_tooltip("Defines the duration of each simulation step in seconds. Smaller values yield finer temporal resolution.", "time-step"),
                dcc.Input(
                    type="number",
                    placeholder="5",
                    style={
                        "width": "100%",
                        "padding": "10px",
                        "marginBottom": "20px",
                        "borderRadius": "4px",
                        "border": "1px solid #ddd",
                    },
                ),

                # Save Resolution
                html.Div(
                    [
                        html.Label("Save Resolution", style={"fontWeight": "600", "marginBottom": "8px"}),
                        html.Img(src="/static/tooltip.png", id="save-resolution")
                    ],
                    style={
                        "display": "flex",
                        "alignItems": "center",
                        "justifyContent": "space-between",
                        "marginBottom": "8px",
                    }
                ),
                create_tooltip("Number of time steps per iteration. Determines how frequently simulation data is recorded.", "save-resolution"),
                dcc.Input(
                    type="number",
                    placeholder="12",
                    style={
                        "width": "100%",
                        "padding": "10px",
                        "marginBottom": "20px",
                        "borderRadius": "4px",
                        "border": "1px solid #ddd",
                    },
                ),
                
                # Maximum Iterations
                html.Div(
                    [
                        html.Label("Max Iterations", style={"fontWeight": "600", "marginBottom": "8px"}),
                        html.Img(src="/static/tooltip.png", id="max-iterations")
                    ],
                    style={
                        "display": "flex",
                        "alignItems": "center",
                        "justifyContent": "space-between",
                        "marginBottom": "8px",
                    }
                ),
                create_tooltip("Total number of iterations to run the simulation. Controls the overall simulation length.", "max-iterations"),
                dcc.Input(
                    type="number",
                    placeholder="250",
                    style={
                        "width": "100%",
                        "padding": "10px",
                        "marginBottom": "20px",
                        "borderRadius": "4px",
                        "border": "1px solid #ddd",
                    },
                ),

                # Terrains
                # TODO: Integrate dynamic terrain options 
                # Connect 
                html.Div(
                    [
                        html.Label("Terrain", style={"fontWeight": "600", "marginBottom": "8px"}),
                        html.Img(src="/static/tooltip.png", id="terrain")
                    ],
                    style={
                        "display": "flex",
                        "alignItems": "center",
                        "justifyContent": "space-between",
                        "marginBottom": "8px",
                    }
                    
                ),
                create_tooltip("Select the terrain type for the simulation. Different terrains can affect the spread of disease and the effectiveness of interventions.", "terrain"),
                dcc.Dropdown(
                    options=[
                        {"label": "Bow View Manor", "value": "bow_view_manor"},
                        
                    ],
                    placeholder="Select map file",
                    style={"marginBottom": "20px"},
                ),
                
                # Action buttons
                html.Div(
                    [
                        html.Button(
                            "Create Simulation",
                            className="btn btn-primary",
                            style={"marginRight": "10px", "padding": "10px 20px"},
                        ),
                        html.Button(
                            "Update Values",
                            className="btn btn-primary",
                            style={"marginRight": "10px","padding": "10px 20px"},
                        ),
                        html.Button(
                            "Delete Simulation",
                            className="btn btn-danger",
                            style={"padding": "10px 20px"},
                        ),
                    ],
                    style={"marginTop": "20px"},
                ),
            ]
        )
        
        sim_style = {
            "flex": "1",
            "padding": "12px",
            "backgroundColor": "#ffffff",
            "border": "none",
            "borderRadius": "8px 8px 0 0",
            "fontWeight": "600",
            "cursor": "pointer",
        }
        prev_style = {
            "flex": "1",
            "padding": "12px",
            "backgroundColor": "#e0e0e0",
            "border": "none",
            "borderRadius": "8px 8px 0 0",
            "fontWeight": "600",
            "cursor": "pointer",
        }
    else:
        content = html.Div(
            [
                html.H5("Prevention Configuration", style={"marginBottom": "20px"}),
                
                # Prevention Name
                html.Label(" Name", style={"fontWeight": "600", "marginBottom": "8px"}),
                dcc.Input(
                    type="text",
                    placeholder="Enter prevention name",
                    style={
                        "width": "100%",
                        "padding": "10px",
                        "marginBottom": "20px",
                        "borderRadius": "4px",
                        "border": "1px solid #ddd",
                    },
                ),

                # Mask Information
                html.H6("Mask Information", style={
                    "fontWeight": "600", 
                    "marginBottom": "20px",
                    "borderBottom": "2px solid #000",
                    "paddingBottom": "8px",
                }),
                html.Label("Mask Type", style={"fontWeight": "600", "marginBottom": "8px"}),
                # Mask type inputs using the reusable function
                html.Div([
                    # First row
                    html.Div([
                        create_mask_input("N95", "N95", default_value=0.85, is_checked=False),
                        create_mask_input("HOME", "Home/Cloth", default_value=0.0, is_checked=False),
                    ], style={
                        "display": "flex",
                        "gap": "20px",
                        "marginBottom": "12px",
                    }),
                    
                    # Second row
                    html.Div([
                        create_mask_input("CLOTH", "Cloth", default_value=0.83, is_checked=False),
                        create_mask_input("SURGICAL", "Surgical", default_value=0.85, is_checked=False),
                    ], style={
                        "display": "flex",
                        "gap": "20px",
                        "marginBottom": "12px",
                    }),
                ], style={
                    "marginBottom": "20px",
                    "width": "100%"
                }),

                # TODO: Add functionality to the buttons
                html.Div(
                [
                    html.Button(
                        "Create",
                        id="create-prevention-btn",
                        className="btn btn-primary",
                        style={"marginRight": "10px", "padding": "10px 20px"},
                    ),
                    html.Button(
                        "Clear",
                        id="clear-prevention-btn",
                        className="btn btn-secondary",
                        style={"padding": "10px 20px"},
                    ),
                ],
                style={"marginTop": "30px"},
                 ),

                
                # Vaccine Information
                html.H6("Vaccine Information", style={
                    "fontWeight": "600", 
                    "margin": "20px 20px 0px 0px",
                    "borderBottom": "2px solid #000",
                    "paddingBottom": "8px",}),
                # Vaccine type inputs using the reusable function
                html.Div([
                    create_vaccine_type("MRNA", "MRNA (Moderna)", default_doses=[0.0, 0.31, 0.88], is_checked=True),
                    create_vaccine_type("ASTRA", "ASTRA (AstraZeneca)", default_doses=[0.0, 0.31, 0.67], is_checked=True),
                ], style={"marginBottom": "20px"}),

                # Action buttons
                html.Div(
                    [
                        html.Button(
                            "Add Prevention",
                            className="btn btn-primary",
                            style={"marginRight": "10px", "padding": "10px 20px"},
                        ),
                        html.Button(
                            "Update Prevention",
                            className="btn btn-secondary",
                            style={"marginRight": "10px", "padding": "10px 20px"},
                        ),
                        html.Button(
                            "Clear",
                            className="btn btn-secondary",
                            style={"padding": "10px 20px"},
                        ),
                    ],
                    style={"marginTop": "20px"},
                ),
            ]
        )
        
        sim_style = {
            "flex": "1",
            "padding": "12px",
            "backgroundColor": "#e0e0e0",
            "border": "none",
            "borderRadius": "8px 8px 0 0",
            "fontWeight": "600",
            "cursor": "pointer",
        }
        prev_style = {
            "flex": "1",
            "padding": "12px",
            "backgroundColor": "#ffffff",
            "border": "none",
            "borderRadius": "8px 8px 0 0",
            "fontWeight": "600",
            "cursor": "pointer",
        }
    
    return content, sim_style, prev_style


# TODO: Ask Philip about toggling visibility of the sliders and dose inputs
@callback(
    Output({"type": "mask-slider-container", "mask": MATCH}, "style"),
    Input({"type": "mask-checkbox", "mask": MATCH}, "value"),
)

def toggle_slider_visibility(checkbox_value):
    """Show slider only when checkbox is checked.
    
    Args:
        checkbox_value (list): List of selected values from the checklist.
    
    Returns:
        dict: Style dict to show/hide the slider container.
    """
    is_checked = len(checkbox_value) > 0
    return {
        "flex": "1",
        "display": "block" if is_checked else "none"
    }

@callback(
    Output({"type": "vaccine-doses-container", "vaccine": MATCH}, "style"),
    Input({"type": "vaccine-checkbox", "vaccine": MATCH}, "value"),
)
def toggle_vaccine_doses_visibility(checkbox_value):
    """Show vaccine dose inputs only when checkbox is checked.
    
    Args:
        checkbox_value (list): List of selected values from the checklist.
        
    Returns:
        dict: Style dict to show/hide the vaccine doses container.
    """
    is_checked = len(checkbox_value) > 0
    return {
        "display": "block" if is_checked else "none",
        "marginTop": "8px"
    }


# TODO: Create callback to collect vaccine data and mask data when creating a prevention instance - JSON format