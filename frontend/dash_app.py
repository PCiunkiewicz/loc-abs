"""Frontend Dash Application."""
from dash import Dash, html
import dash
import dash_bootstrap_components as dbc
import components_.header as header
import components_.footer as footer
from utilities.logging import configure_logger
from loguru import logger

configure_logger(level="DEBUG")

app = Dash(__name__, use_pages= True, external_stylesheets=[dbc.themes.LUX])

header = header.create_header()

footer = footer.create_footer()

app.layout = html.Div([
    header,
    dash.page_container,
    footer
])


if __name__ == '__main__':
    logger.debug("Registered pages/routes:")
    for p in dash.page_registry.values():
        logger.debug(f"- {p['name']} -> {p['path']}")
    app.run(debug=True)