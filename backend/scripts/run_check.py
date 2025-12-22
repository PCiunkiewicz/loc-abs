"""Run check script."""

from pathlib import Path

from loguru import logger

from api.simulation import models
from utilities.scripting import ORMScript


class Script(ORMScript):
    """Automation script to bulk check runs and update their status."""

    def run(self) -> None:
        """Run the script."""
        runs = range(136, 156)  # Run IDs to check
        for run_id in runs:
            try:
                run = models.Run.objects.get(id=run_id)
                filenames = [Path(run.save_dir) / f'{i}.hdf5' for i in range(run.runs)]
                if all([f.exists() for f in filenames]) and run.status != models.Run.Status.SUCCESS:
                    models.Run.objects.filter(id=run.id).update(status=models.Run.Status.SUCCESS)
                    logger.info(f'Run {run_id} marked as SUCCESS.')
            except Exception as e:
                logger.error(f'Failed to check run {run_id}: {e}')
