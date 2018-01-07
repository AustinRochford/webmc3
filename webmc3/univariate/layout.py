from decorator import decorator

import dash_html_components as html

from ..common.components import selector
from .components import *


def layout(trace_info):
    varname = trace_info.get_varnames()[0]

    layout = html.Div([
        html.Center([
            selector('univariate', trace_info, varname),
            gelman_rubin_p(trace_info, varname),
            effective_n_p(trace_info, varname),
            hist_graph(trace_info, varname),
            lines_graph(trace_info, varname),
            autocorr_graph(trace_info, varname)
        ])
    ])

    return layout
