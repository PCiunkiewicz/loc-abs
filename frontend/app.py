"""Frontend Dash Application."""

import dash
import dash_bootstrap_components as dbc
from dash import Dash, html
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

header = header.create_header()

footer = footer.create_footer()

bottom_nav = bottom_nav.create_bottom_nav()

app.layout = html.Div(
    [header, dash.page_container, footer, bottom_nav],
    className='app-container',
    style={'minHeight': '100vh', 'backgroundColor': '#f5f5f5'},
)


if __name__ == '__main__':
    logger.debug('Registered pages/routes:')
    for p in dash.page_registry.values():
        logger.debug(f'- {p['name']} -> {p['path']}')
    app.run(host='0.0.0.0', port=8050, debug=True)
