"""Input validation utilities for the LocABS frontend."""

import re


def validate_slug_name(name: str) -> dict:
    """Validate that the given name is a valid slug (alphanumeric, dashes, underscores).

    Args:
        name (str): The name to validate.

    Returns:
        dict: A dictionary with validation result and message.
    """
    # Check if input is empty or only whitespace
    if not name or name.strip() == '':
        return False

    validate = name.strip().lower()
    validate = re.sub(r'[^a-z0-9-_]+', '', validate)  # Replace invalid chars with dash
    validate = validate.strip('-')  # Remove leading/trailing dashes

    if not validate:
        return False, '', 'Name must contain at least one alphanumeric character.'

    return True, validate.capitalize(), ''


def validate_hex_color(color: str) -> dict:
    """Validate that the given string is a valid hex color code.

    Args:
        color (str): The color code to validate.

    Returns:
        dict: A dictionary with validation result and message.
    """
    if not color or not isinstance(color, str):
        return False, '', 'Color code cannot be empty.'

    if not color.startswith('#'):
        return False, '', "Color code must start with '#' symbol."

    color = color.strip()
    hex_pattern = r'^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$'

    if re.match(hex_pattern, color):
        return True, color, ''
    else:
        return False, '', 'Invalid hex color code. Must be in format #RRGGBB or #RGB.'


def validate_positive_integer(
    value: float, field_name: str = 'Rate', min_value: float = 0.0, max_value: float = 1.0
) -> dict:
    """Validate that the given value is a positive integer within specified bounds.

    Args:
        value (float): The value to validate.
        field_name (str): The name of the field for error messages.
        min_value (float): Minimum acceptable value (inclusive).
        max_value (float): Maximum acceptable value (inclusive).

    Returns:
        dict: A dictionary with validation result and message.
    """
    if value is None:
        return False, None, f'{field_name} cannot be empty.'

    if not isinstance(value, (int | float)):
        return False, None, f'{field_name} must be a number.'

    if value < min_value or value > max_value:
        return False, None, f'{field_name} must be between {min_value} and {max_value}.'

    return True, value, ''
