"""Export handler for the backend tools."""

import django
from django.db import connections

from api.simulation.models import Export, Run
from tools.animation import SimAnimation
from tools.snapshot import SimSnapshot
from tools.stats import EpidemiologicalStatusVsTime, ExcessRiskVsTime, ViralConcentration
from utilities.paths import BACKEND, EXPORTS


class ExportHandler:
    """Handler for exporting simulation data."""

    def __init__(self, run: Run | int) -> None:
        """Initialize the simulation launcher with a run."""
        django.setup()
        for conn in connections.all():
            conn.close()

        self.run = Run.objects.get(id=run) if isinstance(run, int) else run
        self.save_dir = BACKEND / self.run.save_dir
        self.mapfile = BACKEND / self.run.scenario.sim.mapfile
        self.config = BACKEND / self.run.config

    def export(self, export_type: str, name: str, run_file: str, **kwargs) -> None:
        """Export simulation data based on the export type."""
        try:
            export = Export(run=self.run, name=name, export_type=export_type)
            export.save()
            export.outfile = (
                EXPORTS.rel / f'{self.run.id:03}-{self.run.name}' / f'{export.export_type}-{export.id:03}-{export.name}'
            )
            export.save()
            outfile = BACKEND / export.outfile
            outfile.parent.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            raise ValueError(f'Failed to create export: {e}')

        if export_type == 'ANIMATION':
            SimAnimation(self.save_dir / run_file, self.mapfile).export(outfile, **kwargs)
        elif export_type == 'SNAPSHOT':
            SimSnapshot(self.save_dir / run_file, self.mapfile).export(outfile, **kwargs)
        elif export_type == 'EXCESS_RISK':
            ExcessRiskVsTime(self.config, self.save_dir / run_file).export(outfile, **kwargs)
        elif export_type == 'EPIDEMIOLOGICAL_STATUS':
            EpidemiologicalStatusVsTime(self.config, self.save_dir / run_file).export(outfile, **kwargs)
        elif export_type == 'VIRAL_CONCENTRATION':
            ViralConcentration(self.config, self.save_dir / run_file).export(outfile, **kwargs)
        else:
            raise ValueError(f'Unknown export type: {export_type}')

    @staticmethod
    def get_runs() -> list[Run]:
        """Get all runs associated with the current export handler."""
        return Run.objects.all().order_by('id')
