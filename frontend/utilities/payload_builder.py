"""Payload builder for API requests."""

import copy
from utilities import api


def build_payload(resource, form_data, original=None, extras=None):
    """Build API payload from form data with resource-specific transformations."""
    from pages.run_builder.config import AGENT_LOCKED_FIELDS

    data = dict(form_data)
    extras = extras or {}

    if resource == 'agent_config':
        locked = original or {}
        data['default'] = copy.deepcopy(locked.get('default', AGENT_LOCKED_FIELDS['default']))
        data['custom'] = copy.deepcopy(locked.get('custom', AGENT_LOCKED_FIELDS['custom']))

    elif resource == 'prevention':
        data['mask'] = extras.get('mask', {})
        data['vax'] = extras.get('vax', {})
        for key in list(data.keys()):
            if key.startswith('mask_') or key.startswith('vaccine_'):
                data.pop(key, None)

    elif resource == 'simulation':
        # Auto-populate terrain with all available terrain IDs
        if 'terrain' not in data or not data.get('terrain'):
            success_terrain, terrains, _ = api.get_all('terrain')
            if success_terrain and terrains:
                data['terrain'] = [t['id'] for t in terrains]
            else:
                data['terrain'] = []
        else:
            # Process existing terrain data
            terrain = data.get('terrain')
            if isinstance(terrain, list):
                data['terrain'] = [t['id'] if isinstance(t, dict) else t for t in terrain]

        # Auto-populate mapfile with first available mapfile
        if 'mapfile' not in data or not data.get('mapfile'):
            success_mapfile, mapfiles, _ = api.get_map_files()
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
        if save_verbose == 'true':
            data['save_verbose'] = True
        elif save_verbose == 'false':
            data['save_verbose'] = False
        elif save_verbose is None or save_verbose == '':
            data['save_verbose'] = False  # Default to False if not provided

    return data
