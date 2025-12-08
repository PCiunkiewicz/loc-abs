"""Normalization utilities for the LocABS frontend."""


def normalize_values(resource, values):
    """Normalize values for specific resources before rendering forms.

    Args:
        resource (str): The type of resource (e.g., "prevention").
        values (dict): The original values to normalize.

    Returns:
        dict: The normalized values.
    """
    if not values:
        return {} or None

    normalized = dict(values)

    # Prevention
    if resource == 'prevention':
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

    if resource == 'simulation':
        terrain = values.get('terrain')
        if isinstance(terrain, list):
            normalized['terrain'] = [t['id'] if isinstance(t, dict) else t for t in terrain]

        # Mapfile
        mapfile = values.get('mapfile')
        if isinstance(mapfile, dict):
            normalized['mapfile'] = mapfile.get('id') or mapfile.get('name')
        else:
            normalized['mapfile'] = mapfile

    return normalized
