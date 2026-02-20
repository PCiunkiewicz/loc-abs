"""Tools for  exporting simulation snapshots as image files."""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import tables as tb
from matplotlib import image
from matplotlib.colors import ListedColormap

from simulation.scenario import VIRUS_SCALE
from utilities.tools import STATUS_COLOR, reshape, str_date
from utilities.types.agent import AgentStatus


class SimSnapshot:
    """Base Model class for rendering frame snapshots from simulations.

    Attributes:
        img: Loaded mapfile image.
        agents: Array of agent positions and statuses.
        virus: Array of virus data for each floor.
        timesteps: Array of simulation timesteps.
    """

    img: np.typing.NDArray
    agents: np.typing.NDArray
    virus: np.typing.NDArray
    timesteps: np.typing.NDArray

    def __init__(self, results: Path, mapfile: Path) -> None:
        """Initialize the snapshot with simulation and map files.

        Args:
            results: Path to the simulation output .h5 file.
            mapfile: Path to the map image or directory containing map images.
        """
        self.imgs = []
        if mapfile.is_dir():
            for file in sorted(mapfile.iterdir()):
                if file.suffix == '.png' and '.nodes' not in file.suffixes:
                    self.imgs.append(image.imread(file))
        else:
            self.imgs.append(image.imread(mapfile))
        self.exits = [np.all(np.isclose(img, (1, 1, 0, 1)), axis=2) for img in self.imgs]

        with tb.open_file(results, mode='r') as file:
            self.agents = file.root.agents.read()
            self.timesteps = file.root.timesteps.read()
            try:
                self.virus = file.root.virus.read()
            except tb.NoSuchNodeError:
                self.virus = np.zeros((*self.imgs[0].shape[:2], len(self.imgs)))

    def export(self, outfile: Path, frame_idx: int) -> None:
        """Export snapshot to output file.

        Args:
            outfile: Path to the output file.
            frame_idx: Index of the snapshot frame to export.
        """
        ncols = min(2, len(self.imgs))
        self.fig, self.axes = plt.subplots(
            nrows=len(self.imgs) // ncols,
            ncols=ncols,
            figsize=[8 * ncols, 4 * len(self.imgs) // ncols],
        )
        self.axes = self.axes.flatten()
        self.fig.subplots_adjust(left=0, bottom=0, right=1, top=0.95)

        for floor in range(len(self.imgs)):
            self.draw_floor(floor, frame_idx)

        plt.savefig(outfile, dpi=300, bbox_inches='tight')

    def draw_floor(self, floor: int, i: int) -> None:
        """Draw frame from simulation results for a given floor.

        Args:
            floor: Floor number to draw.
            i: Frame index to draw.
        """
        ax: plt.Axes = self.axes[floor]
        ax.set_title(f'Floor {floor}\n', fontweight='bold', fontsize=14)
        ax.axis('off')

        ax.imshow(self.imgs[floor])
        ax.imshow(
            self.virus[i, :, :, floor] != 0,
            alpha=(self.virus[i, :, :, floor] / VIRUS_SCALE) ** 0.35,
            cmap=ListedColormap(['white', 'red'], N=2),
            vmin=0,
            vmax=1,
        )

        info = [f'{str_date(self.timesteps[i])}\n']
        for status in AgentStatus:
            agents = reshape(self.agents[i], status.value, floor)
            info.append(f'{status.name.capitalize()}: {agents.shape[1]}')
        ax.text(
            x=0.03,
            y=0.05,
            s='\n'.join(info),
            c='black',
            fontsize=8,
            fontweight='bold',
            horizontalalignment='left',
            verticalalignment='bottom',
            transform=ax.transAxes,
        )

        for status in AgentStatus:
            ax.plot(
                *reshape(self.agents[i], status.value, floor),
                'o',
                ms=4,
                mew=0.25,
                c=STATUS_COLOR[status.name],
                mec='black',
                label=status.name,
            )

        for agent in range(self.agents.shape[1]):
            x, y, z = self.agents[i, agent][:3]
            if z == floor and not self.exits[z][x, y]:
                ax.text(
                    y,
                    x,
                    agent,
                    fontsize=2,
                    c='black',
                    horizontalalignment='center',
                    verticalalignment='center',
                )
