"""API requests for loc-abs backend."""
import requests
import os
from pathlib import Path


class GenericAPI:
    """Generic API class to handle requests to the loc-abs backend.

    Attributes:
        base_url (str): The base URL for the API.
        endpoint (str): The specific endpoint for the API.
        session (requests.Session): The session object for making requests.

    """
    base_url: str = os.getenv('API_BASE_URL', 'http://abs-api:8000/api/v1')
    print(f'API Base URL: {base_url}')

    def __init__(self, endpoint: str = '') -> None:
        """Initialize the GenericAPI class with an optional endpoint.

        Args:
            endpoint (str): The specific target endpoint. Defaults to ''.
        """
        self.url = f'{self.base_url}/{endpoint}' if endpoint else self.base_url
        self.session = requests.Session()

    def post(self, data: dict) -> requests.Response:
        """Make a POST request to the API."""
        return self.session.post(
            f'{self.url}/',
            timeout=10,
            json=data,
        )

    def get(self, obj_id: int | None = None) -> requests.Response:
        """Make a GET request to the API."""
        return self.session.get(
            self.url if obj_id is None else f'{self.url}/{obj_id}',
            timeout=10,
        )

    def patch(self, obj_id: int, data: dict) -> requests.Response:
        """Make a PATCH request to the API."""
        return self.session.patch(
            f'{self.url}/{obj_id}/',
            timeout=10,
            json=data,
        )

    def delete(self, obj_id: int) -> requests.Response:
        """Make a DELETE request to the API."""
        return self.session.delete(
            f'{self.url}/{obj_id}/',
            timeout=10,
        )

## API Instances for Specific Endpoints
APIS = {
    'terrain': GenericAPI('terrains'),
    'virus': GenericAPI('viruses'),
    'agent_config': GenericAPI('agent_configs'),
    'prevention': GenericAPI('preventions'),
    'simulation': GenericAPI('simulations'),
    'scenario': GenericAPI('scenarios'),
    'run': GenericAPI('runs'),
}


# Response Handler
def handle_response(response: requests.Response) -> dict:
    """Handle API response and return formatted tuple for Dash callbacks."""
    try:
        if response.ok:
            data = response.json() if response.content else None
            return True, data, 'Success'
        else:
            error_msg = response.json().get('detail', response.reason) if response.content else response.reason
            return False, None, error_msg
    except Exception as e:
        return False, None, str(e)


# Operations for Specific Endpoints
def get_all(resource: str) -> dict:
    """Get all objects from a specific resource endpoint."""
    api = APIS.get(resource)
    if not api:
        return False, None, f"Resource '{resource}' not found."
    return handle_response(APIS[resource].get())


def get_by_id(resource: str, obj_id: int) -> dict:
    """Get a specific object by ID from a resource endpoint."""
    api = APIS.get(resource)
    if not api:
        return False, None, f"Resource '{resource}' not found."
    return handle_response(APIS[resource].get(obj_id))


def create(resource: str, data: dict) -> dict:
    """Create a new object in a specific resource endpoint."""
    api = APIS.get(resource)
    if not api:
        return False, None, f"Resource '{resource}' not found."
    return handle_response(APIS[resource].post(data))


def update(resource: str, obj_id: int, data: dict) -> dict:
    """Update an existing object in a specific resource endpoint."""
    api = APIS.get(resource)
    if not api:
        return False, None, f"Resource '{resource}' not found."
    return handle_response(APIS[resource].patch(obj_id, data))


def delete(resource: str, obj_id: int) -> dict:
    """Delete an existing object in a specific resource endpoint."""
    api = APIS.get(resource)
    if not api:
        return False, None, f"Resource '{resource}' not found."
    return handle_response(APIS[resource].delete(obj_id))


def get_map_files() -> dict:
    """Fetch available map files from admin endpoint."""
    try:
        mapfiles_dir = Path('/data/mapfiles')   # <-- correct container path

        if not mapfiles_dir.exists():
            return False, [], 'Mapfiles directory not found in container at /data/mapfiles.'

        file_paths = [f.name for f in mapfiles_dir.iterdir() if f.is_file() or f.is_dir()]

        return True, file_paths, 'Success'

    except Exception as e:
        return False, [], f'Error accessing map files: {str(e)}'
