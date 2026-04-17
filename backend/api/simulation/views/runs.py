"""Localized Epidemiological ABS API Run Views."""

import json
import shutil
from multiprocessing import Process
from pathlib import Path
from typing import ClassVar, override

from django.db.models import QuerySet
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.generics import ListAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from api.simulation.models import Export, Run
from api.simulation.serializers import ExportSerializer, NestedRunSerializer, RunSerializer
from simulation.launcher import SimLauncher
from utilities import paths


class RunViewSet(viewsets.ModelViewSet):
    """API Viewset for Run model."""

    queryset = Run.objects.all()
    serializer_class = NestedRunSerializer
    http_method_names: ClassVar[list] = ['get', 'post', 'patch', 'delete']
    authentication_classes: ClassVar[list] = []  # disables authentication
    permission_classes: ClassVar[list] = []  # disables permission

    @override
    def list(self, request: Request) -> Response:
        queryset = self.filter_queryset(self.get_queryset())

        serializer = RunSerializer(queryset, many=True)
        return Response(serializer.data)

    @override
    def create(self, request: Request) -> Response:
        serializer = NestedRunSerializer(data=request.data)
        if serializer.is_valid():
            run: Run = serializer.save()
            run.save_dir = paths.OUTPUTS.rel / f'{run.id:03}-{run.name}'
            run.logfile = paths.LOGS.rel / f'{run.id:03}-{run.name}.log'
            run.config = paths.CFG.rel / f'{run.id:03}-{run.name}.json'
            run.save()

            run.config.write_text(json.dumps(serializer.data, indent=2))

            launcher = SimLauncher(run)
            Process(target=launcher.start, daemon=True).start()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @override
    def partial_update(self, request: Request, pk: int) -> Response:
        run = get_object_or_404(Run, pk=pk)
        name = request.data.get('name', run.name)
        response = super().partial_update(request, pk=pk)

        if name != run.name:
            new_paths = {
                'save_dir': str(paths.OUTPUTS.rel / f'{run.id:03}-{name}'),
                'logfile': str(paths.LOGS.rel / f'{run.id:03}-{name}.log'),
                'config': str(paths.CFG.rel / f'{run.id:03}-{name}.json'),
            }

            for key, new_path in new_paths.items():
                request.data[key] = new_path
                if Path(old_path := getattr(run, key)).exists():
                    shutil.move(old_path, new_path)
            response = super().partial_update(request, pk=pk)

        return response


class CheckRunStatus(APIView):
    """API View to check runs for completion."""

    def get(self, _: Request, pk: int) -> Response:
        """Handle GET request to check run(s) status and update accordingly."""
        run = get_object_or_404(Run, pk=pk)
        outputs = len(list(Path(run.save_dir).iterdir()))
        progress = round(outputs / run.runs * 100, 2)

        if outputs == run.runs:
            run.status = Run.Status.SUCCESS
            run.save()

        result = {'status': run.status, 'outputs': outputs, 'total': run.runs, 'progress': progress}
        return Response(result, status=status.HTTP_200_OK)


class ListRunOutputs(APIView):
    """API View to list run output files."""

    def get(self, _: Request, pk: int) -> Response:
        """Handle GET request to list all run output files."""
        run = get_object_or_404(Run, pk=pk)
        outputs = [path.name for path in Path(run.save_dir).iterdir()]
        return Response(outputs, status=status.HTTP_200_OK)


class ListRunExports(ListAPIView):
    """API view to list exports for a specific run."""

    serializer_class = ExportSerializer

    def get_queryset(self) -> QuerySet[Export]:
        """Get exports queryset filtered by run ID."""
        run = get_object_or_404(Run, pk=self.kwargs['pk'])
        return Export.objects.filter(run=run).order_by('-id')
