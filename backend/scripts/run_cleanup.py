"""Run cleanup script."""

from loguru import logger

from api.simulation import models
from utilities.scripting import ORMScript


class Script(ORMScript):
    """Automation script to bulk delete runs."""

    def run(self) -> None:
        """Run the script."""
        runs = range(10, 35)  # Run IDs to clean up
        for run_id in runs:
            try:
                run = models.Run.objects.get(id=run_id)
                run.delete()
            except Exception as e:
                logger.error(f'Failed to delete run {run_id}: {e}')
