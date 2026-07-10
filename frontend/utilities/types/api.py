"""Type definitions for system-related data structures."""

from typing import Literal

Action = Literal['create', 'update', 'delete', 'select']
Result = Literal['success', 'error']
Resource = Literal['scenario', 'agent_config', 'virus', 'prevention', 'simulation', 'run', 'export']
Endpoint = Literal['scenarios', 'agent_configs', 'viruses', 'preventions', 'simulations', 'runs', 'exports']
