"""Results exploration tools."""

import os
from concurrent.futures import ProcessPoolExecutor
from datetime import datetime
from pathlib import Path

import django
import numpy as np
import tables as tb
from django.db import connections

from api.simulation.models import Run
from utilities.paths import BACKEND
from utilities.types.agent import AgentStatus

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rest.settings')
os.environ['DJANGO_ALLOW_ASYNC_UNSAFE'] = 'true'


class SimResultLoader:
    """Simulation results loader."""

    def __init__(self, run: Run | int) -> None:
        """Initialize the simulation results loader with a run."""
        django.setup()
        for conn in connections.all():
            conn.close()

        self.run = Run.objects.get(id=run) if isinstance(run, int) else run
        self.results_dir = BACKEND / self.run.save_dir
        self.agents = []
        self.timesteps = []
        self.load_results()

    def _load_agents(self, results: Path) -> np.ndarray:
        """Load simulation results from single hdf5."""
        with tb.open_file(results, mode='r') as file:
            return file.root.agents.read()

    def _load_timesteps(self, results: Path) -> np.ndarray:
        """Load simulation results from single hdf5."""
        with tb.open_file(results, mode='r') as file:
            return file.root.timesteps.read()

    def load_results(self) -> tuple[np.ndarray, np.ndarray]:
        """Load results for directory of hdf5."""
        files = list(self.results_dir.glob('*.hdf5'))
        with ProcessPoolExecutor(1) as executor:
            self.agents = list(executor.map(self._load_agents, files))

        self.timesteps = [datetime.fromtimestamp(t) for t in self._load_timesteps(files[0])]

    @property
    def info(self) -> dict:
        """Run information as a dictionary."""
        return {
            'id': self.run.id,
            'name': self.run.name,
            'attack_rate': self.run.scenario.virus.attack_rate,
            'fatality_rate': self.run.scenario.virus.fatality_rate,
            'infection_rate': self.run.scenario.virus.infection_rate,
            'n_agents': len(self.run.agents.custom) + self.run.agents.random_agents,
            **{x.split('=')[0]: x.split('=')[1] for x in self.run.name.split('_')[1:]},
        }

    def count_status(self, status: AgentStatus) -> float:
        """Count status across all agents."""
        return np.mean([count_status(data, status) for data in self.agents])


def count_status(data: np.ndarray, status: AgentStatus) -> int:
    """Count number of agents who were at any point `status`."""
    # Take all timesteps (":" for axis 0), all agents (":" for axis 1), and status ("3" for axis 2)
    status_col = data[:, :, 3]
    # Check each agent if they ever experience a given status
    counts = (status_col == status.value).any(axis=0)
    # Return the sum for all agents
    return counts.sum()
