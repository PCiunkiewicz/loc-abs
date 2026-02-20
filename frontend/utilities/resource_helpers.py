"""Shared helpers for rendering resource summaries and friendly names."""

import json
from collections.abc import Iterable
from typing import Any

from dash import html
from loguru import logger

from utilities import api
from utilities.messages import get_user_friendly_message as get_message

# Re-export the centralized message function
get_user_friendly_message = get_message


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
    return [
        ('Name', item.get('name')),
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

    icon_map = {
        'Name': 'fa-tag',
        'Virus': 'fa-virus',
        'Prevention': 'fa-shield-halved',
        'Simulation': 'fa-gears',
        'Masks': 'fa-mask-face',
        'Vaccines': 'fa-syringe',
        'Random Agents': 'fa-users',
        'Random Infected': 'fa-user-injured',
        'Mask Type': 'fa-mask-face',
        'Vax Type': 'fa-syringe',
        'Vax Doses': 'fa-vial',
        'Access Level': 'fa-key',
        'Urgency': 'fa-circle-exclamation',
        'Custom Profiles': 'fa-user-gear',
        'Mapfile': 'fa-file-lines',
        'XY Scale': 'fa-expand',
        'Time Step (s)': 'fa-clock',
        'Max Iterations': 'fa-infinity',
        'Save Resolution': 'fa-floppy-disk',
    }

    description_map = {
        'Name': 'Unique identifier for this configuration',
        'Virus': 'Outbreak settings used in this environment',
        'Prevention': 'Protective measures applied in this environment',
        'Simulation': 'Technical settings for how the simulation runs',
        'Masks': 'Types of face coverings and their effectiveness',
        'Vaccines': 'Immunization types and dose schedules',
        'Random Agents': 'Total number of people in the facility',
        'Random Infected': 'People who start with the infection',
        'Mask Type': 'Default face covering for participants',
        'Vax Type': 'Default vaccine type for participants',
        'Vax Doses': 'Number of vaccine doses received',
        'Access Level': 'Clearance level for restricted areas',
        'Urgency': 'Movement urgency factor (higher = faster)',
        'Custom Profiles': 'Individually configured participant types',
        'Mapfile': 'Floor plan or facility map reference',
        'XY Scale': 'Real-world distance conversion factor',
        'Time Step (s)': 'How often the simulation updates',
        'Max Iterations': 'Total simulation steps to execute',
        'Save Resolution': 'Frequency of saving simulation state',
    }

    name_field = None
    grid_items = []

    for label, val in rows:
        icon_class = icon_map.get(label, 'fa-circle-info')
        description = description_map.get(label, '')

        if isinstance(val, dict):
            val_display = html.Pre(
                json.dumps(val, indent=2),
                style={
                    'fontSize': '0.875rem',
                    'backgroundColor': '#f8fafc',
                    'padding': '0.5rem',
                    'borderRadius': '4px',
                },
            )
        elif isinstance(val, list) and all(isinstance(x, str | int | float) for x in val):
            val_display = html.Pre(
                json.dumps(val, indent=2),
                style={
                    'fontSize': '0.875rem',
                    'backgroundColor': '#f8fafc',
                    'padding': '0.5rem',
                    'borderRadius': '4px',
                },
            )
        elif isinstance(val, str | int | float | bool):
            val_display = html.Span(
                str(val),
                style={'fontSize': '0.95rem', 'color': '#1e293b', 'fontWeight': '500'},
            )
        else:
            val_display = val

        field_item = html.Div(
            [
                html.Div(
                    [
                        html.I(
                            className=f'fa {icon_class}',
                            style={'color': '#3b82f6', 'fontSize': '1.1rem', 'marginRight': '0.75rem'},
                        ),
                        html.Span(
                            f'{label}',
                            style={'fontSize': '0.875rem', 'color': '#64748b', 'fontWeight': '600'},
                        ),
                    ],
                    style={'display': 'flex', 'alignItems': 'center', 'marginBottom': '0.25rem'},
                ),
                html.Div(
                    description,
                    style={
                        'paddingLeft': '2rem',
                        'fontSize': '0.75rem',
                        'color': '#94a3b8',
                        'fontStyle': 'italic',
                        'marginBottom': '0.5rem',
                    },
                )
                if description
                else None,
                html.Div(
                    val_display,
                    style={'paddingLeft': '2rem'},
                ),
            ],
            className='summary-row',
            style={
                'padding': '0.75rem',
                'backgroundColor': '#ffffff',
                'borderRadius': '6px',
                'border': '1px solid #e2e8f0',
            },
        )

        if label == 'Name':
            name_field = html.Div(
                field_item,
                style={'marginBottom': '1rem'},
            )
        else:
            grid_items.append(field_item)

    result = []
    if name_field:
        result.append(name_field)

    if grid_items:
        result.append(
            html.Div(
                grid_items,
                style={
                    'display': 'grid',
                    'gridTemplateColumns': 'repeat(3, 1fr)',
                    'gap': '0.75rem',
                },
            )
        )

    return result
