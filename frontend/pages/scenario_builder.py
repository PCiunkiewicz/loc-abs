"""Run Builder Page for LocABS Application."""

from dash import register_page

from utilities.logging import configure_logger

# Import layout and callbacks
from pages.run_builder.layout import layout
from pages.run_builder import callbacks

# Configure logging
configure_logger(level='DEBUG')

# Register page
register_page(__name__, path='/scenario-builder', name='Run Builder', title='LocABS  Run Builder')

# Register all callbacks
callbacks.register_all_callbacks()
