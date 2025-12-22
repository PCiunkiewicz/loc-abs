"""Simulation output preprocessing utilities."""

import multiprocessing
import os
from pathlib import Path
from typing import Literal

import django
import numpy as np
import tables as tb
from django.db import connections
from IPython import get_ipython
from tqdm import tqdm

from api.simulation.models import Run
from utilities.types.config import ScenarioConfig

if get_ipython() is not None:
    os.environ['DJANGO_ALLOW_ASYNC_UNSAFE'] = 'true'


Topic = Literal['agents', 'agent_info', 'virus', 'timesteps']


class ResultLoader:
    """Base class for rendering simulation statistics."""

    cfg: ScenarioConfig
    data: list[np.typing.NDArray]

    def __init__(self, run: int | Run) -> None:
        """Initialize result loader with a run ID or Run object."""
        django.setup()
        for conn in connections.all():
            conn.close()

        self.run = Run.objects.get(id=run) if isinstance(run, int) else run
        if self.run.status != Run.Status.SUCCESS:
            raise ValueError('Cannot load results for incomplete runs.')

        files = list(Path(self.run.save_dir).glob('*.hdf5'))
        with multiprocessing.Pool(6) as p:  # TODO: replace with ProcessPoolExecutor
            self.data = list(tqdm(p.imap_unordered(self._load_hdf, files), total=len(files)))

    def _load_hdf(self, file: Path, topic: Topic = 'agents') -> np.typing.NDArray:
        """Load simulation data from .h5 file."""
        with tb.open_file(file, mode='r') as file:
            return file.root[topic].read()

    def validate(self) -> dict[int, dict[str, bool]]:
        """Validate loaded data for spatial and disease progression."""
        with multiprocessing.Pool(6) as p:  # TODO: replace with ProcessPoolExecutor
            spatial = list(tqdm(p.map(_validate_spatial, self.data), total=len(self.data)))
            disease = list(tqdm(p.map(_validate_disease, self.data), total=len(self.data)))

        return spatial, disease


def _validate_spatial(data: np.ndarray) -> bool:
    """Validate spatial data."""
    # step = self.run.scenario.sim.save_resolution
    step = 24
    return np.all(np.abs(np.diff(data[:, :, :3], axis=0)) <= step)


def _validate_disease(data: np.ndarray) -> bool:
    """Validate disease progression data."""
    s = data[:, :, 3]
    statuses = set(np.unique(s[:-1] * 10 + s[1:]))
    valid_progression = {11, 12, 22, 23, 24, 25, 26, 33, 43, 44, 55, 63, 66}
    return statuses.issubset(valid_progression)
