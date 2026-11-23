"""Configuration and field definitions for Run Builder."""

from components.input_components import create_mask_input, create_vaccine_type
from utilities.types.api import Resource
from utilities.types.forms import Field

# All managed resources
RESOURCES: list[Resource] = ['scenario', 'agent_config', 'virus', 'prevention', 'simulation']
# Child resources that should stay read-only until a scenario is being created/edited
SCENARIO_RESOURCES: list[Resource] = ['virus', 'prevention', 'simulation']

# Virus field definitions
VIRUS_FIELDS: list[Field] = [
    {
        'id': {'type': 'form-input', 'resource': 'virus', 'field': 'name'},
        'label': 'Configuration Name',
        'type': 'text',
        'css_class': 'form-input',
        'tooltip': 'Unique identifier for this outbreak configuration',
    },
    {
        'id': {'type': 'form-input', 'resource': 'virus', 'field': 'attack_rate'},
        'label': 'Infection Likelihood (0.0 to 1.0)',
        'type': 'number',
        'min': 0,
        'max': 1,
        'step': 0.001,
        'css_class': 'form-input',
        'tooltip': 'Probability of infection when exposed (0 = 0%, 1 = 100%)',
    },
    {
        'id': {'type': 'form-input', 'resource': 'virus', 'field': 'infection_rate'},
        'label': 'Transmission Speed (0.0 to 1.0)',
        'type': 'number',
        'min': 0,
        'max': 1,
        'step': 0.001,
        'css_class': 'form-input',
        'tooltip': 'How quickly the infection spreads between people (higher = faster spread)',
    },
    {
        'id': {'type': 'form-input', 'resource': 'virus', 'field': 'fatality_rate'},
        'label': 'Fatality Rate',
        'type': 'number',
        'min': 0,
        'max': 1,
        'step': 0.001,
        'css_class': 'form-input',
        'tooltip': 'Proportion of infected individuals who do not recover (0 = 0%, 1 = 100%)',
    },
]

# Simulation field definitions
SIMULATION_FIELDS: list[Field] = [
    {
        'id': {'type': 'form-input', 'resource': 'simulation', 'field': 'name'},
        'label': 'Configuration Name',
        'type': 'text',
        'css_class': 'form-input',
        'tooltip': 'Unique identifier for this simulation configuration',
    },
    {
        'id': {'type': 'form-input', 'resource': 'simulation', 'field': 'xy_scale'},
        'label': 'Distance Scale (meters to units)',
        'type': 'number',
        'min': 0.001,
        'max': 1000000.0,
        'step': 0.01,
        'css_class': 'form-input',
        'tooltip': 'Conversion factor from real-world meters to simulation units',
    },
    {
        'id': {'type': 'form-input', 'resource': 'simulation', 'field': 't_step'},
        'label': 'Update Interval (seconds)',
        'type': 'dropdown',
        'options': [
            {'label': '1 second', 'value': 1},
            {'label': '5 seconds', 'value': 5},
            {'label': '10 seconds', 'value': 10},
            {'label': '30 seconds', 'value': 30},
            {'label': '1 minute (60 seconds)', 'value': 60},
            {'label': '5 minutes (300 seconds)', 'value': 300},
            {'label': '10 minutes (600 seconds)', 'value': 600},
            {'label': '30 minutes (1800 seconds)', 'value': 1800},
            {'label': '1 hour (3600 seconds)', 'value': 3600},
        ],
        'css_class': 'dropdown-standard',
        'tooltip': 'How often the simulation updates (smaller = more detailed but slower)',
    },
    {
        'id': {'type': 'form-input', 'resource': 'simulation', 'field': 'save_resolution'},
        'label': 'Save Frequency (every N steps)',
        'type': 'number',
        'min': 1,
        'max': 1000,
        'step': 1,
        'css_class': 'form-input',
        'tooltip': 'How often to save simulation state (every N iterations)',
    },
    {
        'id': {'type': 'form-input', 'resource': 'simulation', 'field': 'max_iter'},
        'label': 'Total Steps to Run',
        'type': 'number',
        'min': 1,
        'max': 100000,
        'step': 1,
        'css_class': 'form-input',
        'tooltip': 'Total number of simulation steps to run',
    },
    {
        'id': {'type': 'form-input', 'resource': 'simulation', 'field': 'save_verbose'},
        'label': 'Save Detailed Information',
        'type': 'radio',
        'options': [
            {'label': 'Yes', 'value': True},
            {'label': 'No', 'value': False},
        ],
        'tooltip': 'Save detailed information at each save point (requires more storage)',
    },
]

# Prevention field definitions
PREVENTION_FIELDS: list[Field] = [
    {
        'id': {'type': 'form-input', 'resource': 'prevention', 'field': 'name'},
        'label': 'Configuration Name',
        'type': 'text',
        'css_class': 'form-input',
        'tooltip': 'Unique identifier for this prevention configuration',
    },
    {
        'id': {'type': 'form-input', 'resource': 'prevention', 'field': 'mask_n95'},
        'component': lambda readonly, value: create_mask_input('N95', 'N95', default_value=value, is_disabled=readonly),
    },
    {
        'id': {'type': 'form-input', 'resource': 'prevention', 'field': 'mask_cloth'},
        'component': lambda readonly, value: create_mask_input(
            'CLOTH', 'Cloth', default_value=value, is_disabled=readonly
        ),
    },
    {
        'id': {'type': 'form-input', 'resource': 'prevention', 'field': 'mask_surgical'},
        'component': lambda readonly, value: create_mask_input(
            'SURGICAL', 'Surgical', default_value=value, is_disabled=readonly
        ),
    },
    {
        'id': {'type': 'form-input', 'resource': 'prevention', 'field': 'vaccine_mrna'},
        'component': lambda readonly, value: create_vaccine_type(
            'MRNA',
            'MRNA (Moderna)',
            default_doses=value,
            is_disabled=readonly,
        ),
    },
    {
        'id': {'type': 'form-input', 'resource': 'prevention', 'field': 'vaccine_astra'},
        'component': lambda readonly, value: create_vaccine_type(
            'ASTRA',
            'ASTRA (AstraZeneca)',
            default_doses=value,
            is_disabled=readonly,
        ),
    },
]

# Scenario field definitions
SCENARIO_FIELDS: list[Field] = [
    {
        'id': {'type': 'form-input', 'resource': 'scenario', 'field': 'name'},
        'label': 'Scenario Name',
        'type': 'text',
        'css_class': 'form-input',
        'tooltip': 'Unique name for this simulation scenario setup',
    },
]

# Agent configuration field definitions
AGENT_CONFIG_FIELDS: list[Field] = [
    {
        'id': {'type': 'form-input', 'resource': 'agent_config', 'field': 'name'},
        'label': 'Configuration Name',
        'type': 'text',
        'css_class': 'form-input',
        'tooltip': 'Unique name for this population configuration',
    },
    {
        'id': {'type': 'form-input', 'resource': 'agent_config', 'field': 'random_agents'},
        'label': 'Total Number of People',
        'type': 'number',
        'min': 0,
        'max': 10000,
        'css_class': 'form-input-number',
        'tooltip': 'Total number of people to simulate in the facility',
    },
    {
        'id': {'type': 'form-input', 'resource': 'agent_config', 'field': 'random_infected'},
        'label': 'Initially Infected People',
        'type': 'number',
        'min': 0,
        'max': 10000,
        'css_class': 'form-input-number',
        'tooltip': 'How many people start with the infection at the beginning',
    },
]

# Agent configuration locked fields structure
AGENT_LOCKED_FIELDS = {
    'default': {
        'info': {
            'mask_type': '',
            'vax_type': '',
            'vax_doses': 0,
            'age': None,
            'start_zone': None,
            'work_zone': None,
            'home_zone': None,
            'schedule': {},
            'access_level': 0,
            'urgency': 1.0,
        },
        'state': {'dt': None, 'status': 'UNKNOWN', 'pos': (0, 0, 0), 'path': []},
    },
    'custom': [],
}

# Resource labels for user-friendly messages
RESOURCE_LABELS = {
    'scenario': 'scenario',
    'simulation': 'simulation configuration',
    'virus': 'virus parameters',
    'prevention': 'prevention measures',
    'agent_config': 'agent configuration',
}
