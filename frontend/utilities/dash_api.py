"""API requests for loc-abs backend."""
import requests
import os

class GenericAPI:
    """Generic API class to handle requests to the loc-abs backend.
    
    Attributes:
        base_url (str): The base URL for the API.
        endpoint (str): The specific endpoint for the API.
        session (requests.Session): The session object for making requests.

    """
    # TODO: fOR WHEN CONNECTING TO DOCKER CONTAINER
    #base_url: str = 'http://api:8000/api/v1'

    base_url: str = os.getenv('API_BASE_URL', 'http://localhost:8000/api/v1')

    def __init__(self, endpoint: str = '') -> None:
        """Initialize the GenericAPI class with an optional endpoint.

        Args:
            endpoint (str): The specific target endpoint. Defaults to ''.
        """
        self.url = f'{self.base_url}/{endpoint}' if endpoint else self.base_url
        self.session = requests.Session()

    def post(self, data: dict) -> requests.Response:
        """Make a POST request to the API.

        Args:
            data (dict): The data to send in the POST request.

        Returns:
            requests.Response: The response from the API.
        """
        return self.session.post(
            f'{self.url}/',
            timeout=10,
            json=data,
        )

    def get(self, obj_id: int | None = None) -> requests.Response:
        """Make a GET request to the API.

        Args:
            obj_id (int | None): The ID of the object to retrieve. If None, retrieves all objects. Defaults to None.

        Returns:
            requests.Response: The response from the API.
        """
        return self.session.get(
            self.url if obj_id is None else f'{self.url}/{obj_id}',
            timeout=10,
        )
    
    def patch(self, obj_id: int, data: dict) -> requests.Response:
        """Make a PATCH request to the API.

        Args:
            obj_id (int): The ID of the object to update.
            data (dict): The data to send in the PATCH request.

        Returns:
            requests.Response: The response from the API.
        """
        return self.session.patch(
            f'{self.url}/{obj_id}/',
            timeout=10,
            json=data,
        )
    
    def delete(self, obj_id: int) -> requests.Response:
        """Make a DELETE request to the API.

        Args:
            obj_id (int): The ID of the object to delete.

        Returns:
            requests.Response: The response from the API.
        """
        return self.session.delete(
            f'{self.url}/{obj_id}/',
            timeout=10,
        )


## API Instances for Specific Endpoints
APIS = {
    'terrain': GenericAPI('terrains'),
    'virus': GenericAPI('viruses'),
    'agent_config': GenericAPI('agent-configs'),
    'prevention': GenericAPI('preventions'),
    'simulation': GenericAPI('simulations'),
    'scenario': GenericAPI('scenarios'),
    'run': GenericAPI('runs'),
    'admin': GenericAPI('admin/mapfiles'),
}


# Response Handler
def handle_response(response: requests.Response) -> dict:
    """
    Handle API response and return formatted tuple for Dash callbacks.
    
    Args:
        response: requests.Response object
    
    Returns:
        Tuple[bool, Any, str]: (success, data, message)
    """
    try:
        if response.ok:
            data = response.json() if response.content else None
            return True, data, "Success"
        else:
            error_msg = response.json().get('detail', response.reason) if response.content else response.reason
            return False, None, error_msg
    except Exception as e:
        return False, None, str(e)


# Operations for Specific Endpoints 
def get_all(resource: str) -> dict:
    """Get all objects from a specific resource endpoint.

    Args:
        resource (str): The resource endpoint to query.

    Returns:
        dict: The result of the operation.
    """
    api = APIS.get(resource)
    if not api:
        return False, None, f"Resource '{resource}' not found."
    return handle_response(APIS[resource].get())


def get_by_id(resource: str, obj_id: int) -> dict:
    """Get a specific object by ID from a resource endpoint.

    Args:
        resource (str): The resource endpoint to query.
        obj_id (int): The ID of the object to retrieve.

    Returns:
        dict: The result of the operation.
    """
    api = APIS.get(resource)
    if not api:
        return False, None, f"Resource '{resource}' not found."
    return handle_response(APIS[resource].get(obj_id))

def create(resource: str, data: dict) -> dict:
    """Create a new object in a specific resource endpoint.

    Args:
        resource (str): The resource endpoint to query.
        data (dict): The data for the new object.

    Returns:
        dict: The result of the operation.
    """
    api = APIS.get(resource)
    if not api:
        return False, None, f"Resource '{resource}' not found."
    return handle_response(APIS[resource].post(data))


def update(resource: str, obj_id: int, data: dict) -> dict:
    """Update an existing object in a specific resource endpoint.

    Args:
        resource (str): The resource endpoint to query.
        obj_id (int): The ID of the object to update.
        data (dict): The updated data for the object.

    Returns:
        dict: The result of the operation.
    """
    api = APIS.get(resource)
    if not api:
        return False, None, f"Resource '{resource}' not found."
    return handle_response(APIS[resource].patch(obj_id, data))

def delete(resource: str, obj_id: int) -> dict:
    """Delete an existing object in a specific resource endpoint.

    Args:
        resource (str): The resource endpoint to query.
        obj_id (int): The ID of the object to delete.

    Returns:
        dict: The result of the operation.
    """
    api = APIS.get(resource)
    if not api:
        return False, None, f"Resource '{resource}' not found."
    return handle_response(APIS[resource].delete(obj_id))

def get_map_files() -> dict:
    """Fetch available map files from admin endpoint."""
    success, data, msg = handle_response(APIS['admin'].get())
    if success and data:
        return True, data.get('mapfiles', []), msg
    return False, [], msg
    