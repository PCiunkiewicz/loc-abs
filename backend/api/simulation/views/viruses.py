"""Localized Epidemiological ABS API Virus Views."""

from typing import ClassVar

from rest_framework import viewsets

from api.simulation.models import Virus
from api.simulation.serializers import VirusSerializer


class VirusViewSet(viewsets.ModelViewSet):
    """Viewset for Virus model."""

    queryset = Virus.objects.all()
    serializer_class = VirusSerializer
    http_method_names: ClassVar[list] = ['get', 'post', 'patch', 'delete']
    authentication_classes: ClassVar[list] = []  # disables authentication
    permission_classes: ClassVar[list] = []  # disables permission
