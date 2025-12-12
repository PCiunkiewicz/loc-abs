"""Shared helpers for rendering resource summaries and friendly names."""

import json
from typing import Any
from collections.abc import Iterable

from dash import html
from loguru import logger

from utilities import api


def get_user_friendly_message(resource, action, success, error_msg=''):
    """Convert backend errors to user-friendly messages."""
    resource_labels = {
        'scenario': 'scenario',
        'simulation': 'simulation configuration',
        'virus': 'virus parameters',
        'prevention': 'prevention measures',
        'agent_config': 'agent configuration',
    }
    label = resource_labels.get(resource, resource)

    if success:
        if action == 'create':
            return f'Successfully created {label}!'
        elif action == 'update':
            return f'Successfully updated {label}!'
        elif action == 'delete':
            return f'Successfully deleted {label}!'
        elif action == 'select':
            return f'Selected {label}'
        return f'{action.capitalize()} successful!'

    # Error messages
    error_lower = error_msg.lower() if error_msg else ''

    # Check for common error patterns
    if 'unique' in error_lower or 'already exists' in error_lower:
        return f'A {label} with this name already exists. Please choose a different name.'
    elif 'required' in error_lower or 'cannot be null' in error_lower or 'cannot be blank' in error_lower:
        return f'Please fill in all required fields for {label}.'
    elif 'invalid' in error_lower:
        return f'The information provided for {label} is invalid. Please check your input.'
    elif 'not found' in error_lower or '404' in error_lower:
        return f'The {label} you are looking for could not be found.'
    elif 'permission' in error_lower or 'forbidden' in error_lower or '403' in error_lower:
        return f'You do not have permission to {action} this {label}.'
    elif 'connection' in error_lower or 'timeout' in error_lower:
        return 'Unable to connect to the server. Please check your connection and try again.'
    elif action == 'create':
        return f'Failed to create {label}. Please check your input and try again.'
    elif action == 'update':
        return f'Failed to update {label}. Please check your input and try again.'
    elif action == 'delete':
        return f'Failed to delete {label}. It may be in use by other items.'
    else:
        return f'An error occurred while performing {action} on {label}. Please try again.'


def friendly_name(resource: str, res_id: Any) -> str:
    """Resolve a readable name for a related resource id."""
    if not res_id:
        return 'Not set'
    try:
        success, obj, _ = api.get_by_id(resource, res_id)
        if success and obj:
            return obj.get('name') or str(res_id)
    except Exception as exc:  # pylint: disable=broad-exception-caught
        logger.exception('Error fetching %s %s: %s', resource, res_id, exc)
    return str(res_id)


def _format_dict_items(data: dict[str, Any]) -> list[html.Li]:
    """Return a list of <li> for non-empty dict entries."""
    items = []
    for k, v in data.items():
        if v in (None, '', [], {}, 0):
            continue
        items.append(html.Li(f'{k.replace("_", " ").title()}: {v}'))
    return items or [html.Li('None')]


def _prevention_rows(item: dict[str, Any]) -> Iterable[tuple[str, Any]]:
    """Format prevention mask/vax selections."""
    # Extract mask data from flat fields
    mask_items = []
    mask_fields = {
        'mask_n95': 'N95',
        'mask_home': 'Home/Cloth',
        'mask_cloth': 'Cloth',
        'mask_surgical': 'Surgical',
    }
    for field, label in mask_fields.items():
        val = item.get(field)
        if val and float(val) > 0:
            mask_items.append(html.Li(f'{label}: {val}'))
    mask_list = html.Ul(mask_items or [html.Li('None selected')])

    # Extract vaccine data from flat fields
    vax_items = []
    vax_fields = {
        'vaccine_mrna': 'MRNA (Moderna)',
        'vaccine_astra': 'ASTRA (AstraZeneca)',
    }
    for field, label in vax_fields.items():
        doses = item.get(field)
        if doses and isinstance(doses, list):
            dose_items = [html.Li(f'Dose {i + 1}: {d}') for i, d in enumerate(doses) if d]
            if dose_items:
                vax_items.append(html.Li([html.Strong(f'{label}:'), html.Ul(dose_items)]))
    vax_list = html.Ul(vax_items or [html.Li('None selected')])

    return [
        ('Name', item.get('name')),
        ('Masks', mask_list),
        ('Vaccines', vax_list),
    ]


def _agent_rows(item: dict[str, Any]) -> Iterable[tuple[str, Any]]:
    """Format agent configuration details."""
    default = item.get('default') or {}
    info = default.get('info') or {}
    rows = [
        ('Name', item.get('name')),
        ('Random Agents', item.get('random_agents')),
        ('Random Infected', item.get('random_infected')),
        ('Mask Type', info.get('mask_type') or 'Not set'),
        ('Vax Type', info.get('vax_type') or 'Not set'),
        ('Vax Doses', info.get('vax_doses') or 0),
        ('Access Level', info.get('access_level') or 0),
        ('Urgency', info.get('urgency') or 0),
    ]

    custom = item.get('custom') or []
    rows.append(('Custom Profiles', f'{len(custom)} configured'))
    return rows


def _simulation_rows(item: dict[str, Any]) -> Iterable[tuple[str, Any]]:
    """Format simulation details with terrain names."""
    terrain_ids = item.get('terrain', [])
    terrain_items = []
    if terrain_ids:
        for tid in terrain_ids:
            terrain_items.append(html.Li(friendly_name('terrain', tid)))
    terrain_list = html.Ul(terrain_items or [html.Li('None selected')])

    return [
        ('Name', item.get('name')),
        ('Terrain', terrain_list),
        ('Mapfile', item.get('mapfile') or 'Not set'),
        ('XY Scale', item.get('xy_scale')),
        ('Time Step (s)', item.get('t_step')),
        ('Max Iterations', item.get('max_iter')),
        ('Save Resolution', item.get('save_resolution')),
    ]


def build_rows(resource_type: str, item: dict[str, Any]) -> Iterable[tuple[str, Any]]:
    """Build label/value rows for a resource."""
    if resource_type == 'scenario':
        return [
            ('Name', item.get('name')),
            ('Virus', friendly_name('virus', item.get('virus') or item.get('virus_id'))),
            ('Prevention', friendly_name('prevention', item.get('prevention') or item.get('prevention_id'))),
            ('Simulation', friendly_name('simulation', item.get('sim') or item.get('simulation'))),
        ]
    if resource_type == 'prevention':
        return _prevention_rows(item)
    if resource_type == 'agent_config':
        return _agent_rows(item)
    if resource_type == 'simulation':
        return _simulation_rows(item)
    return [(k.title().replace('_', ' '), v) for k, v in item.items() if k != 'id']


def render_summary(resource_type: str, item: dict[str, Any]):
    """Render a readable summary block for a resource item."""
    if not item:
        return html.Div()

    rows = build_rows(resource_type, item)
    summary_rows = []
    for label, val in rows:
        if isinstance(val, dict):
            summary_rows.append(html.Div([html.Strong(f'{label}: '), html.Pre(json.dumps(val, indent=2))]))
        elif isinstance(val, list) and all(isinstance(x, str | int | float) for x in val):
            summary_rows.append(html.Div([html.Strong(f'{label}: '), html.Pre(json.dumps(val, indent=2))]))
        elif isinstance(val, str | int | float | bool):
            summary_rows.append(html.P([html.Strong(f'{label}: '), str(val)]))
        else:
            summary_rows.append(html.Div([html.Strong(f'{label}: '), val]))

    return summary_rows
