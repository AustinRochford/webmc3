import dash_core_components as dcc
import dash_html_components as html
from plotly import graph_objs as go

import numpy as np


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
            title=varname,
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
            title=varname,
            yaxis={'title': "Sample value"}
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
