""""Bottom navigation component for the Dash app."""
from dash import html, dcc


# TODO: Make the bottom nav collapsible and expansion on hover or click

def create_bottom_nav():
    """Create a fixed bottom navigation bar."""
    nav_item_style = {
        "display": "flex",
        "flexDirection": "column",
        "alignItems": "center",
        "justifyContent": "center",
        "color": "white",
        "textDecoration": "none",
        "fontSize": "12px",
        "fontWeight": "500",
        "cursor": "pointer",
        "padding": "8px 16px",
        "flex": "1",
    }

    icon_style = {
        "fontSize": "24px",
        "marginBottom": "4px",
    }


    return html.Div(
        [
            # Home Item
            dcc.Link(
                [
                    html.Img(src="/static/home.png", style=icon_style),
                    html.Span("Home"),
                ],
                href="/",
                style=nav_item_style,   
            ),

            # Visualise Item
            dcc.Link(
                [
                    html.Img(src="/static/viz.png", style=icon_style),
                    html.Span("Visualise"),
                ],
                href="/data-viz",
                style=nav_item_style,
            ),

            # Reports Item
            dcc.Link(
                [
                    html.Img(src="/static/reports.png", style=icon_style),
                    html.Span("Reports"),
                ],
                href="/reports",
                style=nav_item_style,
            ),

            # Help Item
            dcc.Link(
                [
                    html.Img(src="/static/help.png", style=icon_style),
                    html.Span("Help"),
                ],
                href="/help",
                style=nav_item_style,
            ),
        ],
        style={
            "position": "fixed",
            "bottom": "30px",
            # "left": "37vw",
            "right": "0",
            "backgroundColor": "#000000",
            "display": "flex",
            "flexDirection": "row",
            "justifyContent": "space-around",
            "alignItems": "center",
            "height": "70px",
            "borderRadius": "35px",
            "width": "500px",
            "zIndex": "1000",
            "boxShadow": "0 -2px 10px rgba(0,0,0,0.1)",
        },
    )