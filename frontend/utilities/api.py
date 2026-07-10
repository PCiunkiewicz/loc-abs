"""API requests for loc-abs backend."""

import functools
import os
from collections.abc import Callable
from typing import Any, ClassVar
from urllib.parse import urljoin

import requests
from loguru import logger

from utilities.types.api import Endpoint, Resource

type FormattedDashResponse = tuple[bool, Any, str]

DEFAULT_TIMEOUT = 10
STREAM_TIMEOUT = 120
BASE_URL: str = os.getenv('API_BASE_URL', 'http://abs-api:8000/api/v1/')
BASE_URL = BASE_URL if BASE_URL.endswith('/') else BASE_URL + '/'
logger.info(f'API base URL set to: {BASE_URL}')


def dash_formatted[**P](
    func: Callable[P, requests.Response],
) -> Callable[P, FormattedDashResponse]:
    """Convert responses to Dash callback friendly format."""

    @functools.wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> FormattedDashResponse:
        resp = func(*args, **kwargs)
        try:
            if resp.ok:
                data = resp.json() if resp.content else None
                return True, data, 'Success'
            error_msg = resp.json().get('detail', resp.reason) if resp.content else resp.reason
            return False, None, error_msg
        except (ValueError, requests.exceptions.JSONDecodeError) as exc:
            return False, None, str(exc)

    return wrapper


class GenericAPI:
    """Generic API class to handle requests to the loc-abs backend."""

    endpoints: ClassVar[dict[Resource, Endpoint]] = {
        'virus': 'viruses',
        'agent_config': 'agent_configs',
        'prevention': 'preventions',
        'simulation': 'simulations',
        'scenario': 'scenarios',
        'run': 'runs',
        'export': 'exports',
    }

    def __init__(self, endpoint: str = '', session: requests.Session | None = None) -> None:
        """Initialize the GenericAPI instance with endpoint and session."""
        self.url = urljoin(BASE_URL, endpoint)
        self.session = session or requests.Session()

    @dash_formatted
    def get_all(self, params: dict | None = None) -> requests.Response:
        """Get all objects."""
        return self.session.get(self.url, params=params, timeout=DEFAULT_TIMEOUT)

    @dash_formatted
    def get_by_id(self, obj_id: int, *args: str) -> requests.Response:
        """Get a specific object by ID."""
        path = '/'.join((str(obj_id), *args))
        return self.session.get(f'{self.url}/{path}', timeout=DEFAULT_TIMEOUT)

    @dash_formatted
    def create(self, data: dict) -> requests.Response:
        """Create a new object."""
        return self.session.post(f'{self.url}/', json=data, timeout=DEFAULT_TIMEOUT)

    @dash_formatted
    def update(self, obj_id: int, data: dict) -> requests.Response:
        """Update an existing object."""
        return self.session.patch(f'{self.url}/{obj_id}/', json=data, timeout=DEFAULT_TIMEOUT)

    @dash_formatted
    def delete(self, obj_id: int) -> requests.Response:
        """Delete an existing object."""
        return self.session.delete(f'{self.url}/{obj_id}/', timeout=DEFAULT_TIMEOUT)

    @dash_formatted
    def download(self, obj_id: int) -> requests.Response:
        """Download a file associated with an object."""
        return self.session.get(f'{self.url}/{obj_id}/download/', timeout=STREAM_TIMEOUT, stream=True)


SESSION = requests.Session()
API: dict[Resource, GenericAPI] = {
    name: GenericAPI(endpoint, SESSION) for name, endpoint in GenericAPI.endpoints.items()
}

SCENARIOS = API['scenario']
AGENT_CONFIGS = API['agent_config']
VIRUSES = API['virus']
PREVENTIONS = API['prevention']
SIMULATIONS = API['simulation']
RUNS = API['run']
EXPORTS = API['export']

MAPFILES = GenericAPI('mapfiles/', SESSION)
