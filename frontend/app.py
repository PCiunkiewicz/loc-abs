"""Frontend Dash Application."""

from pathlib import Path

import dash
import dash_bootstrap_components as dbc
from dash import Dash, Input, Output, dcc, html
from flask import send_from_directory
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

# Determine exports directory path
docker_exports = Path('/data/exports')
local_exports = Path(__file__).parents[1] / 'backend' / 'data' / 'exports'

if docker_exports.exists():
    EXPORTS_DIR = docker_exports
else:
    EXPORTS_DIR = local_exports
    EXPORTS_DIR.mkdir(parents=True, exist_ok=True)

logger.info(f'Using exports directory: {EXPORTS_DIR}')

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


@app.server.route('/exports/<path:filepath>')
def serve_export(filepath):
    """Serve export files from the exports directory."""
    try:
        full_path = EXPORTS_DIR / filepath
        if not full_path.exists():
            return 'File not found', 404
        return send_from_directory(EXPORTS_DIR, filepath)
    except Exception as exc:
        logger.error(f'Error serving export: {filepath} - {exc}')
        return 'Internal server error', 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8050, debug=True)
