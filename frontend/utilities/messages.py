"""Centralized user-facing messages, labels, and tooltips for accessibility and consistency."""

from typing import Any

from utilities.types.api import Action, Resource, Result

# Field labels and tooltips (WCAG 2.2 - user-friendly terminology)
TERM_MAP = {
    'range': {
        'label': 'Scenario Range (Start — End)',
        'tooltip': 'The time or iteration span for this simulation run.',
    },
    'save_verbose': {
        'label': 'Save Detailed Output',
        'tooltip': 'Saves additional data but increases disk usage. Choose "No" for faster runs.',
    },
    'mapfile': {
        'label': 'Map (Visual Layout)',
        'tooltip': 'The spatial layout file that defines walkable areas and rooms.',
    },
    'vaccine': {
        'label': 'Vaccine Configuration',
        'tooltip': 'Vaccine types and doses. Each dose increases protection level.',
    },
    'mask': {
        'label': 'Mask Configuration',
        'tooltip': 'Mask types and their effectiveness values (0.0 - 1.0).',
    },
    'agents': {
        'label': 'Agent Population',
        'tooltip': 'The number and configuration of simulated agents (people).',
    },
    'simulation': {
        'label': 'Simulation Settings',
        'tooltip': 'Core parameters that control how the simulation runs.',
    },
}

# Resource-friendly names
RESOURCE_LABELS: dict[Resource, str] = {
    'scenario': 'Scenario',
    'simulation': 'Simulation Configuration',
    'virus': 'Virus Parameters',
    'prevention': 'Prevention Measures',
    'agent_config': 'Agent Configuration',
}

# Action messages for notifications
ACTION_MESSAGES: dict[Action, dict[Result, str]] = {
    'create': {
        'success': 'Successfully created {resource}.',
        'error': 'Failed to create {resource}. {detail}',
    },
    'update': {
        'success': 'Successfully updated {resource}.',
        'error': 'Failed to update {resource}. {detail}',
    },
    'delete': {
        'success': 'Successfully deleted {resource}.',
        'error': 'Failed to delete {resource}. {detail}',
    },
    'select': {
        'success': '{resource} selected.',
        'error': 'Failed to select {resource}.',
    },
}

# Common error translations (user-friendly)
ERROR_TRANSLATIONS = {
    'unique': 'A resource with this name already exists. Please choose a different name.',
    'required': 'This field is required.',
    'invalid': 'The value provided is not valid.',
    'not_found': 'The requested resource was not found.',
    '500': 'Server error. Please try again later.',
    '403': 'You do not have permission to perform this action.',
    '400': 'Invalid request. Please check your inputs.',
}


def get_user_friendly_message(resource: Resource, action: Action, success: bool, error: Any = None) -> str:
    """Generate user-friendly message for notifications.

    Args:
        resource: Resource type (e.g., 'scenario', 'simulation')
        action: Action performed ('create', 'update', 'delete', 'select')
        success: Boolean indicating success/failure
        error: Optional error details from backend

    Returns:
        User-friendly message string
    """
    resource_label = RESOURCE_LABELS.get(resource, resource.replace('_', ' ').title())

    if success:
        template = ACTION_MESSAGES.get(action, {}).get('success', '{resource} action completed.')
        return template.format(resource=resource_label)

    # Handle error cases with friendly translations
    detail = ''
    if error:
        error_str = str(error).lower()
        for key, translation in ERROR_TRANSLATIONS.items():
            if key in error_str:
                detail = translation
                break
        if not detail:
            detail = 'Please check your inputs and try again.'

    template = ACTION_MESSAGES.get(action, {}).get('error', '{resource} action failed.')
    return template.format(resource=resource_label, detail=detail)
