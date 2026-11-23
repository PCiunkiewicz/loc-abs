"""Dash app for COVID DSS using a custom Bayesian network."""

import time
import uuid
from pathlib import Path
from typing import Any

import plotly.express as px
import plotly.graph_objs as go
from cachetools import TTLCache, cached
from dash import ALL, Input, Output, callback, dcc, html
from dash.exceptions import PreventUpdate

from utilities.bn.custom_bayesnet import LocABSBN

BN_ROOT = Path(__file__).parent.parent / 'utilities/bn'
UPDATE_TIMEOUT = 1.0  # seconds


class DashBNGraph(html.Div):
    """Class for generating Dash graphs from Bayesian network posteriors."""

    @cached(cache=TTLCache(maxsize=1024, ttl=3600))
    def __init__(self, session_id: uuid.UUID) -> None:
        """Initialize the DashBNGraph with a CustomBayesNet instance."""
        self.bn = LocABSBN.load(str(BN_ROOT / 'bn.pkl'))
        self.data = self.bn.posteriors()
        self.graphs = {node: self.draw_bar(node) for node in self.bn.bn.names()}
        self.latest = time.time()

        super().__init__(
            [
                dcc.Store(data=session_id, id='session-id'),
                html.Div(
                    [
                        dcc.Graph(
                            id={'type': 'node-graph', 'index': node},
                            figure=fig,
                            config={'displayModeBar': False},
                            animate=True,
                            style=self.bn.positions.get(node, {}),
                        )
                        for node, fig in self.graphs.items()
                    ],
                    id='graph-container',
                    style={
                        'background-image': 'url(/static/background.png)',
                        'background-size': 'contain',
                        'position': 'absolute',
                        'width': '1500px',
                        'height': '100%',
                    },
                ),
            ],
        )

    @property
    def updating(self) -> bool:
        """Check if the graph is currently updating."""
        return time.time() - self.latest < 1.0

    def draw_bar(self, node: str) -> go.Figure:
        """Draw a bar chart for the given node's posterior distribution."""
        title = node.replace('_', ' ').capitalize()
        fig = px.bar(self.data[node] * 100, x=0, orientation='h', range_x=[0, 100], title=title)
        fig.update_xaxes(visible=False, fixedrange=True)
        fig.update_yaxes(ticklabelposition='inside', title=None, fixedrange=True)
        fig.update_traces(
            hoverinfo='none',
            hovertemplate=None,
            textposition='none',
            marker={'color': 'lightgreen'},
            selected={'marker': {'color': 'orange'}},
        )
        fig.update_layout(
            autosize=False,
            height=len(self.data[node]) * 30 + 40,
            margin={'l': 15, 'r': 15, 't': 25, 'b': 15},
            width=300,
            title_x=0.5,
            title_yanchor='middle',
            title_xanchor='center',
            paper_bgcolor='lightgray',
            clickmode='event+select',
        )

        return self.annotate(fig, node)

    def annotate(self, fig: go.Figure, node: str) -> go.Figure:
        """Annotate the bar chart with posterior probabilities."""
        for label, value in self.data[node].items():
            fig.add_annotation(
                x=1,
                y=label,
                xref='paper',
                text=f'{value * 100:.2f}%',
                showarrow=False,
                xanchor='right',
                yanchor='middle',
            )
        return fig

    def update(self, **evs: Any) -> dict[str, go.Figure]:
        """Update the graphs based on new evidence."""
        self.data = self.bn.posteriors(**evs)
        for node, fig in self.graphs.items():
            fig.update_traces(
                x=self.data[node] * 100,
                selectedpoints=[i for i, val in enumerate(evs.get(node, [])) if val],
            )
            fig.layout.annotations = []
            self.graphs[node] = self.annotate(fig, node)

        return self.graphs


@callback(
    Output({'type': 'node-graph', 'index': ALL}, 'figure'),
    Input({'type': 'node-graph', 'index': ALL}, 'selectedData'),
    Input({'type': 'node-graph', 'index': ALL}, 'id'),
    Input('session-id', 'data'),
    prevent_initial_call=True,
)
def update_bn(selected: list[dict], ids: list[dict], session_id: uuid.UUID) -> list[dcc.Graph]:
    """Update the Bayesian network graphs based on selected data."""
    graph = DashBNGraph(session_id)
    graph.latest = time.time()
    time.sleep(UPDATE_TIMEOUT)
    if not graph.updating:
        evs = {i['index']: d['points'] for d, i in zip(selected, ids, strict=True) if d is not None}
        for node, points in evs.items():
            evidence = [p['y'] for p in points]
            labels = graph.bn.bn.variable(node).labels()
            evidence = tuple(1 if x in evidence else 0 for x in labels)
            evs[node] = evidence
        graph.update(**evs)
        return list(graph.graphs.values())
    raise PreventUpdate
