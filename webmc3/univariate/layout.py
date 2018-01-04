from decorator import decorator

import dash_html_components as html

from ..common.components import selector
from .components import *


def layout(trace):
    varname = trace.varnames[0]

    layout = html.Div([
        html.Center([
            selector('univariate', trace, varname),
            gelman_rubin_p(trace, varname),
            effective_n_p(trace, varname),
            hist_graph(trace, varname),
            lines_graph(trace, varname),
            autocorr_graph(trace, varname)
        ])
    ])

    return layout
