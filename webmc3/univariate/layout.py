from decorator import decorator

import dash_html_components as html

from .components import *


def layout(trace):
    varname = trace.varnames[0]

    layout = html.Div([
        selector(trace, varname),
        table(trace, varname)
    ])

    return layout


def table(trace, varname):
    return html.Center([
        html.Table([
            html.Tr([
                html.Td(
                    [hist_graph(trace, varname)],
                    style={'width': '40%'}
                ),
                html.Td(
                    [lines_graph(trace, varname)],
                    style={'width': '40%'}
                )
            ]),
            html.Tr([
                html.Td([
                    html.Center([
                        gelman_rubin_p(trace, varname),
                        effective_n_p(trace, varname)
                    ])
                ]),
                html.Td([autocorr_graph(trace, varname)])
            ])
        ],
        style={'tableLayout': 'fixed'})
    ])
