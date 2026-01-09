"""Localized Epidemiological ABS API Agent Config Views."""

from typing import ClassVar

from rest_framework import viewsets

from api.simulation.models import AgentConfig
from api.simulation.serializers import AgentConfigSerializer


class AgentConfigViewSet(viewsets.ModelViewSet):
    """Viewset for Agent Config model."""

    queryset = AgentConfig.objects.all()
    serializer_class = AgentConfigSerializer
    http_method_names: ClassVar[list] = ['get', 'post', 'patch', 'delete']
    authentication_classes: ClassVar[list] = []  # disables authentication
    permission_classes: ClassVar[list] = []  # disables permission
