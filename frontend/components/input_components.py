"""Input Components for LocABS Application."""
from dash import html, dcc, callback, Input, Output, MATCH

#import dash_bootstrap_components as dbc

def create_mask_input(mask_type, label,is_disabled, default_value=0.5, is_checked=False):
    """Create a mask input component with label and slider.
    
    Args:
        mask_type (str): The type of mask (e.g., "N95").
        label (str): The label to display next to the checkbox.
        default_value (float): The default effectiveness value for the slider.
        is_checked (bool): Whether the mask checkbox is checked by default.
        is_disabled (bool): Whether the checkbox is disabled.

    Returns:
        html.Div: A Dash HTML Div component representing the mask input.
    """
    return html.Div([
        dcc.Checklist(
            id={"type": "mask-checkbox", "mask": mask_type},
            options=[{"label": f" {label}", "value": mask_type, "disabled": is_disabled}],
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


def create_vaccine_type(vaccine_type, label,is_disabled, default_doses=[0.5, 0.5, 0.5], is_checked=False):
    """Create a vaccine input component.
    
    Args:
        vaccine_type (str): The type of vaccine (e.g., "MRNA").
        label (str): The label to display next to the checkbox.
        is_disabled (bool): Whether the checkbox is disabled.
        default_doses (list): List of default effectiveness values for doses 1, 2, and 3.
        is_checked (bool): Whether the vaccine checkbox is checked by default.

    Returns:
        html.Div: A Dash HTML Div component representing the vaccine input.
    """
    return html.Div([
        dcc.Checklist(
            id={"type": "vaccine-checkbox", "vaccine": vaccine_type},
            options=[{"label": f" {label}", "value": vaccine_type, "disabled": is_disabled}],
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