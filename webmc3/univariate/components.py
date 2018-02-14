from __future__ import division

from dash import dependencies as dep
import dash_core_components as dcc
import dash_html_components as html
from plotly import graph_objs as go

import numpy as np

from ..common.components import add_include_transformed_callback
from webmc3.utils import get_ix_slice


def add_callbacks(app, trace_info):
    add_include_transformed_callback(app, 'univariate', trace_info)

    @app.callback(
        dep.Output('univariate-autocorr', 'figure'),
        [
            dep.Input('univariate-selector', 'value'),
            dep.Input('univariate-lines', 'relayoutData')
        ]
    )
    def update_autocorr(varname, relayoutData):
        ix_slice = get_ix_slice(relayoutData)

        return autocorr_figure(trace_info, varname, ix_slice=ix_slice)

    @app.callback(
        dep.Output('univariate-effective-n', 'children'),
        [dep.Input('univariate-selector', 'value')]
    )
    def update_effective_n(varname):
        return effective_n_p(trace_info, varname)

    @app.callback(
        dep.Output('univariate-gelman-rubin', 'children'),
        [dep.Input('univariate-selector', 'value')]
    )
    def update_gelman_rubin(varname):
        return gelman_rubin_p(trace_info, varname)

    @app.callback(
        dep.Output('univariate-hist', 'figure'),
        [
            dep.Input('univariate-selector', 'value'),
            dep.Input('univariate-lines', 'relayoutData')
        ]
    )
    def update_hist(varname, relayoutData):
        ix_slice = get_ix_slice(relayoutData)

        return hist_figure(trace_info, varname, ix_slice=ix_slice)

    @app.callback(
        dep.Output('univariate-lines', 'figure'),
        [dep.Input('univariate-selector', 'value')]
    )
    def update_lines(varname):
        return lines_figure(trace_info, varname)


def autocorr_graph(trace_info, varname):
    return dcc.Graph(
        id='univariate-autocorr',
        figure=autocorr_figure(trace_info, varname)
    )


def autocorr_figure(trace_info, varname, ix_slice=None):
    max_lag = min(100, len(trace_info))

    if ix_slice is not None:
        max_lag = min(max_lag, ix_slice.stop - ix_slice.start)

    x = np.arange(max_lag)

    return {
        'data': [
            go.Bar(
                x=x + chain_ix / trace_info.nchains,
                y=chain_autocorr,
                name="Chain {}".format(chain_ix),
                marker={'line': {'width': 1. / trace_info.nchains}}
            )
            for chain_ix, chain_autocorr in enumerate(
                trace_info.autocorr(varname, ix_slice=ix_slice)
            )
        ],
        'layout': go.Layout(
            xaxis={'title': "Lag"},
            yaxis={'title': "Sample autocorrelation"},
            showlegend=False
        )
    }


def effective_n_p(trace_info, varname):
    if trace_info.nchains > 1:
        try:
            text = "Effective sample size = {}".format(
                trace_info.effective_n[varname]
            )
        except KeyError:
            text = "Effective sample size not found"
    else:
        text = "Cannot calculate effective sample size with only one chain"

    return html.P(id='univariate-effective-n', children=text)
    

def gelman_rubin_p(trace_info, varname):
    if trace_info.nchains > 1:
        text = u"Gelman-Rubin R̂ = {:.4f}".format(
            trace_info.gelman_rubin[varname]
        )
    else:
        text = "Cannot calculate Gelman-Rubin statistic with only one chain"

    return html.P(id='univariate-gelman-rubin', children=text) 


def hist_graph(trace_info, varname):
    return dcc.Graph(
        id='univariate-hist',
        figure=hist_figure(trace_info, varname)
    )


def hist_figure(trace_info, varname, ix_slice=None):
    return {
        'data': [
            go.Histogram(x=trace_info.get_values(varname, ix_slice=ix_slice))
        ],
        'layout': go.Layout(
            yaxis={'title': "Frequency"}
        )
    }


def lines_graph(trace_info, varname):
    return dcc.Graph(
        id='univariate-lines',
        figure=lines_figure(trace_info, varname)
    )


def lines_figure(trace_info, varname):
    x = np.arange(len(trace_info))

    return {
        'data': [
            go.Scatter(
                x=x, y=y,
                name="Chain {}".format(chain_ix)
            )
            for chain_ix, y in enumerate(
                trace_info.get_values(varname, combine=False)
            )
        ],
        'layout': go.Layout(
            yaxis={'title': "Sample value"},
            showlegend=False
        )
    }
