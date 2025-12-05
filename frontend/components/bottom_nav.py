"""Bottom navigation component for the Dash app."""

from dash import dcc, html

# TODO: Make the bottom nav collapsible and expansion on hover or click


def create_bottom_nav() -> html.Div:
    """Create a fixed bottom navigation bar."""
    nav_item_style = {
        'display': 'flex',
        'flexDirection': 'column',
        'alignItems': 'center',
        'justifyContent': 'center',
        'color': 'white',
        'textDecoration': 'none',
        'fontSize': '12px',
        'fontWeight': '500',
        'cursor': 'pointer',
        'padding': '8px 16px',
        'flex': '1',
    }

    icon_style = {
        'fontSize': '24px',
        'marginBottom': '4px',
    }

    return html.Div(
        [
            dcc.Link(
                [html.I(className='fa fa-house', style=icon_style), 'Home'],
                href='/',
                style=nav_item_style,
            ),
            dcc.Link(
                [html.I(className='fa fa-chart-column', style=icon_style), 'Visualise'],
                href='/data-viz',
                style=nav_item_style,
            ),
            dcc.Link(
                [html.I(className='fa fa-file-lines', style=icon_style), 'Reports'],
                href='/reports',
                style=nav_item_style,
            ),
            dcc.Link(
                [html.I(className='fa fa-circle-question', style=icon_style), 'Help'],
                href='/help',
                style=nav_item_style,
            ),
        ],
        style={
            'position': 'fixed',
            'bottom': '30px',
            # "left": "37vw",
            'right': '0',
            'backgroundColor': '#000000',
            'display': 'flex',
            'flexDirection': 'row',
            'justifyContent': 'space-around',
            'alignItems': 'center',
            'height': '70px',
            'borderRadius': '35px',
            'width': '500px',
            'zIndex': '1000',
            'boxShadow': '0 -2px 10px rgba(0,0,0,0.1)',
        },
    )
