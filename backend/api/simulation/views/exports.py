"""Localized Epidemiological ABS API Export Views."""

import shutil
from typing import ClassVar, override

from rest_framework import status, viewsets
from rest_framework.request import Request
from rest_framework.response import Response

from api.simulation.models import Export, Run
from api.simulation.serializers import ExportSerializer
from utilities.paths import EXPORTS


class ExportViewSet(viewsets.ModelViewSet):
    """API Viewset for Export model."""

    queryset = Export.objects.all()
    serializer_class = ExportSerializer
    http_method_names: ClassVar[list] = ['get', 'post', 'patch', 'delete']
    authentication_classes: ClassVar[list] = []  # disables authentication
    permission_classes: ClassVar[list] = []  # disables permission

    @override
    def create(self, request: Request) -> Response:
        serializer = ExportSerializer(data=request.data)
        if serializer.is_valid():
            export: Export = serializer.save()
            run: Run = export.run

            export.outfile = (
                EXPORTS.rel / f'{run.id:03}-{run.name}' / f'{export.export_type}-{export.id:03}-{export.name}'
            )
            export.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @override
    def partial_update(self, request: Request, pk: int) -> Response:
        try:
            export = Export.objects.get(id=pk)
        except Export.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        name = request.data.get('name', export.name)
        run = export.run
        response = super().partial_update(request, pk=pk)

        if name != export.name:
            path = EXPORTS.rel / f'{run.id:03}-{run.name}' / f'{export.export_type}-{export.id:03}-{name}'
            request.data['outfile'] = str(path)
            shutil.move(export.outfile, path)
            response = super().partial_update(request, pk=pk)

        return response
