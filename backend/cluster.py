"""Dask cluster management for parallel simulation runs."""

import argparse
import os
import time
from typing import get_args

from dask.distributed import LocalCluster
from distributed.scheduler import TaskStateState
from loguru import logger

from utilities.paths import BACKEND
from utilities.reloader import Reloader

N_JOBS = os.cpu_count() or 1


def summarize_tasks(cluster: LocalCluster, verbose: bool = True) -> dict[str, int]:
    """Summarize the tasks in the Dask cluster."""
    tasks = cluster.scheduler.tasks.copy()
    summary = {state: sum(1 for task in tasks.values() if task.state == state) for state in get_args(TaskStateState)}
    summary['total'] = len(tasks)
    if verbose:
        logger.info('┌── Task summary ──┐')
        for state, count in summary.items():
            logger.info(f'│ {state.capitalize():<10} {count:>5} │')
        logger.info('└──────────────────┘')
    return summary


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='Dask-Cluster', description='Simulation Dask cluster for multiprocessing.')
    parser.add_argument(
        '--force-reload',
        default=False,
        action='store_true',
        help='Force hot reloading on file-system changes.',
    )
    args = parser.parse_args()

    with Reloader(BACKEND) as reloader:
        logger.info(f'Starting Dask cluster with {N_JOBS} workers...')
        cluster = LocalCluster(
            host='0.0.0.0',
            n_workers=N_JOBS,
            processes=True,
            threads_per_worker=1,
            scheduler_port=8786,
        )
        logger.debug(cluster)
        logger.debug(f'Force reload is {"enabled" if args.force_reload else "disabled"}.')
        logger.success('Dask cluster started, awaiting jobs.')

        try:
            while reloader.is_alive():
                if cluster.scheduler.tasks:
                    summarize_tasks(cluster)
                reloader.join(5)
            if not args.force_reload and (tasks := cluster.scheduler.tasks):
                logger.warning(f'Scheduler has {len(tasks)} active tasks. Waiting for tasks to finish...')
                logger.info('Use cluster flag `--force` to ignore running tasks on reload.')
                while (tasks := summarize_tasks(cluster))['total']:
                    time.sleep(5)
        finally:
            reloader.stop()
            reloader.join()
            logger.warning('Stopping Dask cluster...')
            cluster.close()
