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

    def __init__(
        self,
        endpoint: str = '',
        *,
        base_url: str | None = None,
        session: requests.Session | None = None,
    ) -> None:
        """Initialize the GenericAPI instance with endpoint and session.

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
OUTPUTS_DIR = Path(os.getenv('OUTPUTS_DIR', '/data/outputs'))


def get_map_files() -> dict:
    """Fetch available map files from admin endpoint."""
    try:
        if not MAPFILES_DIR.exists():
            return False, [], f'Mapfiles directory not found at {MAPFILES_DIR}.'

        file_paths = [f.name for f in MAPFILES_DIR.iterdir() if f.is_file() or f.is_dir()]

        return True, file_paths, 'Success'
    except (OSError, PermissionError) as exc:
        return False, [], f'Error accessing map files: {exc}'


def get_run_output_files(run_id: int, run_name: str) -> dict:
    """Get HDF5 output files for a specific run.

    Args:
        run_id: ID of the run
        run_name: Name of the run

    Returns:
        Dict with success status, list of file names, and message
    """
    try:
        # Match the backend pattern: {run_id:03}-{run_name}
        run_dir = OUTPUTS_DIR / f'{run_id:03}-{run_name}'

        if not run_dir.exists():
            return False, [], f'Output directory not found for run {run_id}'

        # Get all HDF5 files
        hdf5_files = [f.name for f in run_dir.glob('*.hdf5')]

        if not hdf5_files:
            return False, [], f'No HDF5 output files found for run {run_id}'

        return True, hdf5_files, 'Success'
    except (OSError, PermissionError) as exc:
        return False, [], f'Error accessing output files: {exc}'


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


def list_output_files() -> dict:
    """Get list of all available HDF5 output files from backend."""
    api = _get_api('export')
    try:
        resp = api.request('get', 'list_outputs', append_slash=True)
        return handle_response(resp)
    except requests.RequestException as exc:
        return False, None, str(exc)


def create_export(run_id: int, name: str, export_type: str, params: dict | None = None) -> dict:
    """Create a new export for a specific run.

    Args:
        run_id: ID of the run to export
        name: Name for the export
        export_type: Type of export (ANIMATION, SNAPSHOT, EXCESS_RISK, etc.)
        params: Additional parameters for the export

    Returns:
        Dict with success status, export data, and message
    """
    # Get run details to find the output files
    success, run_data, err = get_by_id('run', run_id)

    if not success or not run_data:
        return False, None, f'Failed to get run details: {err}'

    run_name = run_data.get('name', 'unknown')

    # Get HDF5 output files for this run
    success, hdf5_files, err = get_run_output_files(run_id, run_name)

    if not success or not hdf5_files:
        return False, None, f'No output files found for this run: {err}'

    # Use the first HDF5 file or the one specified in params
    if params is None:
        params = {}

    if 'run_file' not in params:
        params['run_file'] = hdf5_files[0]

    payload = {'run': run_id, 'name': name, 'export_type': export_type, 'params': params}

    return create('export', payload)


def get_exports_for_run(run_id: int) -> dict:
    """Get all exports for a specific run."""
    try:
        success, all_exports, msg = get_all('export')
        if not success:
            return False, [], msg

        run_exports = [exp for exp in (all_exports or []) if exp.get('run') == run_id]
        return True, run_exports, 'Success'
    except Exception as exc:
        return False, [], str(exc)
