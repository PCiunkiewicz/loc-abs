"""Scripting and automation utilities."""

import os
from abc import ABC, abstractmethod

import django
from django.db import connections


class BaseScript(ABC):
    """Base class for all scripts."""

    name: str = __qualname__

    @abstractmethod
    def run(self) -> None:
        """Run the script."""
        raise NotImplementedError('Subclasses must implement the run method.')


class ORMScript(BaseScript):
    """Base class for scripts that use Django ORM."""

    def __init__(self) -> None:
        """Initialize the script."""
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rest.settings')
        os.environ['DJANGO_ALLOW_ASYNC_UNSAFE'] = 'true'

        django.setup()
        for conn in connections.all():
            conn.close()
