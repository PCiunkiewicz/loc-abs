"""Normalization utilities for the Loc-ABS frontend."""

from pathlib import Path


def normalize_values(resource: str, values: dict) -> dict:
    """Normalize values for specific resources before rendering forms.

    Args:
        resource (str): The type of resource (e.g., "prevention").
        values (dict): The original values to normalize.

    Returns:
        dict: The normalized values.
    """
    if not values:
        return {}

    normalizers = {
        'prevention': _normalize_prevention,
        'simulation': _normalize_simulation,
        'scenario': _normalize_scenario,
    }

    normalizer = normalizers.get(resource)
    if normalizer:
        return normalizer(dict(values))

    return dict(values)


def _normalize_prevention(values: dict) -> dict:
    """Normalize prevention resource values."""
    normalized = dict(values)
    mask = values.get('mask', {})
    vax = values.get('vax', {})

    normalized['mask_n95'] = mask.get('N95', 0.0)
    normalized['mask_home'] = mask.get('HOME', 0.0)
    normalized['mask_cloth'] = mask.get('CLOTH', 0.0)
    normalized['mask_surgical'] = mask.get('SURGICAL', 0.0)

    normalized['vaccine_mrna'] = vax.get('MRNA', 0.0)
    normalized['vaccine_astra'] = vax.get('ASTRA', 0.0)

    normalized.pop('mask', None)
    normalized.pop('vax', None)

    return normalized


def _normalize_simulation(values: dict) -> dict:
    """Normalize simulation resource values."""
    normalized = dict(values)

    # Normalize mapfile
    mapfile = values.get('mapfile')
    if isinstance(mapfile, dict):
        normalized['mapfile'] = mapfile.get('id') or mapfile.get('name')
    elif isinstance(mapfile, str):
        normalized['mapfile'] = _normalize_mapfile_path(mapfile)
    else:
        normalized['mapfile'] = mapfile

    return normalized


def _normalize_mapfile_path(mapfile: str) -> str:
    """Normalize mapfile path to relative format."""
    p = Path(mapfile)
    parts = p.parts
    if 'mapfiles' in parts:
        idx = parts.index('mapfiles')
        return Path(*parts[idx + 1 :]).as_posix()
    return p.as_posix()


def _normalize_scenario(values: dict) -> dict:
    """Normalize scenario resource values."""
    normalized = dict(values)

    for fk in ['sim', 'virus', 'prevention']:
        val = values.get(fk)
        if isinstance(val, dict):
            normalized[fk] = val.get('id') or val.get('name') or val
        else:
            normalized[fk] = val

    return normalized
