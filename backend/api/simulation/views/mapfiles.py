"""Importer tool for already created simulation run config files."""

from __future__ import annotations

from typing import TYPE_CHECKING

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from utilities import paths

if TYPE_CHECKING:
    from rest_framework.request import Request


class ListMapfiles(APIView):
    """API View to list all simulation mapfiles."""

    def get(self, _: Request) -> Response:
        """Handle GET request to list all simulation mapfiles."""
        mapfiles = [path.name for path in paths.MAPFILES.glob(r'[!.]*')]
        return Response(mapfiles, status=status.HTTP_200_OK)
