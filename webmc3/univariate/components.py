from __future__ import division

from math import ceil, floor

from dash import dependencies as dep
import dash_core_components as dcc
import dash_html_components as html
from plotly import graph_objs as go

import numpy as np

from ..common.components import add_include_transformed_callback
from ..utils import get_values
from .stats import *


def add_callbacks(app, trace):
    add_include_transformed_callback(app, 'univariate', trace)

    @app.callback(
        dep.Output('univariate-autocorr', 'figure'),
        [dep.Input('univariate-selector', 'value')]
    )
    def update_autocorr(varname):
        return autocorr_figure(trace, varname)

    @app.callback(
        dep.Output('univariate-effective-n', 'children'),
        [dep.Input('univariate-selector', 'value')]
    )
    def update_effective_n(varname):
        return effective_n_p(trace, varname)

    @app.callback(
        dep.Output('univariate-gelman-rubin', 'children'),
        [dep.Input('univariate-selector', 'value')]
    )
    def update_gelman_rubin(varname):
        return gelman_rubin_p(trace, varname)

    @app.callback(
        dep.Output('univariate-hist', 'figure'),
        [
            dep.Input('univariate-selector', 'value'),
            dep.Input('univariate-lines', 'relayoutData')
        ]
    )
    def update_hist(varname, relayoutData):
        if relayoutData is None:
            ix_slice = None
        else:
            try:
                ix_slice = slice(
                    floor(relayoutData['xaxis.range[0]']),
                    ceil(relayoutData['xaxis.range[1]'])
                )
            except KeyError:
                ix_slice = None

        return hist_figure(trace, varname, ix_slice=ix_slice)

    @app.callback(
        dep.Output('univariate-lines', 'figure'),
        [dep.Input('univariate-selector', 'value')]
    )
    def update_lines(varname):
        return lines_figure(trace, varname)


def autocorr_graph(trace, varname):
    return dcc.Graph(
        id='univariate-autocorr',
        figure=autocorr_figure(trace, varname)
    )


def autocorr_figure(trace, varname):
    x = np.arange(len(trace))

    return {
        'data': [
            go.Bar(
                x=x + chain_ix / trace.nchains,
                y=chain_autocorr,
                name="Chain {}".format(chain_ix),
                marker={'line': {'width': 1. / trace.nchains}}
            )
            for chain_ix, chain_autocorr in enumerate(autocorr(trace, varname))
        ],
        'layout': go.Layout(
            xaxis={'title': "Lag"},
            yaxis={'title': "Sample autocorrelation"},
            showlegend=False
        )
    }


def effective_n_p(trace, varname):
    if trace.nchains > 1:
        try:
            text = "Effective sample size = {}".format(effective_n(trace, varname))
        except KeyError:
            text = "Effective sample size not found"
    else:
        text = "Cannot calculate effective sample size with only one chain"

    return html.P(id='univariate-effective-n', children=text)
    

def gelman_rubin_p(trace, varname):
    if trace.nchains > 1:
        text = u"Gelman-Rubin R̂ = {:.4f}".format(gelman_rubin(trace, varname))
    else:
        text = "Cannot calculate Gelman-Rubin statistic with only one chain"

    return html.P(id='univariate-gelman-rubin', children=text) 


def hist_graph(trace, varname):
    return dcc.Graph(
        id='univariate-hist',
        figure=hist_figure(trace, varname)
    )


def hist_figure(trace, varname, ix_slice=None):
    return {
        'data': [
            go.Histogram(x=get_values(trace, varname, ix_slice=ix_slice))
        ],
        'layout': go.Layout(
            yaxis={'title': "Frequency"}
        )
    }


def lines_graph(trace, varname):
    return dcc.Graph(
        id='univariate-lines',
        figure=lines_figure(trace, varname)
    )


def lines_figure(trace, varname):
    x = np.arange(len(trace))

    return {
        'data': [
            go.Scatter(
                x=x, y=y,
                name="Chain {}".format(chain_ix)
            )
            for chain_ix, y in enumerate(
                trace.get_values(varname, combine=False, squeeze=False)
            )
        ],
        'layout': go.Layout(
            yaxis={'title': "Sample value"},
            showlegend=False
        )
    }
