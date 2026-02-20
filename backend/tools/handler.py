"""Export handler for the backend tools."""

from pathlib import Path
from typing import overload

import django
from django.db import connections

from api.simulation.models import Export, Run
from tools.animation import SimAnimation
from tools.snapshot import SimSnapshot
from tools.stats import EpidemiologicalStatusVsTime, ExcessRiskVsTime, ViralConcentration
from utilities.paths import BACKEND, EXPORTS


class ExportHandler:
    """Handler for exporting simulation data."""

    def __init__(self, run: Run | int, run_file: int | str = 0) -> None:
        """Initialize the simulation launcher with a run."""
        django.setup()
        for conn in connections.all():
            conn.close()

        self.run = Run.objects.get(id=run) if isinstance(run, int) else run
        self.save_dir = BACKEND / self.run.save_dir
        self.mapfile = BACKEND / self.run.scenario.sim.mapfile
        self.config = BACKEND / self.run.config

        self.run_file = self.save_dir / (run_file if isinstance(run_file, str) else self.run_files()[run_file])

    @overload
    def export[**P](self, export: Export, export_type: None = None, name: None = None, **kwargs: P.kwargs) -> None: ...
    @overload
    def export[**P](self, export_type: str, name: str, export: None = None, **kwargs: P.kwargs) -> None: ...
    def export[**P](
        self,
        export: Export | None = None,
        export_type: str | None = None,
        name: str | None = None,
        **kwargs: P.kwargs,
    ) -> None:
        """Export simulation data based on the export type.

        A new Export entry is created if `export=None` and both
        `export_type: str` and `name: str` are provided.
        """
        if export is None:
            try:
                export = Export(run=self.run, name=name, export_type=export_type)
                export.save()
                export.outfile = (
                    EXPORTS.rel
                    / f'{self.run.id:03}-{self.run.name}'
                    / f'{export.id:03}-{export.export_type}-{export.name}'  # TODO: Check why this isn't persisting for GIFs
                )
                export.save()

            except Exception as e:
                raise ValueError(f'Failed to create export: {e}') from e

        outfile = BACKEND / export.outfile
        outfile.parent.mkdir(parents=True, exist_ok=True)

        if export.export_type == 'ANIMATION':
            SimAnimation(self.run_file, self.mapfile).export(outfile, **kwargs)
        elif export.export_type == 'SNAPSHOT':
            SimSnapshot(self.run_file, self.mapfile).export(outfile, **kwargs)
        elif export.export_type == 'EXCESS_RISK':
            ExcessRiskVsTime(self.config, self.run_file).export(outfile, **kwargs)
        elif export.export_type == 'EPIDEMIOLOGICAL_STATUS':
            EpidemiologicalStatusVsTime(self.config, self.run_file).export(outfile, **kwargs)
        elif export.export_type == 'VIRAL_CONCENTRATION':
            ViralConcentration(self.config, self.run_file).export(outfile, **kwargs)
        else:
            raise ValueError(f'Unknown export type: {export_type}')

    @staticmethod
    def get_runs() -> list[Run]:
        """Get all runs associated with the current export handler."""
        return Run.objects.all().order_by('id')

    def run_files(self) -> list[Path]:
        """Get all outputs files for an associated run."""
        return list(self.save_dir.glob('*.hdf5'))
