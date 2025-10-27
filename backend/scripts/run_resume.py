"""Run resume script."""

from loguru import logger

from api.simulation import models
from simulation.launcher import SimLauncher
from utilities.scripting import ORMScript


class Script(ORMScript):
    """Automation script to bulk resume runs which may have failed."""

    def run(self) -> None:
        """Run the script."""
        runs = range(116, 136)  # Run IDs to attempt resume
        for run_id in runs:
            try:
                run = models.Run.objects.get(id=run_id)
                launcher = SimLauncher(run)
                launcher.resume(await_results=False)
            except Exception as e:
                logger.error(f'Failed to resume run {run_id}: {e}')
