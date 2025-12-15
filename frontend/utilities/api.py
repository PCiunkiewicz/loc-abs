"""API requests for loc-abs backend."""

import os
from pathlib import Path

import requests

DEFAULT_TIMEOUT = 10
STREAM_TIMEOUT = 120

def _join_url(*parts: object) -> str:
    """Join URL parts without duplicate slashes."""
    cleaned = [str(p).strip('/') for p in parts if p not in (None, '')]
    return '/'.join(cleaned)

class GenericAPI:
    """Generic API class to handle requests to the loc-abs backend.

    Attributes:
        base_url (str): The base URL for the API.
        endpoint (str): The specific endpoint for the API.
        session (requests.Session): The session object for making requests.

    """
    base_url: str = os.getenv('API_BASE_URL', 'http://abs-api:8000/api/v1').rstrip('/')

    def __init__(self, endpoint: str = '', *, base_url: str | None = None, session: requests.Session | None = None,
    ) -> None:
        """"Initialize the GenericAPI instance with endpoint and session.

        Args:
            endpoint (str): The specific endpoint for the API. Defaults to ''.
            base_url (str | None): The base URL for the API. If None, uses the class default. Defaults to None.
            session (requests.Session | None): The session object for making requests.
        """
        self.base_url = (base_url or self.base_url).rstrip('/')
        self.session = session or requests.Session()
        self.url = _join_url(self.base_url, endpoint)

    def request(
        self,
        method: str,
        path: object = '',
        *,
        params: dict | None = None,
        json: dict | None = None,
        timeout: int = DEFAULT_TIMEOUT,
        append_slash: bool = False,
        **kwargs,
    ) -> requests.Response:
        """Make an HTTP request to the API.

        Args:
            method (str): The HTTP method (e.g., 'get', 'post', 'patch', 'delete').
            path (object): The specific path or object ID to append to the endpoint. Defaults to ''.
            params (dict | None): Query parameters for the request. Defaults to None.
            json (dict | None): JSON payload for the request. Defaults to None.
            timeout (int): Timeout for the request in seconds. Defaults to DEFAULT_TIMEOUT.
            append_slash (bool): Whether to append a trailing slash to the URL. Defaults to False.
            **kwargs: Additional arguments to pass to the request.

        Returns:
            requests.Response: The response object from the request.
        """
        target = _join_url(self.url, path)
        if append_slash:
            target = f'{target}/'
        return self.session.request(
            method=method,
            url=target,
            params=params,
            json=json,
            timeout=timeout,
            **kwargs,
        )

    def post(self, data: dict) -> requests.Response:
        """Create a new object in the API."""
        return self.request('post', json=data, append_slash=True)

    def get(self, obj_id: object | None = None, params: dict | None = None) -> requests.Response:
        """Retrieve objects from the API."""
        return self.request('get', obj_id, params=params)

    def patch(self, obj_id: object, data: dict) -> requests.Response:
        """Update an existing object in the API."""
        return self.request('patch', obj_id, json=data, append_slash=True)

    def delete(self, obj_id: object) -> requests.Response:
        """Delete an existing object in the API."""
        return self.request('delete', obj_id, append_slash=True)

RESOURCE_ENDPOINTS = {
    'terrain': 'terrains',
    'virus': 'viruses',
    'agent_config': 'agent_configs',
    'prevention': 'preventions',
    'simulation': 'simulations',
    'scenario': 'scenarios',
    'run': 'runs',
    'export': 'exports',
}

SESSION = requests.Session()
APIS: dict[str, GenericAPI] = {
    name: GenericAPI(endpoint, session=SESSION) for name, endpoint in RESOURCE_ENDPOINTS.items()
}

def _get_api(resource: str) -> GenericAPI:
    endpoint = RESOURCE_ENDPOINTS.get(resource, resource)
    if resource not in APIS:
        APIS[resource] = GenericAPI(endpoint, session=SESSION)
    return APIS[resource]

def handle_response(response: requests.Response) -> dict:
    """Handle API response and return formatted tuple for Dash callbacks."""
    try:
        if response.ok:
            data = response.json() if response.content else None
            return True, data, 'Success'
        error_msg = response.json().get('detail', response.reason) if response.content else response.reason
        return False, None, error_msg
    except (ValueError, requests.exceptions.JSONDecodeError) as exc:
        return False, None, str(exc)

def _dispatch(resource: str, fn) -> dict:
    return handle_response(fn(_get_api(resource)))

def get_all(resource: str, params: dict | None = None) -> dict:
    """Get all objects from a specific resource endpoint."""
    return _dispatch(resource, lambda api: api.get(params=params))

def get_by_id(resource: str, obj_id: int) -> dict:
    """Get a specific object by ID from a resource endpoint."""
    return _dispatch(resource, lambda api: api.get(obj_id))

def create(resource: str, data: dict) -> dict:
    """Create a new object in a specific resource endpoint."""
    return _dispatch(resource, lambda api: api.post(data))

def update(resource: str, obj_id: int, data: dict) -> dict:
    """Update an existing object in a specific resource endpoint."""
    return _dispatch(resource, lambda api: api.patch(obj_id, data))

def delete(resource: str, obj_id: int) -> dict:
    """Delete an existing object in a specific resource endpoint."""
    return _dispatch(resource, lambda api: api.delete(obj_id))

MAPFILES_DIR = Path(os.getenv('MAPFILES_DIR', '/data/mapfiles'))

def get_map_files() -> dict:
    """Fetch available map files from admin endpoint."""
    try:
        if not MAPFILES_DIR.exists():
            return False, [], f'Mapfiles directory not found at {MAPFILES_DIR}.'

        file_paths = [f.name for f in MAPFILES_DIR.iterdir() if f.is_file() or f.is_dir()]

        return True, file_paths, 'Success'
    except (OSError, PermissionError) as exc:
        return False, [], f'Error accessing map files: {exc}'


def start_run(run_id: int) -> dict:
    """Request backend to start a run (enqueue worker)."""
    api = _get_api('run')
    try:
        resp = api.request('post', f'{run_id}/start', append_slash=True)
        return handle_response(resp)
    except requests.RequestException as exc:
        return False, None, str(exc)


def get_run_status(run_id: int) -> dict:
    """Get run details / status from runs endpoint."""
    api = _get_api('run')
    try:
        return handle_response(api.get(run_id))
    except requests.RequestException as exc:
        return False, None, str(exc)


def download_run_export(run_id: int, dest: str | Path) -> dict:
    """Stream export file for a finished run to dest (file path or directory)."""
    api = _get_api('run')
    try:
        resp = api.request('get', f'{run_id}/export', append_slash=True, stream=True, timeout=STREAM_TIMEOUT)
    except requests.RequestException as exc:
        return False, None, str(exc)

    if not resp.ok:
        return handle_response(resp)

    dest_path = Path(dest)
    if dest_path.is_dir() or str(dest).endswith(('/', '\\')):
        cd = resp.headers.get('content-disposition', '')
        filename = None
        if 'filename=' in cd:
            filename = cd.split('filename=')[-1].strip('"; ')
        filename = filename or f'run_{run_id}_export.zip'
        dest_path = dest_path.joinpath(filename)

    dest_path.parent.mkdir(parents=True, exist_ok=True)
    try:
        with open(dest_path, 'wb') as fh:
            for chunk in resp.iter_content(chunk_size=8192):
                if chunk:
                    fh.write(chunk)
        return True, str(dest_path), 'Success'
    except OSError as exc:
        return False, None, str(exc)
