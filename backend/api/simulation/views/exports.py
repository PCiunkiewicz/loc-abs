"""Localized Epidemiological ABS API Export Views."""

import shutil
from multiprocessing import Process
from pathlib import Path
from typing import ClassVar, override

from django.http import FileResponse
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from api.simulation.models import Export, Run
from api.simulation.serializers import ExportSerializer
from tools.handler import ExportHandler
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
            if export.export_type == 'SNAPSHOT' and 'frame_idx' not in export.params:
                export.params['frame_idx'] = 0
            export.save()

            handler = ExportHandler(run, export.params.pop('run_file', default=0))
            Process(target=handler.export, kwargs={'export': export, **export.params}, daemon=True).start()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @override
    def partial_update(self, request: Request, pk: int) -> Response:
        export = get_object_or_404(Export, pk=pk)
        name = request.data.get('name', export.name)
        run = export.run
        response = super().partial_update(request, pk=pk)

        if name != export.name:
            path = EXPORTS.rel / f'{run.id:03}-{run.name}' / f'{export.export_type}-{export.id:03}-{name}'
            request.data['outfile'] = str(path)
            if Path(export.outfile).exists():
                shutil.move(export.outfile, path)
            response = super().partial_update(request, pk=pk)

        return response


class DownloadExportFile(APIView):
    """API View to handle downloading of export files."""

    def get(self, _: Request, pk: int) -> FileResponse | Response:
        """Handle GET request to download an export file."""
        export = get_object_or_404(Export, pk=pk)
        outfile = Path(export.outfile)

        if outfile.is_file():
            # as_attachment=True prompts a 'Save As' dialog in the browser
            return FileResponse(outfile.open('rb'), as_attachment=True, filename=outfile.name)

        return Response({'error': 'File not found'}, status=status.HTTP_404_NOT_FOUND)
