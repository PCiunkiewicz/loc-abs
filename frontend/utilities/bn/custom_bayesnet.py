"""This module provides various custom Bayesian network topologies using the PyAgrum library."""

from __future__ import annotations

from abc import ABC, abstractmethod
from functools import lru_cache
from typing import Any, ClassVar, overload, override

import numpy as np
import pandas as pd
import pyagrum as gum


class CustomBayesNet(ABC):
    """Custom wrapper class for PyAgrum for parameter-learning Bayesian networks."""

    layout: dict[str, tuple[float, float]]

    @overload
    def __init__(self, *, data: pd.DataFrame) -> None: ...
    @overload
    def __init__(self, *, bn: gum.BayesNet) -> None: ...
    def __init__(self, *, data: pd.DataFrame | None = None, bn: gum.BayesNet | None = None) -> None:
        """Initialize BN with data.

        Params
        ------
        data: pandas.DataFrame
            Dataset you are working with.
        bn: pyagrum.BayesNet
            Pre-constructed Bayesian network to be used for inference.
        """
        if (data is None) == (bn is None):
            raise ValueError('Provide exactly one of data or bn')

        if data is not None:
            self.bn = gum.BayesNet('CustomBayesNet')
            self.data = data.copy()
            for col in self.data:
                self.bn.add(gum.LabelizedVariable(col, col, self._sort(self.data[col].unique())))
        else:
            self.bn = bn

        self.inference = lru_cache()(self._inference)

    @property
    def positions(self) -> dict[str, dict]:
        """Get the positions of the nodes in the Bayesian network."""
        return {node: {'position': 'absolute', 'left': x, 'top': y} for node, (x, y) in self.layout.items()}

    def _remove_unused_nodes(self) -> None:
        """Convenience method for removing unused nodes from the Bayesian network DAG."""
        used_nodes = self.bn.connectedComponents()[0]
        all_nodes: set[int] = self.bn.nodes()
        unused = all_nodes.difference(used_nodes)

        for node in unused:
            self.bn.erase(node)

        self.data = self.data[list(self.bn.names())]
        self.bn = gum.BayesNet('CustomBayesNet')
        for col in self.data:
            self.bn.add(gum.LabelizedVariable(col, col, self._sort(self.data[col].unique())))
        self.topology()

    def _sort(self, vals: list[str]) -> list[str]:
        """Convenience method for sorting numerical intervals for future representation in the NPT graph.

        Params
        ------
        vals: array_like
            Array of generated string labels for sorting.
            DynamicDiscretizer and StatisDiscretizer classes
            are recommended for generating these labels.

        Returns:
        -------
        vals: array_like
            Sorted string labels.
        """
        if all(';' in x for x in vals):
            num = [float(x.split(';')[0][1:]) for x in vals]
            order = np.argsort(num)
            return [vals[i] for i in order]
        return sorted(vals)

    def construct(self) -> None:
        """Bayesian network construction and parameter learning."""
        if not hasattr(self, 'data'):
            raise ValueError('Can only call construct when BayesNet initialized with data.')

        self.topology()
        self._remove_unused_nodes()
        learner = gum.BNLearner(self.data, self.bn)
        # learner.useEM(1e-3)
        learner.useSmoothingPrior()
        learner.fitParameters(self.bn)

    def save(self, filename: str) -> None:
        """Save the Bayesian network to a file.

        Params
        ------
        filename: str
            File path to save the Bayesian network.
        """
        if not filename.endswith('.pkl'):
            filename += '.pkl'
        gum.saveBN(self.bn, filename)

    @classmethod
    def load(cls, filename: str) -> CustomBayesNet:
        """Load the Bayesian network from a file.

        Params
        ------
        filename: str
            File path to load the Bayesian network from.
        """
        if not filename.endswith('.pkl'):
            filename += '.pkl'
        return cls(bn=gum.loadBN(filename))

    def posterior(self, node: str, **evs: Any) -> pd.DataFrame:
        """Get posterior for a single node in the Bayesian network."""
        ie = self.inference(**evs)
        return ie.posterior(node).topandas()

    def posteriors(self, **evs: Any) -> pd.Series:
        """Get posteriors for the Bayesian network."""
        ie = self.inference(**evs)
        return pd.concat([ie.posterior(node).topandas() for node in self.bn.names()])

    def _inference(self, **evs: Any) -> gum.LazyPropagation:
        """Private inference method for caching."""
        ie = gum.LazyPropagation(self.bn)
        ie.setEvidence(evs)
        ie.makeInference()
        return ie

    @abstractmethod
    def topology(self) -> None:
        """Network topology defined when subclassing CustomBayesNet."""


class LocABSBN(CustomBayesNet):
    """Custom Bayesian network for Loc-ABS decision support."""

    layout: ClassVar = {
        'age': (0, 0),
        'immunocompromised': (350, 100),
        'sex': (700, 100),
        'mask': (1050, 75),
        'vax': (1150, 300),
        'role': (350, 420),
        'prevention_index': (700, 400),
        'distancing': (1100, 550),
        'deceased': (0, 800),
        'hospitalized': (400, 800),
        'infected': (800, 800),
        'long_covid': (1200, 800),
    }

    @override
    def topology(self) -> None:
        self.bn.addArc('age', 'hospitalized')
        self.bn.addArc('age', 'role')

        for var in ['age', 'mask', 'vax', 'sex', 'immunocompromised']:
            self.bn.addArc(var, 'prevention_index')

        for var in ['prevention_index', 'role', 'distancing']:
            self.bn.addArc(var, 'infected')

        for var in ['long_covid', 'hospitalized']:
            self.bn.addArc('infected', var)

        self.bn.addArc('hospitalized', 'deceased')
