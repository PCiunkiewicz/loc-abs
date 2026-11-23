"""Run Builder Page for LocABS Application."""

from dash import register_page

from pages.run_builder import callbacks
from pages.run_builder.layout import layout  # noqa

# Register page
register_page(__name__, path='/scenario-builder', name='Run Builder', title='Loc-ABS  Run Builder')

# Register all callbacks
callbacks.register_all_callbacks()
