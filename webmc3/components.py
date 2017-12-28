from __future__ import division

import dash
import dash_core_components as dcc
import dash_html_components as html
from plotly import graph_objs as go

import numpy as np

from .stats import *


def add_var_callbacks(app, trace):
    @app.callback(
        dash.dependencies.Output('var-autocorr', 'figure'),
        [dash.dependencies.Input('var-selector', 'value')]
    )
    def update_var_autocorr(varname):
        return var_autocorr_figure(trace, varname)

    @app.callback(
        dash.dependencies.Output('var-effective-n', 'children'),
        [dash.dependencies.Input('var-selector', 'value')]
    )
    def update_var_effective_n(varname):
        return var_effective_n(trace, varname)

    @app.callback(
        dash.dependencies.Output('var-gelman-rubin', 'children'),
        [dash.dependencies.Input('var-selector', 'value')]
    )
    def update_var_gelman_rubin(varname):
        return var_gelman_rubin(trace, varname)

    @app.callback(
        dash.dependencies.Output('var-hist', 'figure'),
        [dash.dependencies.Input('var-selector', 'value')]
    )
    def update_var_hist(varname):
        return var_hist_figure(trace, varname)

    @app.callback(
        dash.dependencies.Output('var-lines', 'figure'),
        [dash.dependencies.Input('var-selector', 'value')]
    )
    def update_var_lines(varname):
        return var_lines_figure(trace, varname)


def var_autocorr(trace, varname):
    return dcc.Graph(
        id='var-autocorr',
        figure=var_autocorr_figure(trace, varname)
    )


def var_autocorr_figure(trace, varname):
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


def var_effective_n(trace, varname):
    return html.P(
        id='var-effective-n',
        children=u"Effective sample size = {}".format(effective_n(trace, varname))
    )
    

def var_gelman_rubin(trace, varname):
    return html.P(
        id='var-gelman-rubin',
        children=u"Gelman-Rubin R̂ = {:.4f}".format(gelman_rubin(trace, varname))
    )


def var_hist(trace, varname):
    return dcc.Graph(
        id='var-hist',
        figure=var_hist_figure(trace, varname)
    )


def var_hist_figure(trace, varname):
    return {
        'data': [
            go.Histogram(x=trace[varname])
        ],
        'layout': go.Layout(
            yaxis={'title': "Frequency"}
        )
    }


def var_lines(trace, varname):
    return dcc.Graph(
        id='var-lines',
        figure=var_lines_figure(trace, varname)
    )


def var_lines_figure(trace, varname):
    x = np.arange(len(trace))

    return {
        'data': [
            go.Scatter(
                x=x, y=y,
                name="Chain {}".format(chain_ix)
            )
            for chain_ix, y in enumerate(trace.get_values(varname, combine=False))
        ],
        'layout': go.Layout(
            yaxis={'title': "Sample value"},
            showlegend=False
        )
    }


def var_selector(trace, varname):
    return html.Div(
        [
            html.Label("Variable"),
            dcc.Dropdown(
                id='var-selector',
                value=varname,
                options=[
                    {
                        'label': varname,
                        'value': varname
                    }
                    for varname in trace.varnames
                ]
            )
        ],
        style={'width': '20%'}
    )
