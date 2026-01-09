"""Localized Epidemiological ABS API Prevention Views."""

from typing import ClassVar

from rest_framework import viewsets

from api.simulation.models import Prevention
from api.simulation.serializers import PreventionSerializer


class PreventionViewSet(viewsets.ModelViewSet):
    """Viewset for Prevention model."""

    queryset = Prevention.objects.all()
    serializer_class = PreventionSerializer
    http_method_names: ClassVar[list] = ['get', 'post', 'patch', 'delete']
    authentication_classes: ClassVar[list] = []  # disables authentication
    permission_classes: ClassVar[list] = []  # disables permission
