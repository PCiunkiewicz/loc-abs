"""Dash app for COVID DSS using a custom Bayesian network."""

import os
import time
from pathlib import Path
from typing import Any, override

import plotly.express as px
import plotly.graph_objs as go
from dash import ALL, Dash, Input, Output, callback, dcc, html
from dash.exceptions import PreventUpdate
from dynamic_discretization.custom_bayesnet import CustomBayesNet

os.chdir(Path(__file__).parent)


class CovidBN(CustomBayesNet):
    """Custom Bayesian network for COVID DSS."""

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


class DashBNGraph:
    """Class for generating Dash graphs from Bayesian network posteriors."""

    UPDATE_TIMEOUT = 1.0  # seconds

    def __init__(self, bn: CustomBayesNet) -> None:
        """Initialize the DashBNGraph with a CustomBayesNet instance."""
        self.bn = bn
        self.data = self.bn.posteriors()
        self.graphs = {node: self.draw_bar(node) for node in self.bn.bn.names()}
        self.latest = time.time()

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


bn = CovidBN.load('bn.pkl')

graph = DashBNGraph(bn)
positions = {
    'age': {'position': 'absolute', 'left': 0, 'top': 0},
    'immunocompromised': {'position': 'absolute', 'left': 350, 'top': 100},
    'sex': {'position': 'absolute', 'left': 700, 'top': 100},
    'mask': {'position': 'absolute', 'left': 1050, 'top': 75},
    'vax': {'position': 'absolute', 'left': 1150, 'top': 300},
    'role': {'position': 'absolute', 'left': 350, 'top': 420},
    'prevention_index': {'position': 'absolute', 'left': 700, 'top': 400},
    'distancing': {'position': 'absolute', 'left': 1100, 'top': 550},
    'deceased': {'position': 'absolute', 'left': 0, 'top': 800},
    'hospitalized': {'position': 'absolute', 'left': 400, 'top': 800},
    'infected': {'position': 'absolute', 'left': 800, 'top': 800},
    'long_covid': {'position': 'absolute', 'left': 1200, 'top': 800},
}

app = Dash(__name__)
app.layout = html.Div(
    [
        html.Div(
            [
                dcc.Graph(
                    id={'type': 'node-graph', 'index': node},
                    figure=fig,
                    config={'displayModeBar': False},
                    animate=True,
                    style=positions.get(node, {}),
                )
                for node, fig in graph.graphs.items()
            ],
            id='graph-container',
            style={
                'background-image': 'url(/assets/background.png)',
                'background-size': 'contain',
                'position': 'absolute',
                'width': '1500px',
                'height': '100%',
            },
        ),
    ],
)


@callback(
    Output({'type': 'node-graph', 'index': ALL}, 'figure'),
    Input({'type': 'node-graph', 'index': ALL}, 'selectedData'),
    Input({'type': 'node-graph', 'index': ALL}, 'id'),
    prevent_initial_call=True,
)
def update_bn(selected: list[dict], ids: list[dict]) -> list[dcc.Graph]:
    """Update the Bayesian network graphs based on selected data."""
    graph.latest = time.time()
    time.sleep(graph.UPDATE_TIMEOUT)
    if not graph.updating:
        evs = {i['index']: d['points'] for d, i in zip(selected, ids, strict=True) if d is not None}
        for node, points in evs.items():
            evidence = [p['y'] for p in points]
            labels = bn.bn.variable(node).labels()
            evidence = tuple(1 if x in evidence else 0 for x in labels)
            evs[node] = evidence
        graph.update(**evs)
        return list(graph.graphs.values())
    raise PreventUpdate


if __name__ == '__main__':
    app.run(debug=True, port=8051)
