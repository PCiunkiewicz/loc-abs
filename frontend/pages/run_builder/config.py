"""Configuration and field definitions for Run Builder."""

from components.input_components import create_mask_input, create_vaccine_type

# Child resources that should stay read-only until a scenario is being created/edited
SCENARIO_CHILD_RESOURCES = ['virus', 'prevention', 'simulation']

# All managed resources
RESOURCES = ['scenario', 'agent_config', 'virus', 'prevention', 'simulation']

# Virus field definitions
virus_fields = [
    {
        'id': {'type': 'form-input', 'resource': 'virus', 'field': 'name'},
        'label': 'Name',
        'type': 'text',
        'className': 'form-input',
    },
    {
        'id': {'type': 'form-input', 'resource': 'virus', 'field': 'attack_rate'},
        'label': 'Attack Rate',
        'type': 'number',
        'min': 0,
        'max': 1,
        'step': 0.001,
        'className': 'form-input',
    },
    {
        'id': {'type': 'form-input', 'resource': 'virus', 'field': 'infection_rate'},
        'label': 'Infection Rate',
        'type': 'number',
        'min': 0,
        'max': 1,
        'step': 0.001,
        'className': 'form-input',
    },
    {
        'id': {'type': 'form-input', 'resource': 'virus', 'field': 'fatality_rate'},
        'label': 'Fatality Rate',
        'type': 'number',
        'min': 0,
        'max': 1,
        'step': 0.001,
        'className': 'form-input',
    },
]

# Simulation field definitions
simulation_fields = [
    {
        'id': {'type': 'form-input', 'resource': 'simulation', 'field': 'name'},
        'label': 'Name',
        'type': 'text',
        'className': 'form-input',
    },
    {
        'id': {'type': 'form-input', 'resource': 'simulation', 'field': 'xy_scale'},
        'label': 'XY Scale',
        'type': 'number',
        'min': 1.0,
        'max': 1000000.0,
        'step': 0.01,
        'className': 'form-input',
    },
    {
        'id': {'type': 'form-input', 'resource': 'simulation', 'field': 't_step'},
        'label': 'Time Step (s)',
        'type': 'dropdown',
        'options': [
            {'label': '1 second', 'value': 1},
            {'label': '5 seconds', 'value': 5},
            {'label': '10 seconds', 'value': 10},
            {'label': '30 seconds', 'value': 30},
            {'label': '1 minute (60s)', 'value': 60},
            {'label': '5 minutes (300s)', 'value': 300},
            {'label': '10 minutes (600s)', 'value': 600},
            {'label': '30 minutes (1800s)', 'value': 1800},
            {'label': '1 hour (3600s)', 'value': 3600},
        ],
        'className': 'dropdown-standard',
    },
    {
        'id': {'type': 'form-input', 'resource': 'simulation', 'field': 'save_resolution'},
        'label': 'Save Resolution',
        'type': 'number',
        'min': 1,
        'max': 2147483647,
        'step': 1,
        'className': 'form-input',
    },
    {
        'id': {'type': 'form-input', 'resource': 'simulation', 'field': 'max_iter'},
        'label': 'Max Iterations',
        'type': 'number',
        'min': 1,
        'max': 2147483647,
        'step': 1,
        'className': 'form-input',
    },
    {
        'id': {'type': 'form-input', 'resource': 'simulation', 'field': 'save_verbose'},
        'label': 'Save Verbose',
        'type': 'radio',
        'options': [
            {'label': 'True', 'value': True},
            {'label': 'False', 'value': False},
        ],
    },
]

# Prevention field definitions
prevention_fields = [
    {
        'id': {'type': 'form-input', 'resource': 'prevention', 'field': 'name'},
        'label': 'Name',
        'type': 'text',
        'className': 'form-input',
    },
    {'id': 'mask_group_label', 'section_label': 'Mask Information'},
    {
        'id': {'type': 'form-input', 'resource': 'prevention', 'field': 'mask_n95'},
        'component': lambda readonly, value: create_mask_input('N95', 'N95', default_value=value, is_disabled=readonly),
    },
    {
        'id': {'type': 'form-input', 'resource': 'prevention', 'field': 'mask_home'},
        'component': lambda readonly, value: create_mask_input(
            'HOME', 'Home/Cloth', default_value=value, is_disabled=readonly
        ),
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
    {'id': 'vax_group_label', 'section_label': 'Vaccines'},
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
scenario_fields = [
    {
        'id': {'type': 'form-input', 'resource': 'scenario', 'field': 'name'},
        'label': 'Name',
        'type': 'text',
        'className': 'form-input',
    },
]

# Agent configuration field definitions
agentconfig_fields = [
    {
        'id': {'type': 'form-input', 'resource': 'agent_config', 'field': 'name'},
        'label': 'Name',
        'type': 'text',
        'className': 'form-input',
    },
    {'id': 'agent_pop_label', 'section_label': 'Agent Population'},
    {
        'id': {'type': 'form-input', 'resource': 'agent_config', 'field': 'random_agents'},
        'label': 'Random Agents',
        'type': 'number',
        'min': 0,
        'max': 10000,
        'className': 'form-input-number',
    },
    {
        'id': {'type': 'form-input', 'resource': 'agent_config', 'field': 'random_infected'},
        'label': 'Random Infected',
        'type': 'number',
        'min': 0,
        'max': 10000,
        'className': 'form-input-number',
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
