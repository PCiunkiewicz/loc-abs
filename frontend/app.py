"""Frontend Dash Application."""

import dash
import dash_bootstrap_components as dbc
from dash import Dash, html, dcc, Input, Output
from loguru import logger

from components import bottom_nav, footer, header
from utilities.logging import configure_logger

configure_logger(level='DEBUG')

app = Dash(
    __name__,
    use_pages=True,
    external_stylesheets=[dbc.themes.LUX, dbc.icons.FONT_AWESOME],
    suppress_callback_exceptions=True,
)

footer = footer.create_footer()

bottom_nav = bottom_nav.create_bottom_nav()

app.layout = html.Div(
    [
        dcc.Location(id='url', refresh=False),
        html.Div(id='header-container'),
        dash.page_container,
        footer,
        bottom_nav,
    ],
    className='app-container',
    style={'minHeight': '100vh', 'backgroundColor': '#f5f5f5'},
)


@app.callback(Output('header-container', 'children'), Input('url', 'pathname'))
def update_header(pathname):
    """Update header based on current pathname."""
    return header.create_header(pathname=pathname or '/')


if __name__ == '__main__':
    logger.debug('Registered pages/routes:')
    for p in dash.page_registry.values():
        logger.debug(f'- {p["name"]} -> {p["path"]}')
    app.run(host='0.0.0.0', port=8050, debug=True)
