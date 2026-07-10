"""Payload builder for API requests."""

import copy

from pages.run_builder.config import AGENT_LOCKED_FIELDS
from utilities import api
from utilities.types.api import Resource


def build_payload(
    resource: Resource, form_data: dict, original: dict | None = None, extras: dict | None = None
) -> dict:
    """Build API payload from form data with resource-specific transformations."""
    data = dict(form_data)
    extras = extras or {}

    if resource == 'agent_config':
        locked = original or {}
        data['default'] = copy.deepcopy(locked.get('default', AGENT_LOCKED_FIELDS['default']))
        data['custom'] = copy.deepcopy(locked.get('custom', AGENT_LOCKED_FIELDS['custom']))

    elif resource == 'prevention':
        data['mask'] = extras.get('mask', {})
        data['vax'] = extras.get('vax', {})
        for key in data:
            if key.startswith(('mask_', 'vaccine_')):
                data.pop(key, None)

    elif resource == 'simulation':
        # Auto-populate mapfile with first available mapfile
        if 'mapfile' not in data:
            success_mapfile, mapfiles, _ = api.MAPFILES.get_all()
            if success_mapfile and mapfiles:
                data['mapfile'] = mapfiles[0]  # Use first available mapfile
            else:
                data['mapfile'] = None  # This will fail validation but let backend handle it
        else:
            # Process existing mapfile data
            mapfile = data.get('mapfile')
            if isinstance(mapfile, dict):
                data['mapfile'] = mapfile.get('id') or mapfile.get('name')

        # Convert save_verbose to boolean if it's a string
        save_verbose = data.get('save_verbose')
        if not isinstance(save_verbose, bool):
            data['save_verbose'] = save_verbose == 'true'

    return data
